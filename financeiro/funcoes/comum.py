from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from financeiro.models import Perfil, Receita, DespesaFixa, DespesaVariavel, Metas

class OperacoesUsuarios:
    tabelas = {
        "Receita": Receita,
        "DespesaFixa": DespesaFixa,
        "DespesaVariavel": DespesaVariavel
    }
    def __init__(self, user_id):
        self.__perfil = Perfil.objects.filter(fk_user=user_id).first()
        if not self.__perfil:
            raise ValueError(f"Erro: Nenhum perfil encontrado para o usuário {user_id}.")

    def total_valor(self, Nome_tabela):
        modelo = self.tabelas.get(Nome_tabela)
        if not modelo:
            raise ValueError(f"Error: tabela {Nome_tabela} não encontrada.")
        total = modelo.objects.filter(perfil=self.__perfil).aggregate(Sum("valor"))["valor__sum"] or 0
        return total

    def calcular_saldo(self):
        total_receitas = self.total_valor("Receita")
        total_despesas_fixas = self.total_valor("DespesaFixa")
        total_despesas_variaveis = self.total_valor("DespesaVariavel")

        saldo = total_receitas - (total_despesas_fixas + total_despesas_variaveis)
        return saldo
