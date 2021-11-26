from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class UserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'email', 'first_name', 'last_name', 'image')


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'image')


class FriendForm(forms.Form):
    friend = forms.CharField(max_length=100, required=False)
