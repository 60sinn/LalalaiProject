from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from django.contrib.auth import get_user_model
User = get_user_model()

from django.http import Http404
from .forms import RegisterForm, LoginForm, ProfileUpdateForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # потом заменим на нужный маршрут
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
        return context

    def post(self, request, *args, **kwargs):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return self.render_to_response(self.get_context_data(form=ProfileUpdateForm(instance=request.user), success=True))
        return self.render_to_response(self.get_context_data(form=form))


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
