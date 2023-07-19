from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, UserForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib.auth import logout
@login_required
def user_profile(request):
    if request.method == 'POST':
        print("LOGIN POST INIT")
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'user_profile.html', {'user_form': user_form, 'profile_form': profile_form})

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def register(request):
    print("REGISTER INIT")
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        print("POST INIT")
        if form.is_valid():
            print("USER REGISTERED")
            form.save()
            return redirect('login.html')  # Change 'login' to the appropriate URL name for your login view
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Replace 'home' with the appropriate URL name for your home page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('index/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')
