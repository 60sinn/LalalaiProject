from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from .models import CustomUser
from .validators import validate_username_change, validate_email_change


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar', 'bio']
        labels = {
            'username': 'Ник',
            'email': 'Почта',
            'avatar': 'Аватар',
            'bio': 'Описание профиля'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # По умолчанию отключаем обязательность
        self.fields['username'].required = False
        self.fields['email'].required = False

        # Делаем обязательными, если они реально присутствуют в POST
        data = args[0] if args else {}
        if 'username' in data:
            self.fields['username'].required = True
        if 'email' in data:
            self.fields['email'].required = True

    def clean_username(self):
        if 'username' not in self.cleaned_data:
            return self.instance.username
        username = self.cleaned_data.get('username')
        if username != self.instance.username:
            validate_username_change(self.instance)
        return username

    def clean_email(self):
        if 'email' not in self.cleaned_data:
            return self.instance.email
        email = self.cleaned_data.get('email')
        if email != self.instance.email:
            validate_email_change(self.instance)
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        now = timezone.now()

        original_username = self.initial.get('username')
        original_email = self.initial.get('email')

        if 'username' in self.cleaned_data and self.cleaned_data.get('username') != original_username:
            user.last_username_change = now

        if 'email' in self.cleaned_data and self.cleaned_data.get('email') != original_email:
            user.last_email_change = now

        if commit:
            user.save()
        return user
