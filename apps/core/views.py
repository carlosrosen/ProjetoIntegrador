import re

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from apps.financeiro.models import Categoria
from apps.financeiro.operacoes.getter import GetterFinanceiro
from apps.financeiro.operacoes.saldo import Historico
from apps.financeiro.operacoes.transacao import OperacoesTransacao
from apps.objetivos.models import Objetivos
from apps.metas.models import Metas
from common.dominio.data import Data

from datetime import date
from decimal import Decimal

from apps.financeiro.views import criarTransacaoReceita, criarTransacaoDespesa
from apps.metas.views import criarMeta
from apps.objetivos.views import criarObjetivo

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    if request.method == "GET":
        historico = Historico(request.user.id)
        transacoes = OperacoesTransacao(request.user.id)
        historico.verificarInsercoesHistorico()
        infos_financeiro = GetterFinanceiro(request.user.id)

        saldo_atual = infos_financeiro.saldoAtual()
        hoje = date.today()

        ganhos_mes = infos_financeiro.receitaTotalMes(hoje.month, hoje.year)
        gastos_mes = infos_financeiro.despesaTotalMes(hoje.month, hoje.year)

        dicionario_despesas_categorias = infos_financeiro.valorTotalDasCategorias(hoje.month, hoje.year, 'despesa')
        dicionario_receitas_categorias = infos_financeiro.valorTotalDasCategorias(hoje.month, hoje.year, 'receita')

        categorias = Categoria.objects.all()

        objetivo_prox = Objetivos.objects.order_by('valor_guardado').first()
        meta_prox = Metas.objects.order_by('data_fim').first()

        informacoes_dashboard = {'saldo_atual': saldo_atual
                               , 'username': request.user.username
                               , 'ganhos_mes': ganhos_mes
                               , 'gastos_mes': gastos_mes
                               , 'balanco_mes': ganhos_mes - gastos_mes
                               , 'mes_ano': Data.formatarMesAno(hoje.month, hoje.year)
                               , 'lancamentos_futuros': infos_financeiro.proximasTresParcelas()
                               , 'ultimos_lancamentos': infos_financeiro.ultimaCincoParcelas()
                               , 'categorias': categorias
                               , 'todas_categorias_receita': categorias.filter(tipo='R')
                               , 'todas_categorias_despesa': categorias.filter(tipo='D')
                               , 'lista_receitas_categoria': ','.join(dicionario_receitas_categorias.values())
                               , 'categorias_transacoes_receitas': ','.join(dicionario_receitas_categorias.keys())
                               , 'lista_despesas_categoria': ','.join(dicionario_despesas_categorias.values())
                               , 'categorias_transacoes_despesas': ','.join(dicionario_despesas_categorias.keys())
                               , 'mes': hoje.month
                               , 'ano': hoje.year
                               , 'meta': meta_prox
                               , 'objetivo': objetivo_prox
        }
        return render(request, 'dashboard.html', informacoes_dashboard)
    return redirect(reverse('core:dashboard'))





def notfound(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    return render(request, 'erro/404.html')

def erro(request, mensagem):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    return render(request, 'erro/erroinesperado.html', {'mensagem': mensagem})