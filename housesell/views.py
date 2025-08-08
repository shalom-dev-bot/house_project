from django.shortcuts import render
from .models import Listing
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def index(request):
    return render(request, 'index.html')


def listings(request):
    houses = Listing.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'listings.html', {'houses': houses})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('forum_home')  # redirige si déjà connecté

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('forum_home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('forum_home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion directe après inscription
            return redirect('forum_home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def about_view(request):
    return render(request, 'about.html')
