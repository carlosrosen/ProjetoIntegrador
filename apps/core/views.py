from django.shortcuts import render, redirect
from django.urls import reverse

from apps.financeiro.operacoes.saldo import Historico

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    historico = Historico(request.user)
    historico.verificarInsercoesHistorico()

    return render(request, 'dashboard.html')

def notfound(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    return render(request, 'erro/404.html')