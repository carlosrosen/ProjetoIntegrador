from django.contrib.auth.models import AbstractBaseUser

from metas.models import Objetivos

from financeiro.dominio.valor import Valor
from financeiro.dominio.data import Data

# Estou importando do financeiro a formatação

class OperacoesObjetivo:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario invalido')
        self.user = user

        def criarObjetivo(self
                          , titulo: str
                          , valor_objetivo: Valor
                          , valor_guardado: Valor
                          , data_inicio: Data
                          , data_fim: Data
                          , status: str
                          ):

            if valor_objetivo == valor_guardado:
                status = 'C'

            Objetivos.objects.create(user_fk= self.user
                                     ,titulo=titulo
                                     ,valor_objetivo=valor_objetivo
                                     ,valor_guardado=valor_guardado
                                     ,data_inicio=data_inicio
                                     ,data_fim=data_fim
                                     ,status=status
            )

