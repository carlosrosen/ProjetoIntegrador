from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    
    return render(request, 'dashboard.html')

def manutencao(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    
    return render(request, 'manutencao.html')