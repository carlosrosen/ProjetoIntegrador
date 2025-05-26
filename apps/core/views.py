from django.shortcuts import render, redirect
from django.urls import reverse

from apps.financeiro.operacoes.saldo import Historico

def index(request):
    return render(request, 'templates/index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    Historico(request.user)
    Historico.verificarInsercoesHistorico(request.user)

    return render(request, 'templates/dashboard.html')

def notfound(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    return render(request, 'templates/404.html')