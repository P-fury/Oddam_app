from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View

from oddam_app.forms import UserEditForm, UserPasswordEditForm
from oddam_app.models import Donation, Institution, Category
from user.forms import CustomUserCreationForm
from user.models import CustomUser
from user.utils import send_activation_email


# Create your views here.


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = CustomUser.objects.create_user(username=email, email=email, password=password, first_name=first_name,
                                                  last_name=last_name)
            send_activation_email(user, request)
            return redirect('login')

        else:
            return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['email']
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            try:
                exisitng_user = CustomUser.objects.get(username=username)
                messages.error(request, 'Niepoprawne hasło')
                return redirect('login')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Nie ma takiego użytkownika')
                return redirect('register')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class UserSiteView(View):
    def get(self, request):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)
        donations = Donation.objects.filter(user=user).order_by('is_taken', 'pick_up_date')
        number_of_bags = sum([bags.quantity for bags in donations])

        context = {
            'user': user,
            'number_of_bags': number_of_bags,
            'donations': donations,
            'today': date.today(),

        }
        return render(request, 'user-site.html', context)

    def post(self, request):
        donation_id = request.POST.get('donation_id')
        is_taken = request.POST.get('is_taken') == 'true'
        donation = Donation.objects.get(id=donation_id)
        donation.is_taken = is_taken
        donation.save()
        return JsonResponse({'success': True, 'message': 'Stan darowizny został pomyślnie zaktualizowany.'})


class UserEditView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login-user')

    def get(self, request):
        userEdit = UserEditForm(instance=request.user)
        userPasswordEditForm = UserPasswordEditForm(user=request.user)
        messages.add_message(request, messages.INFO, "aby zmienic dane podaj haslo", extra_tags='edit_data')
        return render(request, 'user-edit.html', {'userEdit': userEdit, 'userPasswordEditForm': userPasswordEditForm})

    def post(self, request):
        url1 = reverse('user_edit') + '#user_data'
        url2 = reverse('user_edit') + '#user_password'
        if 'edit_data' in request.POST:
            password = request.POST.get("confirm-password")
            if request.user.check_password(password):
                name = request.POST.get("first_name")
                lastname = request.POST.get("last_name")
                email = request.POST.get("email")
                user = CustomUser.objects.get(id=request.user.id)
                user.first_name = name
                user.last_name = lastname
                user.email = email
                user.save()
                messages.add_message(request, messages.INFO, "dane zmienione", extra_tags='edit_data')
                return redirect(url1)
            else:
                messages.add_message(request, messages.INFO, "haslo niepoprawne", extra_tags='edit_data')
                return redirect(url1)

        elif 'change_password' in request.POST:
            user_password_edit_form = UserPasswordEditForm(request.user, request.POST)
            if user_password_edit_form.is_valid():
                user = user_password_edit_form.save()
                update_session_auth_hash(request, user)
                messages.add_message(request, messages.INFO, "Hasło zmienione", extra_tags='edit_password')
                return redirect(url2)
            else:
                for field in user_password_edit_form:
                    for error in field.errors:
                        messages.error(request, f"{field.label}: {error}", extra_tags='edit_password')
                        return redirect(url2)

        return redirect('user_edit')


class LandingPageView(View):
    def get(self, request, page=1):
        amount_of_bags = sum([item.quantity for item in Donation.objects.all()])
        number_of_institution = Institution.objects.all().count()
        institutions = Institution.objects.all()

        # PAGINATOR

        # FUNDATIONS
        fundations = institutions.filter(type='fundacja').order_by('name')
        paginator_fundation = Paginator(fundations, per_page=5)
        page = request.GET.get('page')
        paginator_fundation = paginator_fundation.get_page(page)

        # ORGANIZATION
        organizations = institutions.filter(type='organizacja_pozarządowa').order_by('name')
        paginator_organizations = Paginator(organizations, per_page=5)
        pageorg = request.GET.get('page')
        paginator_organizations = paginator_organizations.get_page(pageorg)

        # LOCAL
        locals = institutions.filter(type='zbiórka_lokalna').order_by('name')
        paginator_locals = Paginator(locals, per_page=5)
        pagelocal = request.GET.get('page')
        paginator_locals = paginator_locals.get_page(pagelocal)

        context = {'amount_of_bags': amount_of_bags,
                   'number_of_institution': number_of_institution,
                   'fundations': fundations,
                   'paginator_fundation': paginator_fundation,
                   'paginator_organizations': paginator_organizations,
                   'paginator_locals': paginator_locals,
                   }

        return render(request, 'index.html',
                      context)


def pag_fund_view(request):
    institutions = Institution.objects.all()
    fundations = institutions.filter(type='fundacja')
    page = request.GET.get('page', 1)
    paginator_fundation = Paginator(fundations, per_page=5)
    fundations_page = paginator_fundation.get_page(page)

    fundations_data = [{
        'id': fundation.id,
        'name': fundation.name,
        'description': fundation.description,
        'categories': ', '.join([category.name for category in fundation.categories.all()])
    } for fundation in fundations_page]

    data = {
        'fundations': fundations_data,
        'current_page': fundations_page.number,
        'num_pages': fundations_page.paginator.num_pages,

    }
    return JsonResponse(data)


def pag_org_view(request):
    institutions = Institution.objects.all()
    organizations = institutions.filter(type='organizacja_pozarządowa')
    page = request.GET.get('page', 1)
    paginator_organization = Paginator(organizations, per_page=5)
    organizations_page = paginator_organization.get_page(page)

    organizations_data = [{
        'id': organization.id,
        'name': organization.name,
        'description': organization.description,
        'categories': ", ".join([category.name for category in organization.categories.all()])
    } for organization in organizations_page]

    data = {
        'organizations': organizations_data,
        'current_page': organizations_page.number,
        'num_pages': organizations_page.paginator.num_pages,
    }
    return JsonResponse(data)


def pag_local_view(request):
    institutions = Institution.objects.all()
    locals = institutions.filter(type='zbiórka_lokalna')
    page = request.GET.get('page', 5)
    paginator_local = Paginator(locals, per_page=5)
    locals_page = paginator_local.get_page(page)

    locals_data = [{
        'id': local.id,
        'name': local.name,
        'description': local.description,
        'categories': ", ".join([category.name for category in local.categories.all()])
    } for local in locals_page]

    data = {
        'organizations': locals_data,
        'current_page': locals_page.number,
        'num_pages': locals_page.paginator.num_pages,
    }
    return JsonResponse(data)


class AddDonationView(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()

        context = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'form.html', context)

    def post(self, request):
        if request.method == "POST":
            form = request.POST
            inst = Institution.objects.get(name=form['organization'])
            categories = Category.objects.filter(name__in=form.getlist('categories'))
            date = form['data']
            time = form['time']
            donation = Donation.objects.create(
                quantity=form['bags'],
                address=form['address'],
                city=form['city'],
                phone=form['phone'],
                zipcode=form['postcode'],
                pick_up_date=date,
                pick_up_time=time,
                pick_up_comment=form['more_info'],
                user=request.user,
                institution=inst
            )
            donation.category.set(categories)
            return redirect('confirm')


class ConfirmationView(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'activation_invalid.html')
