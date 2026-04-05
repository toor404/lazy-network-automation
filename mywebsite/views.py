from urllib import response
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import requests


def RegistrationPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:

        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')


        context = {
                'title':'Lazy Network Automation',
                'page': 'Registration',
                'form': form,
            }
        return render(request, 'register.html', context)

def LoginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                print("butut")
        
        context = {
                'title':'Lazy Network Automation',
                'page': 'Login',
            
            }
        return render(request, 'login.html', context)

@login_required(login_url='login')
def LogoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    context = {
        'title':'Netter',
        'heading':'Selamat Datang',
        'subheading':'Di Lazy Flair',
        'page': 'Home',
    }
    
    
    return render(request, 'index.html', context)

