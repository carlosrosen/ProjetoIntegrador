from django.contrib.auth.models import AbstractBaseUser
from financeiro.models import HistoricoSaldo
from financeiro.models import ParcelasTransacao

from datetime import date

class HistoricoSaldo:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario Invalido')
        self.user = user


    def salvarInicioMes(self,valor):
        ultima_insercao = HistoricoSaldo.objects.filter(user=self.user)[-1]
