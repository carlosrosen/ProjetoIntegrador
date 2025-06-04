from django.contrib.auth.models import AbstractBaseUser
from apps.usuarios.models import CustomUser
from typing import cast

from apps.objetivos.models import Objetivos, TransacaoObjetivo

from django.db.models import F, ExpressionWrapper, DecimalField

from apps.objetivos.dominio.valorobjetivo import ValorObjetivo
from apps.objetivos.dominio.tipoobjetivo import TipoObjetivo
from apps.objetivos.dominio.status import Status
from common.dominio.data import Data

from itertools import chain

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

    def deposito(self
                     ,Objetivo: Objetivos
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

        if Objetivo.status == 'C':
            return 'Objetivo já está concluido'

        if Valor.valor > valor_limite:
            return 'Excede o objetivo estabelecido'
        elif Valor.valor == valor_limite:
            Objetivo.status = 'C'

        # Fazendo a soma do valor
        Objetivo.valor_guardado += Valor.valor

        # Criação do registro de deposito
        TransacaoObjetivo.objects.create(objetivo_fk=Objetivo
                                             ,tipo= 'D'
                                             ,valor=Valor.valor
                                             ,data=Data
        )

        try:
            Objetivo.save()
        except Exception as e:
            raise Exception('Não foi possivel criar a transação objetivo')

    def resgate(self
                     ,Objetivo: Objetivos
                     ,Valor: ValorObjetivo
                     ,Data: Data
                     ):

        # Não pode prosseguir caso o objetivo esteja pausado
        if Objetivo.status == 'P':
            return 'Objetivo Pausado'

        if Valor.valor > Objetivo.valor_guardado:
            return 'Valor informado para resgate excede o valor que está guardado'

        if Objetivo.status == 'C':
            if(Data > Objetivo.data_fim):
                Objetivo.status = 'T'
            else:
                Objetivo.status = 'A'

        # Fazendo a subtração do valor
        Objetivo.valor_guardado -= Valor.valor

        # Criação do registro de resgate
        TransacaoObjetivo.objects.create(objetivo_fk=Objetivo
                                             ,tipo='R'
                                             ,valor=Valor.valor
                                             ,data=Data
        )

        try:
            Objetivo.save()
        except Exception as e:
            raise Exception('Não foi possivel criar a transação objetivo')

class GetObjetivo:
    def __init__(self, user_id):
        self.user = CustomUser.objects.get(id=user_id)

    def informacoes(self, objetivo_id):
        return Objetivos.objects.get(user_fk=self.user, id=objetivo_id)

    def transacoes(self, objetivo_id):
        objetivo = Objetivos.objects.get(user_fk=self.user ,id=objetivo_id)
        return TransacaoObjetivo.objects.filter(user_fk=self.user ,objetivo_fk=objetivo)

    def variacao(self, objetivo_id):
        transacoes = TransacaoObjetivo.objects.filter(user_fk=self.user ,objetivo_fk=objetivo_id).order_by('data')
        ## Fazer depois o gráfico do valor guardado
        pass

    def todosEmOrdem(self) -> list:
        objetivos = Objetivos.objects.filter(user_fk=self.user)

        # Aplicar anotação e ordenar por menor diferença
        ativos = objetivos.filter(status='A')
        pausado = objetivos.filter(status='P')
        atrasados = objetivos.filter(status='T')
        concluidos = objetivos.filter(status='C')

        #A função sorted utiliza timSort que é uma ordenação hibrida baseada em Heap sort e InsertionSort
        ativos = sorted(ativos, key=lambda objetivo: abs(objetivo.valor_objetivo - objetivo.valor_guardado))
        pausado = sorted(pausado, key=lambda objetivo: abs(objetivo.valor_objetivo - objetivo.valor_guardado))
        atrasados = sorted(atrasados, key=lambda objetivo: abs(objetivo.valor_objetivo - objetivo.valor_guardado))
        concluidos = sorted(concluidos, key=lambda objetivo: abs(objetivo.valor_objetivo - objetivo.valor_guardado))

        return list(chain( ativos, atrasados, pausado, concluidos))




