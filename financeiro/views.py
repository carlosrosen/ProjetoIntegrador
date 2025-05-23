from pydoc import describe
from wsgiref.util import request_uri

from django.shortcuts import render
from django.http import HttpResponse

from usuarios.views import deslogar
from .dominio.valortransacao import Valor
from .operacoes import usuario
from .models import Transacao, Categoria
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404


#classes de logica
from financeiro.operacoes.usuario import OperacoesTransacao
from financeiro.operacoes.historicoSaldo import HistoricoSaldo
from financeiro.models import ParcelasTransacao

from financeiro.dominio.valortransacao import Valor
from financeiro.dominio.tipo import Tipo
from financeiro.dominio.data import Data
from financeiro.dominio.quantidadeparcelas import QuantidadeParcelas
from financeiro.dominio.pago import Pago


operacoes = {
    'c': 'criação',
    'e': 'edição',
    'd': 'deletar'
}

def CriarTransacao(request):             #, operacao:str):
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))
    operacoes_usuario = OperacoesTransacao(request.user)

    valor = Valor('100.0')
    data = Data('2025-01-30')
    tipo = Tipo('receita')
    quantidade_parcelas = QuantidadeParcelas('4')
    Categoria.verificacaoNomesCategoria('salario')
    categoria = Categoria.objects.get(nome='salario')
    descricao = 'abroba'
    pago = Pago('true')

    operacoes_usuario.criar(valor=valor
                            , data=data
                            , tipo=tipo
                            , quantidade_parcelas=quantidade_parcelas
                            , categoria_objeto=categoria
                            , descricao=descricao
                            , pago=pago
    )

    return HttpResponse('criou')

def EditarTransacao(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))
    operacoes_usuario = OperacoesTransacao(request.user)
    parcela = ParcelasTransacao.objects.filter(id=1)
    valor = Valor('25.0')
    data = Data('2025-06-30')

    Categoria.verificacaoNomesCategoria('salario')
    categoria = Categoria.objects.get(nome='salario')

    descricao = 'abroba2'
    pago = Pago('true')

    operacoes_usuario.editarUmaParcela(parcela_id= 6
                                     , valor= valor
                                     , data= data
                                     , categoria= categoria
                                     , pago= pago
                                     , descricao= descricao
    )

    return HttpResponse('editou')

def deletarUmaParcela(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))
    operacoes_usuario = OperacoesTransacao(request.user)
    try:
        parcela = ParcelasTransacao.objects.get(id=2)
    except:
        raise IndexError('Parcela Inexistente')

    operacoes_usuario.deletarUmaParcela(parcela)

    return HttpResponse('deletou')



def deletarTodasParcelas(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))
    operacoes_usuario = OperacoesTransacao(request.user)
    try:
        parcela = ParcelasTransacao.objects.get(id=5)
    except Exception as e:
        raise IndexError('Parcela Inexistente')

    transacao = parcela.transacao_fk
    operacoes_usuario.deletarTodasParcelas(transacao=transacao)

    return HttpResponse('deletou tudo')


def teste(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))
    operacoes_historico_saldo = HistoricoSaldo(request.user)
    pass
