from django import forms
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from .models import User


# Форма для логина
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'placeholder': 'Введите ваш username'
    }), required=True)

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'placeholder': 'Введите пароль'
    }), required=True)

    class Meta:
        model = User
        fields = ('username','password',)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     if not cleaned_data.get("username") and not cleaned_data.get("password"):
    #         messages.error(self.request, "Оба поля должны быть заполнены")


#  Форма для регистрации
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'username',
        'placeholder': 'Введите ваш username'
    }), required=True)

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'email',
        'placeholder': 'Введите ваш email'
    }), required=True)

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'placeholder': 'Придумайте пароль'
    }), required=True)

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'placeholder': 'Повторите пароль'
    }), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# Форма для восстановления
class UserPasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'email',
        'placeholder': 'Введите ваш email'
    }), required=True)


# Стилизация формы восстановления пароля
class StyledSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs.update({
            'id': 'password',
            'placeholder': 'Введите новый пароль'
        })

        self.fields["new_password2"].widget.attrs.update({
            'id': 'password',
            'placeholder': 'Повторите новый пароль'
        })
