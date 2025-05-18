from django.contrib.auth.models import AbstractUser
from django.db import models

from decimal import Decimal

class CustomUser(AbstractUser):
    saldoAtual = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def subtrairSaldoAtual(self, valor):
        valor = Decimal(valor)
        if valor < 0:
            valor = -valor
        self.saldoAtual -= valor
        self.save()

    def somarSaldoAtual(self, valor):
        valor = Decimal(valor)
        if valor < 0:
            valor = -valor
        self.saldoAtual += valor
        self.save()

    def editarReceita(self, valor_antigo:str, valor_novo:str):
        valor_antigo = Decimal(valor_antigo)
        valor_novo = Decimal(valor_novo)
        if valor_antigo > valor_novo:
            self.saldoAtual -= valor_antigo - valor_novo
        elif valor_novo < valor_antigo:
            self.saldoAtual += valor_antigo - valor_novo
        self.save()

    def editarDespesa(self, valor_antigo:str, valor_novo:str):
        valor_antigo = Decimal(valor_antigo)
        valor_novo = Decimal(valor_novo)
        if valor_antigo > valor_novo:
            self.saldoAtual += valor_antigo - valor_novo
        elif valor_novo < valor_antigo:
            self.saldoAtual -= valor_antigo - valor_novo
        self.save()




    def __str__(self):
        return self.id + self.username + self.email + str(self.saldoAtual)
