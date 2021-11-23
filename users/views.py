from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .forms import UserCreationForm, UserChangeForm


class RegisterUserView(CreateView):
    template_name = 'users/register.html'
    model = get_user_model()
    # Still has to implement success url
    success_url = reverse_lazy('url_name')
    form_class = UserCreationForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'


class UpdateProfileView(LoginRequiredMixin, View):

    def get(self, request):
        form = UserChangeForm(instance=request.user)
        context = {'form': form}
        return render(request, 'users/update_profile.html', context)

    def post(self, request):
        form = UserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return render(request, 'users/profile.html')


class LoginView(LoginView):
    template_name = 'users/login.html'


class LogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
