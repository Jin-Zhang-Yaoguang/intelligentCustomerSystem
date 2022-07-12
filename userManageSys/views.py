from django.http import HttpResponse
from django.shortcuts import render,redirect
from . import forms


def index(request):
    return render(request, 'userManagerSys/index.html')


def login(request):
    return render(request, 'userManagerSys/login.html')


def register(request):
    return render(request, 'userManagerSys/register.html', {'form': forms})


def edit(request):
    return render(request, 'userManagerSys/edit.html')


def find(request):
    pass

