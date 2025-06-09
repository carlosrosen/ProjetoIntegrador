from django.http import HttpResponse, Http404

from common.dominio.data import Data
from .models import Categoria
from django.shortcuts import render, reverse, redirect, get_object_or_404

#classes de logica
from apps.financeiro.operacoes.transacao import OperacoesTransacao
from apps.financeiro.operacoes.getter import GetterFinanceiro
from apps.financeiro.operacoes.saldo import Historico
from apps.financeiro.models import ParcelasTransacao
from apps.financeiro.dominio import *

from apps.financeiro.models import ParcelasTransacao
from decimal import Decimal



operacoes = {
    'c': 'criação',
    'e': 'edição',
    'd': 'deletar'
}
def menuExtrato(request, mes:int, ano:int):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    if request.method == 'GET':

        getter = GetterFinanceiro(request.user.id)
        parcelas = getter.todasParcelasMes(mes, ano)
        categorias = Categoria.objects.all()
        despesa = getter.despesaTotalMes(mes,ano)
        receita = getter.receitaTotalMes(mes,ano)
        saldo_mes = receita - despesa
        context = {
            'parcelas': parcelas,
            'mes': mes,
            'ano': ano,
            'categorias': categorias,
            'despesas_mes': despesa,
            'receitas_mes': receita,
            'saldo_mes': saldo_mes,
        }
        print(request.session.get('ultima_url'))
        return render(request, 'extrato.html', context=context)
    return redirect(request.session.get('ultima_url'))

def criarTransacaoReceita(request) -> redirect:
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))
    if not request.method == 'POST':
        return redirect(reverse('core:dashboard'))

    for valores_post in request.POST:
        if valores_post == '':
            return redirect(reverse('core:erro', args=['Valores não recebidos']))
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

    return redirect(request.session.get('ultima_url'))


def criarTransacaoDespesa(request) -> redirect :
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))
    if not request.method == 'POST':
        return redirect(reverse('core:dashboard'))
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

    return redirect(request.session.get('ultima_url'))


# Quando a quantidade de parcelas for igual a 1
def editarTransacaoUnica(request, parcela_id):
    if request.method == 'POST':
        parcela = get_object_or_404(ParcelasTransacao, id=parcela_id, transacao_fk__user_fk__id=request.user.id)
        novo_valor = ValorTransacao(request.POST.get('novoValor'))
        nova_data = Data(request.POST.get('novaData'))
        categoria = request.POST.get('novaCategoria')
        pago = Pago(request.POST.get('pago'))
        descricao = request.POST.get('descricao')

        categoria = Categoria.objects.get(nome=categoria)

        operacao = OperacoesTransacao(request.user.id)
        operacao.editarTransacaoUnica(parcela, novo_valor, nova_data, categoria, pago, descricao)

    return redirect(reverse('core:extrato:menuExtrato'))

# Quando a quantidade de parcelas for maior a 1
def editarTransacaoParcelada(request, parcela_id):
    if request.method == 'POST':
        parcela = get_object_or_404(ParcelasTransacao, id=parcela_id, transacao_fk__user_fk__id=request.user.id)
        novo_valor = ValorTransacao(request.POST.get('novoValor'))
        pago = Pago(request.POST.get('pago'))
        descricao = request.POST.get('descricao')

        operacao = OperacoesTransacao(request.user.id)
        operacao.editarTransacaoParcelada(parcela, novo_valor, pago, descricao)

    return redirect(reverse('core:extrato:menuExtrato'))

def deletarParcela(request, parcela_id):
    if not request.user.is_authenticated:
        return redirect(reverse('core:login'))
    if request.method == 'POST':
        parcela = get_object_or_404(ParcelasTransacao, id=parcela_id, transacao_fk__user_fk__id=request.user.id)
        deletar = request.POST.get('tipoExclusao')
        operacao = OperacoesTransacao(request.user.id)

        if deletar == 'apenas':
            operacao.deletarUmaParcela(parcela)
        elif deletar == 'estaprox':
            operacao.deletarProximasParcelas(parcela)
        elif deletar == 'todas':
            operacao.deletarTodasParcelas(parcela)

    return redirect(reverse('core:extrato:menuExtrato'))



