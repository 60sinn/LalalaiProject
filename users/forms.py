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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username != self.instance.username:
            validate_username_change(self.instance)
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != self.instance.email:
            validate_email_change(self.instance)
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        now = timezone.now()

        # ВАЖНО: сравниваем с self.instance._loaded_values
        original_username = self.initial.get('username')
        original_email = self.initial.get('email')

        if original_username and self.cleaned_data.get('username') != original_username:
            user.last_username_change = now

        if original_email and self.cleaned_data.get('email') != original_email:
            user.last_email_change = now

        if commit:
            user.save()
        return user