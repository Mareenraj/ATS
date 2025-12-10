"""
Views for user authentication.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RecruiterRegistrationForm, RecruiterLoginForm


class RecruiterLoginView(LoginView):
    """Custom login view for recruiters."""
    form_class = RecruiterLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('jobs:dashboard')


def register_view(request):
    """View for recruiter registration."""
    if request.user.is_authenticated:
        return redirect('jobs:dashboard')

    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to ATS.')
            return redirect('jobs:dashboard')
    else:
        form = RecruiterRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """View for user logout."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('jobs:job_list')