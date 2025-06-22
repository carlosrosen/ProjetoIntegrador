from datetime import date
import datetime
import calendar

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.utils import timezone

from decimal import Decimal

from apps.financeiro.models import Categoria, Transacao, ParcelasTransacao, HistoricoSaldo
from apps.financeiro.operacoes.getter import GetterFinanceiro

from apps.metas.models import Metas
from apps.metas.operacoes.metas import GetMetas

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

    getter_financeiro = GetterFinanceiro(request.user.id)
    mes = date.today().month
    ano = date.today().year

    primeiro_dia = Data.primeiroDiaMes(mes,ano)
    ultimo_dia = Data.ultimoDiaMes(mes, ano)

    user = CustomUser.objects.get(id=request.user.id)

    categorias = Categoria.objects.all()

    # Total

    saldo_atual = user.saldoAtual
    receita_mes = getter_financeiro.receitaTotalMes(mes, ano)
    despesa_mes = getter_financeiro.despesaTotalMes(mes, ano)
    saldo_mes = receita_mes - despesa_mes

    # Resumo geral
    proximo_mes = Data.incrementarMes(primeiro_dia)
    saldo_inicio = HistoricoSaldo.getSaldoInicioMes(user, mes, ano)
    saldo_final = HistoricoSaldo.getSaldoInicioMes(user, proximo_mes.valor.month, proximo_mes.valor.year)
    # Ganho/Lucro

    lucro = saldo_final - saldo_inicio

    transacoes_mes = ParcelasTransacao.objects.filter(transacao_fk__user_fk=user, data__range=(primeiro_dia, ultimo_dia))
    transacoes_totaisMes = transacoes_mes.count()  # Quantidade de transacoes no total no mes
    transacoes_receitasMes = transacoes_mes.filter(transacao_fk__tipo="R").count() # Quantidade de transacoes de receitas no mes
    transacoes_despesasMes = transacoes_mes.filter(transacao_fk__tipo="D").count() # Quantidade de transacoes de despesas no mes
    maior_receita = getter_financeiro.maiorTransacaoMes(mes, ano, "Receita")
    maior_despesa = getter_financeiro.maiorTransacaoMes(mes, ano, "Despesa")

    # Metas
    todas_metas = Metas.objects.filter(user_fk=user)

    total_quantidade_metas = todas_metas.count() # Quantidade total de metas criadas
    metas_ativas = todas_metas.filter(tipo="A").count() # Quantidade total de metas ativas

    metas_intervalo = todas_metas.filter(data_conclusao__range=(primeiro_dia, ultimo_dia))

    metas_concluidas, metas_utrapassadas, metas_naoatingidas  = metas_intervalo.filter(tipo="C").count(), metas_intervalo.filter(tipo="U").count(), metas_intervalo.filter(tipo="N").count()

    getter_metas = GetMetas(request.user.id)

    taxa_de_sucesso = getter_metas.taxaConclusao()

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
    valores_historico, dias_historico = getter_financeiro.historicoSaldoMes(mes, ano)

    # Grafico de fluxo de caixa do mês
    valores_fluxo = getter_financeiro.fluxoCaixaMes(mes, ano)

    # Gráfico de categorias

    categorias_receita = getter_financeiro.valorTotalDasCategorias(mes,ano,'receita')
    categorias_despesa = getter_financeiro.valorTotalDasCategorias(mes,ano,'despesa')


    # Gastos por dia da semana

    dias_semana, gastos_dia_semana = getter_financeiro.gastosPorDiaDaSemana(mes,ano)

    context = {
        'user': user,
        # Dados básicos
        'mes': mes,
        'ano': ano,

        # Saldo e resumo financeiro
        'saldo_atual': saldo_atual,
        'saldo_total': saldo_mes,
        'saldo_inicio': saldo_inicio,
        'saldo_final': saldo_final,
        'receita_total': receita_mes,
        'despesa_total': despesa_mes,
        'lucro': lucro,

        # Transações do mês
        'transacoes_totaisMes': transacoes_totaisMes,
        'transacoes_receitasMes': transacoes_receitasMes,
        'transacoes_despesasMes': transacoes_despesasMes,

        # Dados de metas
        'total_quantidade_metas': total_quantidade_metas,
        'metas_ativas': metas_ativas,
        'metas_concluidas': metas_concluidas,
        'metas_ultrapassadas': metas_utrapassadas,
        'metas_naoatingidas': metas_naoatingidas,
        'taxa_sucesso_metas': taxa_de_sucesso,

        # Dados de objetivos
        'total_objetivos': total_objetivos,
        'objetivos_ativosTotal': objetivos_ativosTotal,
        'objetivos_pausadosTotal': objetivos_pausadosTotal,
        'objetivos_concluidosTotal': objetivos_concluidosTotal,
        'objetivos_criadosMes': objetivos_criadosMes,
        'objetivos_concluidosMes': objetivos_concluidosMes,

        # Análise detalhada do mês
        'maior_categoria_receita': maior_categoria_receita,
        'valor_maior_categoria_receita': valor_maior_categoria_receita,
        'menor_categoria_receita': menor_categoria_receita,
        'valor_menor_categoria_receita': valor_menor_categoria_receita,
        'maior_categoria_despesa': maior_categoria_despesa,
        'valor_maior_categoria_despesa': valor_maior_categoria_despesa,
        'menor_categoria_despesa': menor_categoria_despesa,
        'valor_menor_categoria_despesa': valor_menor_categoria_despesa,
        'maior_receita': maior_receita,
        'maior_despesa': maior_despesa,

        # Frequência de transações no mês
        'frequencia_transacoes': frequencia_transacoes,

        # Categorias (caso precise renderizar filtros ou tabelas)
        'categorias': categorias,

        # Gráfico de variação do saldo
        'valores_historico': ','.join(valores_historico),
        'dias_historico': ','.join(dias_historico),

        # Gráfico de fluxo de saldo
        'valores_fluxo': ','.join(valores_fluxo),

        # Gráfico das categorias
        'categorias_receita': ','.join(categorias_receita.keys()),
        'valores_categoria_receita': ','.join(categorias_receita.values()),
        'categorias_despesa': ','.join(categorias_despesa.keys()),
        'valores_categorias_despesa': ','.join(categorias_despesa.values()),

        'gastos_dia_da_semana': ','.join(gastos_dia_semana),
        'dias_semana': ','.join(dias_semana)
    }

    return render(request, 'relatorios.html', context)