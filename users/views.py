from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.http import Http404
from .forms import RegisterForm, LoginForm, ProfileUpdateForm

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form') or ProfileUpdateForm(instance=self.request.user)
        context['active_field'] = kwargs.get('active_field', '')  # Указывает какая форма была активна
        context['has_error'] = kwargs.get('has_error', False)
        return context

    def post(self, request, *args, **kwargs):
        form_type = request.POST.get('form_type')

        # Частичные данные
        field_mapping = {
            'username': {'username': request.POST.get('username')},
            'email': {'email': request.POST.get('email')},
            'bio': {'bio': request.POST.get('bio')},
            'avatar': request.POST
        }

        data = field_mapping.get(form_type, {})
        files = request.FILES if form_type == 'avatar' else None

        form = ProfileUpdateForm(data, files, instance=request.user)

        # Удаляем поля, не относящиеся к этой форме
        for field_name in list(form.fields.keys()):
            if field_name not in data and field_name not in (files or {}):
                form.fields.pop(field_name)

        if form.is_valid():
            form.save()
            return redirect('profile')

        # Если ошибка — не показывать форму, только toast и возврат к display
        context = self.get_context_data(
            form=ProfileUpdateForm(instance=request.user),
            has_error=True,
            active_field=''  # Сбрасываем активную форму
        )
        context['form'].errors.update(form.errors)
        return self.render_to_response(context)


class PublicProfileView(TemplateView):
    template_name = 'users/public_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')

        try:
            profile_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("Такой пользователь не найден")

        if self.request.user.is_authenticated and self.request.user == profile_user:
            return redirect('profile')

        context['profile_user'] = profile_user
        context['is_self'] = self.request.user == profile_user
        return context
