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
                    ):
        hoje = date.today()
        status = 'A'
        data_conclusao = None

        if valor_guardado.valor > valor_objetivo.valor:
            return 'Valor que já está guardado excede o valor do objetivo'

        if data_fim.valor < hoje and status == 'A':
            status = 'T'

        if valor_guardado.valor == valor_objetivo.valor:
            status = 'C'
            data_conclusao = hoje

        Objetivos.objects.create(user_fk= self.user
                                , titulo=titulo
                                , valor_objetivo=valor_objetivo.valor
                                , valor_guardado=valor_guardado.valor
                                , data_fim=data_fim.valor
                                , status=status
                                , data_conclusao=data_conclusao
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
            objetivo.data_conclusao = date.today()
        else:
            objetivo.status = 'A'

        objetivo.titulo = novo_titulo
        objetivo.valor_objetivo = novo_valor_objetivo
        objetivo.data_fim = nova_data_fim.valor
        objetivo.save()

    def deletar(self, objetivo: Objetivos):
        objetivo.delete()

    def atualizarObjetivo(self, objetivo: Objetivos):
        if not objetivo.status == 'A':
            return 'Objetivo pausado ou concluido'
        else:
            hoje = date.today()
            if objetivo.data_fim < hoje and objetivo.valor_guardado < objetivo.valor_objetivo:
                objetivo.status = 'T'
        try:
            objetivo.save()
        except Exception as e:
            raise Exception('Não foi possivel atualizar o objetivo')

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
            Objetivo.data_conclusao = date.today()

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
                Objetivo.data_conclusao = None
            else:
                Objetivo.status = 'A'
                Objetivo.data_conclusao = None

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
        data_ano_passado = Data.variarMes(hoje.month, hoje.year, -11)
        data = Data(data_ano_passado.valor.replace(day=1))
        transacoes = TransacaoObjetivo.objects.filter(objetivo_fk__user_fk=self.user)
        datas = []
        valores = []
        valor_mes = 0
        for i in range(12):
            deposito_mes = transacoes.filter(objetivo_fk__id=objetivo_id ,tipo='D' ,data__month=data.valor.month, data__year=data.valor.year).aggregate(total_mes=Sum('valor'))['total_mes']
            resgate_mes = transacoes.filter(objetivo_fk__id=objetivo_id ,tipo='R' ,data__month=data.valor.month, data__year=data.valor.year).aggregate(total_mes=Sum('valor'))['total_mes']
            if not deposito_mes:
                deposito_mes = 0
            if not resgate_mes:
                resgate_mes = 0
            total_mes = deposito_mes - resgate_mes
            valor_mes += total_mes
            data_formatada = Data.formatarMesAno(data.valor.month,data.valor.year)
            data = Data.incrementarMes(data.valor)
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

    def totalEconomizadoPorMes(self,mes:int,ano:int):
        inicio_mes = Data.primeiroDiaMes(mes,ano)
        proximo_mes = Data.incrementarMes(inicio_mes)

        parcelas = TransacaoObjetivo.objects.filter(objetivo_fk__user_fk=self.user
                                                    , data__gte=inicio_mes
                                                    , data__lt=proximo_mes.valor
        )
        economia = Decimal('0')
        for parcela in parcelas:
            if parcela.tipo == 'D':
                economia += parcela.valor
            elif parcela.tipo == 'R':
                economia -= parcela.valor
        return economia