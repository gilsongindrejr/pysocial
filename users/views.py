from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import UserCreationForm


class RegisterUserView(CreateView):
    template_name = 'path/to/template'
    model = get_user_model()
    success_url = reverse_lazy('url_name')
    form_class = UserCreationForm
