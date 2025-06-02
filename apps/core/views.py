from django.shortcuts import render, redirect
from django.urls import reverse
from apps.financeiro.operacoes.getter import GetterFinanceiro
from apps.usuarios.models import CustomUser
from apps.financeiro.operacoes.saldo import Historico
from apps.financeiro.operacoes.transacao import OperacoesTransacao
from common.dominio.data import Data

from datetime import date
from decimal import Decimal

import json
from django.core.serializers.json import DjangoJSONEncoder

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

        ganhos_mes = Decimal(infos_financeiro.receitaTotalMes(hoje.month, hoje.year))
        gastos_mes = Decimal(infos_financeiro.despesaTotalMes(hoje.month, hoje.year))

        dicionario_despesas_categorias = infos_financeiro.valorTotalDasCategorias(hoje.month, hoje.year, 'despesa')
        dicionario_receitas_categorias = infos_financeiro.valorTotalDasCategorias(hoje.month, hoje.year, 'receita')

        informacoes_dashboard = {'saldo_atual': saldo_atual
                               , 'username': request.user.username
                               , 'ganhos_mes': ganhos_mes
                               , 'gastos_mes': gastos_mes
                               , 'balanco_mes': ganhos_mes - gastos_mes
                               , 'mes_ano': Data.formatarMesAno(hoje.month, hoje.year)
                               , 'lancamentos_futuros': infos_financeiro.proximasTresParcelas()
                               , 'ultimos_lancamentos': infos_financeiro.ultimaCincoParcelas()
                               , 'lista_receitas_categoria': ','.join(dicionario_receitas_categorias.values())
                               , 'lista_categorias_receitas': ','.join(dicionario_receitas_categorias.keys())
                               , 'lista_despesas_categoria': ','.join(dicionario_despesas_categorias.values())
                               , 'lista_categorias_despesa': ','.join(dicionario_despesas_categorias.keys())
        }

        return render(request, 'dashboard.html', informacoes_dashboard)
    #if request.method != 'GET':

    form = request.GET.get('tipoform')
    print(form)




def notfound(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    return render(request, 'erro/404.html')