from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('profile')
            except IntegrityError:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe.'
                })
        return render(request, 'singup.html', {
            'form': UserCreationForm,
            'error': 'Contraseñas no coinciden.'
        })


def profile(request):
    return render(request, 'profile.html')


def singout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'singin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'singin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta.'
            })
        else:
            login(request, user)
            return redirect('home')
