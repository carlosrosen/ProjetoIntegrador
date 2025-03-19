from django.db.models import Sum
from financeiro.models import Receita, DespesaFixa, DespesaVariavel, Perfil

def calcular_saldo(perfil):
    # Calculando a soma das receitas
    total_receitas = Receita.objects.filter(perfil=perfil).aggregate(Sum('valor'))['valor__sum'] or 0

    # Calculando a soma das despesas fixas
    total_despesas_fixas = DespesaFixa.objects.filter(perfil=perfil).aggregate(Sum('valor'))['valor__sum'] or 0

    # Calculando a soma das despesas variáveis
    total_despesas_variaveis = DespesaVariavel.objects.filter(perfil=perfil).aggregate(Sum('valor'))['valor__sum'] or 0

    # Calculando o saldo final
    saldo = total_receitas - (total_despesas_fixas + total_despesas_variaveis)

    return saldo
