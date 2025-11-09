from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'placeholder': 'Введите ваш username'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('username','password',)