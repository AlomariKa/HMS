# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout # These functions are used for handling user authentication, logging users in and out.
from django.contrib import messages # This module is used to display messages to users.
from .forms import UserRegisterForm
from django.urls import reverse

def home(request):
    return render(request, 'accounts/home.html')


# User Authentication #
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type') # Retrieves the user_type from the form.
            user.userprofile.user_type = user_type # Sets the user_type in the user profile.
            user.userprofile.save() # It helps create a more secure and user-friendly application.
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, 'Registration successful.')
            return redirect('accounts:login')  # Redirect to a home page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_type = user.userprofile.user_type
            if user_type == 'patient':
                return redirect(reverse('logic:patient_profile'))
            elif user_type == 'admin':
                return redirect(reverse('logic:admin_profile'))
            elif user_type == 'provider':
                return redirect(reverse('logic:provider_profile'))
            messages.success(request, 'Login successful.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')  # Redirect to login page