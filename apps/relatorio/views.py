from datetime import date
import datetime
import calendar

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.utils import timezone

from decimal import Decimal

from apps.financeiro.models import Categoria, Transacao, ParcelasTransacao, HistoricoSaldo
from apps.financeiro.operacoes.getter import GetterFinanceiro

from apps.metas.models import Metas

from apps.objetivos.dominio.pausar import Pausar
from apps.objetivos.dominio.tipoobjetivo import TipoObjetivo
from apps.objetivos.dominio.valorobjetivo import ValorObjetivo
from apps.objetivos.models import Objetivos
from apps.objetivos.operacoes.objetivos import GetObjetivo, OperacoesObjetivo
from apps.usuarios.models import CustomUser

from common.dominio.data import Data

def relatorioMensal(request):
    if not request.user.is_authenticated:
        return redirect(reverse('usuario:login'))

    mes = date.today().month
    ano = date.today().year

    primeiro_dia = Data.primeiroDiaMes(mes,ano)
    ultimo_dia = Data.ultimoDiaMes(mes, ano)

    user = CustomUser.objects.get(id=request.user.id)
    getter = GetterFinanceiro(request.user.id)
    categorias = Categoria.objects.all()

    # Total

    saldo_atual = user.saldoAtual
    receita_total = getter.receitaTotalMes(mes, ano)
    despesa_total = getter.despesaTotalMes(mes, ano)

    # Resumo geral
    proximo_mes = Data.incrementarMes(primeiro_dia)
    saldo_inicio = HistoricoSaldo.getSaldoInicioMes(user, mes, ano)
    saldo_final = HistoricoSaldo.getSaldoInicioMes(user, proximo_mes.valor.month, proximo_mes.valor.year)
    # Ganho/Lucro

    transacoes_mes = ParcelasTransacao.objects.filter(transacao_fk__user_fk=user, data__range=(primeiro_dia, ultimo_dia))
    transacoes_totaisMes = transacoes_mes.count()  # Quantidade de transacoes no total no mes
    transacoes_receitasMes = transacoes_mes.filter(transacao_fk__tipo="R").count() # Quantidade de transacoes de receitas no mes
    transcacoes_despesasMes = transacoes_mes.filter(transacao_fk__tipo="D").count() # Quantidade de transacoes de despesas no mes

    # Metas
    todas_metas = Metas.objects.filter(user_fk=user)

    total_quantidade_metas = todas_metas.count() # Quantidade total de metas criadas
    metas_ativas = todas_metas.filter(tipo="A").count() # Quantidade total de metas ativas

    metas_intervalo = todas_metas.filter(data_conclusao__range=(primeiro_dia, ultimo_dia))

    metas_concluidas, metas_utrapassadas, metas_naoatingidas  = metas_intervalo.filter(tipo="C").count(), metas_intervalo.filter(tipo="U").count(), metas_intervalo.filter(tipo="N").count()

    # Objetivos

    objetivos = Objetivos.objects.filter(user_fk=user)

    total_objetivos = objetivos.count() # Quantidade total de objetivos criados
    objetivos_ativosTotal = objetivos.filter(status="A").count() # Quantidade total de objetivos ativos
    objetivos_pausadosTotal = objetivos.filter(status="P").count() # Quantidade total de objetivos pausados

    objetivos_concluidos = objetivos.filter(status="C")

    objetivos_concluidosTotal = objetivos_concluidos.count() # Quantidade total de objetivos concluidos
    objetivos_criadosMes = objetivos.filter(data_conclusao__range=(primeiro_dia, ultimo_dia)).count() # Quantidade de objetivos criados no mês
    objetivos_concluidosMes = objetivos_concluidos.filter(data_conclusao__range=(primeiro_dia, ultimo_dia)).count() # Quantidade de objetivos concluidos no mês

    # total economizado


    #Analise detalhada do mês

    getter_financeiro = GetterFinanceiro(request.user.id)
    maximos_receita, minimos_receita = getter_financeiro.MaiorEMenorValoresDasCategoriasDoMes(mes, ano,'receita')
    maximos_despesa, minimos_despesa = getter_financeiro.MaiorEMenorValoresDasCategoriasDoMes(mes,ano,'despesa')
    maior_categoria_receita = maximos_receita[0]
    valor_maior_categoria_receita = maximos_receita[1]

    menor_categoria_receita = minimos_receita[0]
    valor_menor_categoria_receita = minimos_receita[1]

    maior_categoria_despesa = maximos_despesa[0]
    valor_maior_categoria_despesa = maximos_despesa[1]

    menor_categoria_despesa = minimos_despesa[0]
    valor_menor_categoria_despesa = minimos_despesa[1]

    #Frequencia de transacoes
    frequencia_transacoes = getter_financeiro.mediaTransacoesMes(mes,ano)


    # Gráfico da váriação do saldo do mês
    valores_historico, dias_historico = getter.historicoSaldoMes(mes, ano)


    # Grafico de fluxo de caixa do mês

    # Gráfico de categorias

    # Gastos por dia da semana

    context = {
        # Dados básicos
        'mes': mes,
        'ano': ano,

        # Saldo e resumo financeiro
        'saldo_atual': saldo_atual,
        'saldo_inicio': saldo_inicio,
        'receita_total': receita_total,
        'despesa_total': despesa_total,

        # Transações do mês
        'transacoes_totaisMes': transacoes_totaisMes,
        'transacoes_receitasMes': transacoes_receitasMes,
        'transcacoes_despesasMes': transcacoes_despesasMes,
        'transacoes_mes': transacoes_mes,

        # Dados de metas
        'total_quantidade_metas': total_quantidade_metas,
        'metas_ativas': metas_ativas,
        'metas_concluidas': metas_concluidas,
        'metas_ultrapassadas': metas_utrapassadas,
        'metas_naoatingidas': metas_naoatingidas,
        'todas_metas': todas_metas,
        'metas_intervalo': metas_intervalo,

        # Dados de objetivos
        'total_objetivos': total_objetivos,
        'objetivos_ativosTotal': objetivos_ativosTotal,
        'objetivos_pausadosTotal': objetivos_pausadosTotal,
        'objetivos_concluidosTotal': objetivos_concluidosTotal,
        'objetivos_criadosMes': objetivos_criadosMes,
        'objetivos_concluidosMes': objetivos_concluidosMes,
        'objetivos': objetivos,

        # Análise detalhada do mês
        'maior_categoria_receita': maior_categoria_receita,
        'valor_maior_categoria_receita': valor_maior_categoria_receita,
        'menor_categoria_receita': menor_categoria_receita,
        'valor_menor_categoria_receita': valor_menor_categoria_receita,
        'maior_categoria_despesa': maior_categoria_despesa,
        'valor_maior_categoria_despesa': valor_maior_categoria_despesa,
        'menor_categoria_despesa': menor_categoria_despesa,
        'valor_menor_categoria_despesa': valor_menor_categoria_despesa,

        # Frequência de transações no mês
        'frequencia_transacoes': frequencia_transacoes,

        # Categorias (caso precise renderizar filtros ou tabelas)
        'categorias': categorias,
    }

    return render(request, 'relatorios.html', context)