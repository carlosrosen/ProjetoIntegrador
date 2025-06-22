from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Sum, Max, Min, F
from django.db.models.functions import ExtractWeekDay
from unicodedata import category

from apps.financeiro.operacoes.saldo import Historico
from apps.financeiro.operacoes.transacao import OperacoesTransacao
from apps.usuarios.models import CustomUser

from common.dominio.data import Data
from apps.financeiro.models import *

from decimal import Decimal, ROUND_DOWN

class GetterFinanceiro:
    def __init__(self, user_id: int):
        self.user: CustomUser = CustomUser.objects.get(id=user_id)
        self.transacoes = OperacoesTransacao(user_id=self.user.id)
        self.historico = Historico(user_id=self.user.id)

    def historicoSaldoMes(self,mes:int, ano:int) -> tuple[list[str], list[str]]:
        mes, ano = abs(mes), abs(ano)
        data = Data(Data.primeiroDiaMes(mes=mes, ano=ano))
        proxima_data = Data.incrementarMes(data.valor)
        dados = []
        dias = []

        intervalo_parcelas = ParcelasTransacao.todasParcelasMes(user=self.user,mes=mes,ano=ano)
        quantidade_dias = abs(proxima_data.valor - data.valor).days

        try:
            historico = HistoricoSaldo.objects.get(user_fk=self.user, data=data.valor)
        except ObjectDoesNotExist:
            for dia in range(1,quantidade_dias+1):
                dados.append('0')
                dia = str(dia)
                if len(dia) == 1:
                    dia = '0'+dia
                dias.append(str(dia))
            return dados, dias
        except MultipleObjectsReturned:
            raise IndexError('Ocorreu um erro inesperado com a busca do valores do saldo.')

        saldo = historico.saldo

        for dia in range(1, quantidade_dias+1):
            parcelas_dia = intervalo_parcelas.filter(data=date(day=dia,month=mes,year=ano))
            if not parcelas_dia.exists():
                dados.append(str(saldo))
                if len(str(dia)) == 1:
                    dias.append('0'+ str(dia))
                else:
                    dias.append(str(dia))
                continue
            for parcela in parcelas_dia:
                if parcela.transacao_fk.tipo == 'R':
                    saldo += parcela.valor
                elif parcela.transacao_fk.tipo == 'D':
                    saldo -= parcela.valor
            dados.append(str(saldo))
            if len(str(dia)) == 1:
                dias.append('0' + str(dia))
            else:
                dias.append(str(dia))
        return dados, dias

    def historicoSaldoAno(self,ano: int) -> list:
        ano = abs(ano)
        dados = []
        for mes in range(1,13):
            dados.extend(self.historicoSaldoMes(mes=mes,ano=ano))
        return dados

    def receitaTotalMes(self,mes:int, ano:int) -> str | Decimal:
        mes, ano = abs(mes), abs(ano)
        ganhos:Decimal = ParcelasTransacao.objects.filter(transacao_fk__user_fk= self.user
                                                , transacao_fk__tipo='R'
                                                , pago=True
                                                , data__month=mes, data__year=ano).aggregate(total = Sum('valor'))['total']
        if ganhos is None:
            return Decimal('0.00')
        return  ganhos.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

    def despesaTotalMes(self,mes:int, ano:int):
        gastos = ParcelasTransacao.objects.filter(transacao_fk__user_fk= self.user
                                                , transacao_fk__tipo='D'
                                                , pago=True
                                                , data__month=mes, data__year=ano).aggregate(total = Sum('valor'))['total']
        if gastos is None:
            return Decimal('0.00')
        return gastos.quantize(Decimal('0.01'), rounding=ROUND_DOWN)

    def saldoAtual(self):
        return self.user.saldoAtual

    def valorTotalDasCategorias(self, mes:int, ano:int, tipo = 'all') -> dict:
        categorias = Categoria.objects.all()
        parcelas_mes = ParcelasTransacao.todasParcelasMes(self.user,mes=mes,ano=ano)
        if tipo[0].upper() == 'R':
            parcelas_mes = parcelas_mes.filter(transacao_fk__tipo='R')
            categorias = categorias.filter(tipo='R')
        elif tipo[0].upper() == 'D':
            parcelas_mes = parcelas_mes.filter(transacao_fk__tipo='D')
            categorias = categorias.filter(tipo='D')
        dicionario = {}

        for categoria in categorias:
            valor_total = parcelas_mes.filter(transacao_fk__categoria_fk=categoria
                                              , pago=True).aggregate(total=Sum('valor'))['total']
            if valor_total is None:
                continue
            dicionario[categoria.nome] = str(valor_total)

        return dicionario

    def proximasTresParcelas(self):
        parcelas = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user
                                                    , data__gt=date.today()
                                                    )
        dados = []
        for parcela in parcelas:
            if len(dados) <= 3:
                dados.append(parcela)
                if len(dados) == 3:
                    break
        return dados[::-1]

    def ultimaCincoParcelas(self):
        parcelas = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user).order_by("-id")
        dados = []
        tamanho = parcelas.count()
        inicio = tamanho - 5
        if inicio < 0:
            inicio = 0
        for parcela in parcelas[inicio:tamanho]:
            dados.append(parcela)
        return dados

    def todasParcelasMes(self, mes:int, ano:int):
        data = Data.inicializar(dia=1,mes=mes,ano=ano)
        parcelas = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user
                                                    , data__gte=data.valor
                                                    , data__lt=Data.incrementarMes(data.valor).valor
        )
        return parcelas

    def fluxoCaixaMes(self,mes:int ,ano:int):
        inicio_mes = Data.inicializar(1,mes,ano)
        inicio_proximo_mes = Data.incrementarMes(inicio_mes.valor)
        parcelas = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user
                                                     , data__gte=inicio_mes.valor
                                                     , data__lt= inicio_proximo_mes.valor
        )
        quantidade_dias = abs(inicio_proximo_mes.valor - inicio_mes.valor)

        dados = []
        for dia in range(1,quantidade_dias.days):
            parcelas_dia = parcelas.filter(data__day=dia)
            total_dia = 0
            if parcelas_dia.count() <= 0:
                dados.append(str(total_dia))
                continue

            for parcela in parcelas_dia:
                if parcela.transacao_fk.tipo == 'R':
                    total_dia += parcela.valor
                elif parcela.transacao_fk.tipo == 'D':
                    total_dia -= parcela.valor
                dados.append(str(total_dia))

        return dados

    def MaiorEMenorValoresDasCategoriasDoMes(self, mes:int, ano:int, tipo:str):
        dados = self.valorTotalDasCategorias(mes,ano,tipo)

        if not dados:
            return ('Nenhuma transação realizada','0.00'), ('Nenhuma transação realizada','0.00')

        categoria_maior, maior = max(dados.items(), key=lambda x: x[1])
        categoria_menor, menor = min(dados.items(), key=lambda x: x[1])
        return (categoria_maior,maior), (categoria_menor,menor)

    def mediaTransacoesMes(self, mes:int, ano:int):
        inicio_mes = Data.primeiroDiaMes(mes,ano)
        proximo_mes = Data.incrementarMes(inicio_mes).valor
        parcelas = ParcelasTransacao.todasParcelasMes(self.user, mes=mes, ano=ano)
        quantidade_dias = abs(proximo_mes - inicio_mes)
        return parcelas.count()/quantidade_dias.days

    def gastosPorDiaDaSemana(self, mes:int, ano:int):
        parcelas = ParcelasTransacao.todasParcelasMes(self.user, mes=mes, ano=ano)
        gastos = parcelas.filter(transacao_fk__tipo="D").annotate(dia_semana=ExtractWeekDay('data')).values('dia_semana').annotate(total=Sum('valor')).order_by('dia_semana')
        gastos = [(int(x['dia_semana']),x['total']) for x in gastos]
        valores,dias = ['0' for i in range(7)], [i for i in range(1,8)]
        for dia, total in gastos:
            valores[dia - 1] = str(total)

        dias = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
        return dias,valores
    def maiorTransacaoMes(self, mes, ano, tipo='receita'):
        parcelas = ParcelasTransacao.todasParcelasMes(self.user, mes=mes, ano=ano)
        maior = Decimal('0')
        if parcelas.count() <= 0:
            return maior
        if tipo[0].upper() == 'R':
            parcelas = parcelas.filter(transacao_fk__tipo='R')
        elif tipo[0].upper() == 'D':
            parcelas = parcelas.filter(transacao_fk__tipo='D')

        if parcelas:
            maior = parcelas.order_by('-valor').first().valor
        return maior

