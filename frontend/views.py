from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard after login
            else:
                # Handle invalid login
                return render(request, 'frontend/login.html', {'form': form, 'error': 'Invalid credentials'})
        else:
            return render(request, 'frontend/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'frontend/login.html', {'form': form})


#@login_required
def dashboard_view(request):
     return render(request, 'frontend/patient_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')