"""
URL configuration for Oddam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from oddam_app import views

urlpatterns = [
    path('admin/', admin.site.urls, ),
    path('', views.LandingPageView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user/', views.UserSiteView.as_view(), name='user'),
    path('user_edit/', views.UserEditView.as_view(), name='user_edit'),
    path('adddonation/', views.AddDonationView.as_view(), name="adddonation"),
    path('confirm/', views.ConfirmationView.as_view(), name="confirm"),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('api/datafund/', views.pag_fund_view),
    path('api/dataorg/', views.pag_org_view),
    path('api/datalocal/', views.pag_org_view),
    path('api/contact/', views.ContactView.as_view(), name='contact'),
    path('passwordrecovery', views.PasswordRecovery.as_view(), name='recovery'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
