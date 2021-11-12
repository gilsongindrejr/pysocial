from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

from .forms import UserCreationForm


class RegisterUserView(CreateView):
    template_name = 'users/register.html'
    model = get_user_model()
    # Still has to implement success url
    success_url = reverse_lazy('url_name')
    form_class = UserCreationForm


class LoginView(LoginView):
    template_name = 'users/login.html'


class LogoutView(LogoutView):
    template_name = 'users/logout.html'


class PasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'