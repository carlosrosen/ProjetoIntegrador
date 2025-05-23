from django.contrib.auth.models import AbstractBaseUser

from metas.models import Objetivos, TransacaoObjetivo

from metas.dominio.valorobjetivo import ValorObjetivo
from metas.dominio.tipoobjetivo import TipoObjetivo, TipoObjetivo
from metas.dominio.status import Status
from financeiro.dominio.data import Data

# Estou importando do financeiro a formatação

class OperacoesObjetivo:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario invalido')
        self.user = user

    def criarObjetivo(self
                    , titulo: str
                    , valor_inicial: ValorObjetivo
                    , valor_objetivo: ValorObjetivo
                    , valor_guardado: ValorObjetivo
                    , data_inicio: Data
                    , data_fim: Data
                    , status: Status
                    ):

        if valor_objetivo.valor >= valor_inicial.valor:
            status.valor = 'C'
            valor_guardado.valor =  valor_objetivo.valor

        Objetivos.objects.create(user_fk= self.user
                                , titulo=titulo
                                , valor_objetivo=valor_objetivo.valor
                                , valor_guardado=valor_inicial.valor
                                , data_inicio=data_inicio.valor
                                , data_fim=data_fim.valor
                                , status=status.valor
        )

    def criarTransacaoObj(self
                     ,Objetivo: Objetivos
                     ,Tipo: TipoObjetivo
                     ,Valor: ValorObjetivo
                     ,Data: Data
                     ):
        if Objetivo.status == 'P':
            raise ValueError('Objetivo Pausado')

        valor_objetivo = Objetivo.valor_objetivo
        valor_guardado = Objetivo.valor_guardado
        valor_limite = ValorObjetivo.valorLimite(valor_objetivo, valor_guardado)

        if Tipo.valor == 'D':
            if Objetivo.status == 'C':
                raise ValueError('Objetivo já Concluido')
            if Valor.valor > valor_limite:
                Valor.valor = valor_limite
                Objetivo.status = 'C'
            Objetivo.valor_guardado += Valor.valor

        elif Tipo.valor == 'R':
            if Objetivo.status == 'C':
                Objetivo.status = 'A'
            if Valor.valor > valor_guardado:
                raise ValueError('Valor Invalido')
            Objetivo.valor_guardado -= Valor.valor

        TransacaoObjetivo.objects.create(objetivo_fk=Objetivo
                                             ,tipo=Tipo.valor
                                             ,valor=Valor.valor
                                             ,data=Data
        )

        try:
            Objetivo.save()
        except Exception as e:
            raise Exception('Não foi possivel criar a transação objetivo')
