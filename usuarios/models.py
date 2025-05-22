from django.contrib.auth.models import AbstractUser
from django.db import models

from decimal import Decimal

class CustomUser(AbstractUser):
    saldoAtual = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def operarSaldoAtual(self, valor:Decimal, tipo:str):
        if valor < 0:
            valor = -valor
        if tipo == 'R':
            self.saldoAtual += valor
        elif tipo == 'D':
            self.saldoAtual -= valor
        self.save()

    def operarSaldoAtualInverso(self, valor:Decimal, tipo:str):
        if valor < 0:
            valor = -valor
        if tipo == 'R':
            self.saldoAtual -= valor
        elif tipo == 'D':
            self.saldoAtual += valor
        self.save()

    def editarSaldoAtualComTipo(self, valor_antigo:str, valor_novo:str, tipo:str):
        valor_antigo = Decimal(valor_antigo)
        valor_novo = Decimal(valor_novo)
        if tipo.upper() == 'R':
            if valor_antigo > valor_novo:
                self.saldoAtual -= valor_antigo - valor_novo
            elif valor_novo < valor_antigo:
                self.saldoAtual += valor_antigo - valor_novo
        elif tipo.upper() == 'D':
            if valor_antigo > valor_novo:
                self.saldoAtual += valor_antigo - valor_novo
            elif valor_novo < valor_antigo:
                self.saldoAtual -= valor_antigo - valor_novo
            self.save()
        else:
            raise Exception('Tipo desconhecido')

        self.save()

    def editarDespesa(self, valor_antigo:str, valor_novo:str):
        valor_antigo = Decimal(valor_antigo)
        valor_novo = Decimal(valor_novo)





    def __str__(self):
        return f'''
        {str(self.id)} - {self.username} - {self.email} - {str(self.saldoAtual)}
        '''
