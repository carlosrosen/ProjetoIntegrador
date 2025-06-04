from django.http import HttpResponse, Http404

from common.dominio.data import Data
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

def criarTransacaoReceita(request) -> redirect:
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))
    if not request.method == 'POST':
        return None
    try:
        valor = ValorTransacao(request.POST.get('valor_receita'))
        data = Data(request.POST.get('data_receita'))
        descricao = request.POST.get('descricao_receita').strip()
        categoria = request.POST.get('categoria_receita').strip()
        pago = Pago(request.POST.get('pagamentoRE_receita'))
        tipo = Tipo('receita')
        quantidade_parcelas = QuantidadeParcelas(1)
        Categoria.verificacaoNomesCategoria(categoria)
        categoria = Categoria.objects.get(nome=categoria)
    except Exception as e:
        return redirect(reverse('core:erro', args=[str(e)]))

    transacoes_usuario = OperacoesTransacao(request.user.id)
    try:
        transacoes_usuario.criar(valor,data,tipo,quantidade_parcelas,descricao,pago,categoria)
    except Exception as e:
        return redirect(reverse('core:erro', args=[str(e)]))
    return None


def criarTransacaoDespesa(request) -> redirect :
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))
    if not request.method == 'POST':
        return None
    try:
        valor = ValorTransacao(request.POST.get('valor_despesa'))
        data = Data(request.POST.get('data_despesa'))
        descricao = request.POST.get('descricao_despesa').strip()
        categoria = request.POST.get('categoria_despesa').strip()
        pago = Pago(request.POST.get('pagamentoRE_despesa'))
        tipo = Tipo('despesa')
        quantidade_parcelas = QuantidadeParcelas(request.POST.get('parcelas_despesa'))
    except Exception as e:
        return redirect(reverse('core:erro', args=[str(e)]))
    try:
        Categoria.verificacaoNomesCategoria(categoria)
        categoria = Categoria.objects.get(nome=categoria)
    except Exception:
        return redirect(reverse('core:erro', args=['Falha ao localizar a categoria']))

    transacoes_usuario = OperacoesTransacao(request.user.id)
    try:
        transacoes_usuario.criar(valor, data, tipo, quantidade_parcelas, descricao, pago, categoria)
    except Exception as e:
        return redirect(reverse('core:erro', args=[str(e)]))
    return None


