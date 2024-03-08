from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SignupForm

def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'all_recipes'))

        else:
            error_message = 'There was an error.'

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('logout_success')

def logout_success(request):
    logout(request)
    return render(request, 'auth/success.html')

def error_403(request, exception):
    return render(request, 'error/403.html', status=403)

