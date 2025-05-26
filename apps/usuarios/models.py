from django.contrib.auth.models import AbstractUser
from django.db import models

from decimal import Decimal

class CustomUser(AbstractUser):
    saldoAtual = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    dataUltimaTransacaoVerificada = models.DateField(null=True, blank=True)

    def operarSaldoAtual(self, valor:Decimal, tipo:str, inversor:bool = False):
        valor = abs(valor)
        if inversor == True:
            valor = -valor
        if tipo == 'R':
            self.saldoAtual += valor
        elif tipo == 'D':
            self.saldoAtual -= valor
        self.save()

    def __str__(self):
        return f'''
        {str(self.id)} - {self.username} - {self.email} - {str(self.saldoAtual)}
        '''
