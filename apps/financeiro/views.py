from django.http import HttpResponse

from .models import Categoria
from django.shortcuts import redirect
from django.urls import reverse

#classes de logica
from apps.financeiro.operacoes.transacao import OperacoesTransacao
from apps.financeiro.operacoes.saldo import Historico
from apps.financeiro.models import ParcelasTransacao

from apps.financeiro.dominio import *

operacoes = {
    'c': 'criação',
    'e': 'edição',
    'd': 'deletar'
}

def CriarTransacao(request):             #, operacao:str):
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))

    print(request.method)

#    operacoes_usuario = OperacoesTransacao(request.user)
    return HttpResponse('criou')

