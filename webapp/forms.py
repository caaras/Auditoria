from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(required=True)
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'password1', 'password2')


class EmailForm(forms.Form):
    email = forms.EmailField()


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

