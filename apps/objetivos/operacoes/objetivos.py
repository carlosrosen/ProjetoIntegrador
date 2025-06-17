from django.contrib.auth.models import AbstractBaseUser
from apps.usuarios.models import CustomUser
from typing import cast

from apps.objetivos.models import Objetivos, TransacaoObjetivo

from django.db.models import F, ExpressionWrapper, DecimalField, Sum

from apps.objetivos.dominio.valorobjetivo import ValorObjetivo
from apps.objetivos.dominio.tipoobjetivo import TipoObjetivo
from apps.objetivos.dominio.status import Status

from datetime import date
from common.dominio.data import Data

from decimal import Decimal, ROUND_DOWN

from itertools import chain

# Estou importando do financeiro a formatação

class OperacoesObjetivo:
    def __init__(self, user_id):
        self.user = CustomUser.objects.get(id=user_id)

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
               , novo_valor_objetivo: Decimal
               , nova_data_fim: Data
               , pausado: bool
               ):

        if novo_valor_objetivo < objetivo.valor_guardado:
            return 'O novo valor do objetivo é menor que o valor já guardado'

        if pausado:
            objetivo.status = 'P'
        elif novo_valor_objetivo == objetivo.valor_guardado:
            objetivo.status = 'C'
        else:
            objetivo.status = 'A'

        objetivo.titulo = novo_titulo
        objetivo.valor_objetivo = novo_valor_objetivo
        objetivo.data_fim = nova_data_fim.valor
        objetivo.save()

    def deletar(self, objetivo: Objetivos):
        objetivo.delete()

    def deposito(self
                     ,Objetivo: Objetivos
                     ,Valor: Decimal
                     ,data: date
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

        if Valor > valor_limite:
            return 'Excede o objetivo estabelecido'
        elif Valor == valor_limite:
            Objetivo.status = 'C'

        # Fazendo a soma do valor
        Objetivo.valor_guardado += Valor

        # Criação do registro de deposito
        TransacaoObjetivo.objects.create(objetivo_fk=Objetivo
                                             ,tipo= 'D'
                                             ,valor=Valor
                                             ,data=data
        )

        try:
            Objetivo.save()
        except Exception as e:
            raise Exception('Não foi possivel criar a transação objetivo')

    def resgate(self
                     ,Objetivo: Objetivos
                     ,Valor: Decimal
                     ,data: date
                     ):

        # Não pode prosseguir caso o objetivo esteja pausado
        if Objetivo.status == 'P':
            return 'Objetivo Pausado'

        if Valor > Objetivo.valor_guardado:
            return 'Valor informado para resgate excede o valor que está guardado'

        if Objetivo.status == 'C':
            if data > Objetivo.data_fim:
                Objetivo.status = 'T'
            else:
                Objetivo.status = 'A'

        # Fazendo a subtração do valor
        Objetivo.valor_guardado -= Valor

        # Criação do registro de resgate
        TransacaoObjetivo.objects.create(objetivo_fk=Objetivo
                                             ,tipo='R'
                                             ,valor=Valor
                                             ,data=data
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
        hoje = date.today()
        print(hoje)
        data_ano_passado = Data.variarMes(hoje.month, hoje.year, -11)
        print(data_ano_passado.valor)
        data = Data(data_ano_passado.valor.replace(day=1))
        transacoes = TransacaoObjetivo.objects.filter(objetivo_fk__user_fk=self.user)
        datas = []
        valores = []
        valor_mes = 0
        for i in range(12):
            deposito_mes = transacoes.filter(tipo='D' ,data__month=data.valor.month, data__year=data.valor.year).aggregate(total_mes=Sum('valor'))['total_mes']
            resgate_mes = transacoes.filter(tipo='R' ,data__month=data.valor.month, data__year=data.valor.year).aggregate(total_mes=Sum('valor'))['total_mes']
            if not deposito_mes:
                deposito_mes = 0
            if not resgate_mes:
                resgate_mes = 0
            total_mes = deposito_mes - resgate_mes
            valor_mes += total_mes
            data = Data.incrementarMes(data.valor)
            data_formatada = Data.formatarMesAno(data.valor.month ,data.valor.year)
            datas.append(data_formatada)
            valores.append(str(Decimal(valor_mes).quantize(Decimal('0.01'), ROUND_DOWN)))
        datas = ','.join(datas)
        valores = ','.join(valores)
        return datas, valores



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




