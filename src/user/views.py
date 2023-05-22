from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout

from .forms import UserRegisterForm
from .forms import UserLoginForm


def register_user(request):
    # handler if user simply open register page
    if not request.method == 'POST':
        form = UserRegisterForm()
        return render(request, 'user/register.html', {'form': form})

    # handler if user sent data for register
    form = UserRegisterForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Registration error')
        return render(request, 'user/register.html', {'form': form})

    # handler if sended from user data is valid
    form.save()
    messages.success(request, 'User registration successful')
    return redirect('login_user')


def login_user(request):
    if not request.method == 'POST':
        form = UserLoginForm()
        return render(request, 'user/login.html', {'form': form})

    form = UserLoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'{user.username} successfully logged in.')
        return redirect('index')

    return render(request, 'user/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('login_user')
