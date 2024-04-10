from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from oddam_app.forms import UserForm
from oddam_app.models import Donation, Institution


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


class LandingPageView(View):
    def get(self, request):
        amount_of_bags = sum([item.quantity for item in Donation.objects.all()])
        number_of_institution = Institution.objects.all().count()

        institutions = Institution.objects.all()
        fundations = institutions.filter(type='fundacja')
        organizations = institutions.filter(type='organizacja_pozarządowa')
        locals = institutions.filter(type='zbiórka_lokalna')

        fundations_paginator = Paginator(fundations, 5)
        fundations_page_number = request.GET.get('page')
        fundation_page_obj = fundations_paginator.get_page(fundations_page_number)

        context = {'amount_of_bags': amount_of_bags,
                   'number_of_institution': number_of_institution,
                   'fundations': fundations,
                   'organizations': organizations,
                   'locals': locals,
                   'fundation_page_obj': fundation_page_obj,

                   }
        return render(request, 'index.html',
                      context)


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')