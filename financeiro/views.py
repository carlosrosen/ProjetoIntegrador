from wsgiref.util import request_uri

from django.shortcuts import render
from django.http import HttpResponse
from .operacoes import usuario
from .models import Transacao, Categoria
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404

from financeiro.operacoes.usuario import OperacoesTransacao

operacoes = {
    'c': 'criação',
    'e': 'edição',
    'd': 'deletar'
}

def Transacao(request):             #, operacao:str):
    if not User.is_authenticated:
        return redirect(reverse('core:login'))
    operacoes_usuario = OperacoesTransacao(request.user)
    operacoes_usuario.criarTransacao(valor='10.5',data='2025-02-25',tipo='receita',quantidade_parcelas='2',categoria='lazer',descricao='abroba',pago='true')
    return HttpResponse('sla')


'''
    if operacao.lower() not in operacoes.keys():
        raise Http404('operação não encontrada.')
    return HttpResponse(operacoes[operacao])
'''
