from calendar import calendar
from datetime import date

from django.http import HttpResponse, Http404
from django.template.context_processors import request

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

from ..usuarios.models import CustomUser

operacoes = {
    'c': 'criação',
    'e': 'edição',
    'd': 'deletar'
}


def menuExtrato(request, mes: int, ano: int):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))

    if request.method == 'GET':

        OperacoesTransacao(request.user.id).verificarParcelasPagas()

        getter = GetterFinanceiro(request.user.id)

        parcelas = getter.todasParcelasMes(mes, ano)

        categoria_filtro = request.GET.get('categoria')
        tipo_filtro = request.GET.get('tipo')
        pago_filtro = request.GET.get('pago')

        if categoria_filtro:
            parcelas = parcelas.filter(transacao_fk__categoria_fk__nome=categoria_filtro)

        if tipo_filtro:
            parcelas = parcelas.filter(transacao_fk__tipo=tipo_filtro)

        if pago_filtro is not None and pago_filtro != '':
            pago_bool = pago_filtro.lower() in ('true', '1')
            parcelas = parcelas.filter(pago=pago_bool)

        despesa = getter.despesaTotalMes(mes, ano)
        receita = getter.receitaTotalMes(mes, ano)
        saldo_mes = receita - despesa
        categorias = Categoria.objects.all()
        try:
            meses = {
                1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
                5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
                9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
            }
            nome_mes = meses[mes]
        except IndexError:
            nome_mes = "Mês Inválido"


        context = {
            'parcelas': parcelas.order_by('-data'),
            'mes': mes,
            'ano': ano,
            'mes_nome': nome_mes,
            'categorias': categorias,
            'todas_categorias': Categoria.GetTodasCategorias(),
            'despesas_mes': despesa,
            'receitas_mes': receita,
            'saldo_mes': saldo_mes,
            'request': request,
            'hoje': date.today(),
            'todas_categorias_receita': categorias.filter(tipo='R'),
            'todas_categorias_despesa': categorias.filter(tipo='D')
        }
        return render(request, 'extrato.html', context=context)
    return redirect('core:menuExtrato',mes=mes,ano=ano)

def criarTransacaoReceita(request) -> redirect:
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
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
    url = request.POST.get('next') or reverse('core:dashboard')
    return redirect(url)


def criarTransacaoDespesa(request) -> redirect :
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
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
    url = request.POST.get('next') or reverse('core:dashboard')
    return redirect(url)


# Quando a quantidade de parcelas for igual a 1
def editarTransacaoUnica(request, parcela_id):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    if request.method == 'POST':
        parcela = get_object_or_404(ParcelasTransacao, id=parcela_id, transacao_fk__user_fk__id=request.user.id)
        novo_valor = ValorTransacao(request.POST.get('novoValor'))
        nova_data = Data(request.POST.get('novaData'))
        categoria = request.POST.get('novaCategoria')
        pago = Pago(request.POST.get('pago'))
        descricao = request.POST.get('descricao')
        mes = int(parcela.data.month)
        ano = int(parcela.data.year)

        categoria = Categoria.objects.get(nome=categoria)

        operacao = OperacoesTransacao(request.user.id)
        operacao.editarTransacaoUnica(parcela, novo_valor, nova_data, categoria, pago, descricao)
        return redirect('core:menuExtrato', mes=mes, ano=ano)


# Quando a quantidade de parcelas for maior a 1
def editarTransacaoParcelada(request, parcela_id):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    if request.method == 'POST':
        parcela = get_object_or_404(ParcelasTransacao, id=parcela_id, transacao_fk__user_fk__id=request.user.id)
        novo_valor = ValorTransacao(request.POST.get('novoValor'))
        pago = Pago(request.POST.get('pago'))
        descricao = request.POST.get('descricao')
        mes = int(parcela.data.month)
        ano = int(parcela.data.year)

        operacao = OperacoesTransacao(request.user.id)
        operacao.editarTransacaoParcelada(parcela, novo_valor, pago, descricao)
        return redirect('core:menuExtrato', mes=mes, ano=ano)

def deletarParcela(request, parcela_id):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))
    if request.method == 'POST':
        parcela = get_object_or_404(ParcelasTransacao, id=parcela_id, transacao_fk__user_fk__id=request.user.id)
        deletar = request.POST.get('tipoExclusao')
        operacao = OperacoesTransacao(request.user.id)
        mes = int(parcela.data.month)
        ano = int(parcela.data.year)

        if deletar == 'unica':
            operacao.deletarUmaParcela(parcela)
        elif deletar == 'estaprox':
            operacao.deletarProximasParcelas(parcela)
        elif deletar == 'todas':
            operacao.deletarTodasParcelas(parcela)
        return redirect('core:menuExtrato', mes=mes, ano=ano)



