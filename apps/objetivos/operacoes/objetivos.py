from django.contrib.auth.models import AbstractBaseUser
from apps.usuarios.models import CustomUser
from typing import cast

from apps.objetivos.models import Objetivos, TransacaoObjetivo

from apps.objetivos.dominio.valorobjetivo import ValorObjetivo
from apps.objetivos.dominio.tipoobjetivo import TipoObjetivo
from apps.objetivos.dominio.status import Status
from common.dominio.data import Data

# Estou importando do financeiro a formatação

class OperacoesObjetivo:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario invalido')
        self.user = cast(CustomUser, user)

    def criar(self
                    , titulo: str
                    , valor_objetivo: ValorObjetivo
                    , valor_guardado: ValorObjetivo
                    , data_fim: Data
                    , status: Status
                    ):

        if valor_guardado.valor > valor_objetivo.valor:
            return 'Valor que já está guardado excede o valor do objetivo'
        elif valor_guardado.valor == valor_objetivo.valor:
            status.valor = 'C'

        Objetivos.objects.create(user_fk= self.user
                                , titulo=titulo
                                , valor_objetivo=valor_objetivo.valor
                                , valor_guardado=valor_guardado.valor
                                , data_fim=data_fim.valor
                                , status=status.valor
        )

    def editar(self
                       , objetivo: Objetivos
                       , novo_titulo: str
                       , novo_valor_objetivo: ValorObjetivo
                       , nova_data_fim: Data
                       , novo_status: Status
                       ):

        if novo_status.valor == 'P':
            objetivo.status = 'P'

        if novo_valor_objetivo.valor < objetivo.valor_guardado:
            return 'O novo valor do objetivo é menor que o valor já guardado'
        elif novo_valor_objetivo.valor == objetivo.valor_guardado:
            objetivo.status = 'C'
        elif novo_valor_objetivo.valor > objetivo.valor_guardado and objetivo.status == 'C':
            objetivo.status = 'A'
        else:
            objetivo.status = novo_status.valor

        objetivo.titulo = novo_titulo
        objetivo.valor_objetivo = novo_valor_objetivo.valor
        objetivo.data_fim = nova_data_fim.valor
        objetivo.save()

    def deletar(self, objetivo: Objetivos):
        objetivo.delete()

    def criarTransacao(self
                     ,Objetivo: Objetivos
                     ,Tipo: TipoObjetivo
                     ,Valor: ValorObjetivo
                     ,Data: Data
                     ):

        # Não pode prosseguir nas operações caso o objetivo esteja pausado
        if Objetivo.status == 'P':
            return 'Objetivo Pausado'

        valor_objetivo = Objetivo.valor_objetivo
        valor_guardado = Objetivo.valor_guardado

        # O valor que falta para atingir o objetivo
        valor_limite = ValorObjetivo.valorLimite(valor_objetivo, valor_guardado)

        # Passa pelas operações dependendo do seu tipo
        if Tipo.valor == 'D':
            if Objetivo.status == 'C':
                return 'Objetivo já está concluido'
            if Valor.valor > valor_limite:
                return'Excede o objetivo estabelecido'
            if Valor.valor == valor_limite:
                Objetivo.status = 'C'
            Objetivo.valor_guardado += Valor.valor

        elif Tipo.valor == 'R':
            if Valor.valor > valor_guardado:
                return 'Valor informado para resgate excede o valor que está guardado'
            if Objetivo.status == 'C':
                Objetivo.status = 'A'
            Objetivo.valor_guardado -= Valor.valor

        # Criação do registro das operações acima
        TransacaoObjetivo.objects.create(objetivo_fk=Objetivo
                                             ,tipo=Tipo.valor
                                             ,valor=Valor.valor
                                             ,data=Data
        )

        try:
            Objetivo.save()
        except Exception as e:
            raise Exception('Não foi possivel criar a transação objetivo')
