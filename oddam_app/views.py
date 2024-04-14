from datetime import datetime, time
from time import mktime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from oddam_app.forms import UserForm
from oddam_app.models import Donation, Institution, Category


# Create your views here.


class RegisterView(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name,
                                            last_name=last_name)
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
                exisitng_user = User.objects.get(username=username)
                messages.error(request, 'Niepoprawne hasło')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Nie ma takiego użytkownika')
                return redirect('register')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class LandingPageView(View):
    def get(self, request):
        amount_of_bags = sum([item.quantity for item in Donation.objects.all()])
        number_of_institution = Institution.objects.all().count()

        institutions = Institution.objects.all()
        fundations = institutions.filter(type='fundacja')
        # organizations = institutions.filter(type='organizacja_pozarządowa')
        # locals = institutions.filter(type='zbiórka_lokalna')

        fundations_paginator = Paginator(fundations, 5)
        fundations_page_number = request.GET.get('page')
        fundation_page_obj = fundations_paginator.get_page(fundations_page_number)

        context = {'amount_of_bags': amount_of_bags,
                   'number_of_institution': number_of_institution,
                   # 'fundations': fundations,
                   # 'organizations': organizations,
                   # 'locals': locals,
                   'fundation_page_obj': fundation_page_obj,

                   }
        return render(request, 'index.html',
                      context)


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
