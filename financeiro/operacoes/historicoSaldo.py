from django.contrib.auth.models import AbstractBaseUser
from financeiro.models import HistoricoSaldo
from financeiro.models import ParcelasTransacao

from decimal import Decimal

from datetime import date

class HistoricoSaldo:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario Invalido')
        self.user = user


    def salvarInicioMes(self,valor):
        mes_atual = date(date.today().year, date.today().month,1)
        try:
            ultima_insercao = HistoricoSaldo.objects.filter(user_fk=self.user).latest('data')
        except HistoricoSaldo.DoesNotExist:
            HistoricoSaldo.objects.create(user=self.user
                                          , data=mes_atual
                                          , valor=Decimal(0.0)
                                          )
            return None
        if ultima_insercao == None:
            HistoricoSaldo.objects.create()
        intervalo = ParcelasTransacao.buscaDataIntervalo(ultima_insercao, mes_atual)



