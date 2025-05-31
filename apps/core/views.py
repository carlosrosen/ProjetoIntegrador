from django.shortcuts import render, redirect
from django.urls import reverse
from apps.financeiro.operacoes.transacao import Transacao
from apps.financeiro.operacoes.transacao import OperacoesTransacao
from apps.usuarios.models import CustomUser

from apps.financeiro.operacoes.saldo import Historico
from apps.financeiro.operacoes.transacao import OperacoesTransacao
from common.dominio.data import Data

from datetime import date
from decimal import Decimal

import json

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    historico = Historico(request.user.id)
    transacoes = OperacoesTransacao(request.user.id)
    historico.verificarInsercoesHistorico()

    saldo_atual = historico.pegarSaldoAtual()
    hoje = date.today()

    ganhos_mes = Decimal(historico.pegarGanhosMes(hoje.month, hoje.year))
    gastos_mes = Decimal(historico.pegarGastosMes(hoje.month, hoje.year))

    dicionario_despesas_categorias = historico.pegarValorCategorias(hoje.month, hoje.year, 'despesa')
    dicionario_receitas_categorias = historico.pegarValorCategorias(hoje.month, hoje.year, 'receita')

    return render(request, 'dashboard.html'
                  , {'saldo_atual': saldo_atual
                            , 'username': request.user.username
                            , 'ganhos_mes': historico.pegarGanhosMes(hoje.month, hoje.year)
                            , 'gastos_mes': historico.pegarGastosMes(hoje.month, hoje.year)
                            , 'balanco_mes': ganhos_mes - gastos_mes
                            , 'mes_ano': Data.formatarMesAno(hoje.month, hoje.year)
                            , 'lancamentos_futuros': transacoes.proximasTresParcelas()
                            , 'ultimos_lancamentos': transacoes.ultimaCincoParcelas()
                            , 'lista_receitas_categoria': dicionario_receitas_categorias.values()
                            , 'lista_categorias_receitas': dicionario_receitas_categorias.keys()
                            , 'lista_despesas_categoria': dicionario_despesas_categorias.values()
                            , 'lista_categorias_despesa': dicionario_receitas_categorias.keys()
                            }
                  )

def notfound(request):
    if not request.user.is_authenticated:
        return redirect(reverse('core:index'))
    return render(request, 'erro/404.html')