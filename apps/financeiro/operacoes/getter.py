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
        data = Data.inicializar(dia=1,mes=mes, ano=ano)
        proxima_data = data.incrementarMes(data.valor)
        dados = []
        dias = []

        intervalo_parcelas = ParcelasTransacao.buscaParcelasIntervalo(user=self.user
                                                                      , data_inicio=data.valor
                                                                      , data_fim=proxima_data
        )
        quantidade_dias = abs(proxima_data.valor - data.valor).days

        try:
            historico = HistoricoSaldo.objects.get(user_fk=self.user, data=data)
        except ObjectDoesNotExist:
            for dia in range(1,quantidade_dias+1):
                dados.append('0')
                dia = str(dia)
                if len(dia) == 1:
                    dia = '0'+dia
                dias.append(dia)
            return dados, dias
        except MultipleObjectsReturned:
            raise IndexError('Ocorreu um erro inesperado com a busca do valores do saldo.')

        saldo = historico.saldo

        for dia in range(1, quantidade_dias+1):
            parcelas_dia = intervalo_parcelas.filter(data=date(day=dia,month=mes,year=ano))
            if not parcelas_dia.exists():
                dados.append(saldo)
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
        if tipo[0].lower() == 'r':
            tipo = 'receita'
        elif tipo[0].lower() == 'd':
            tipo = 'despesa'
        inicio_mes = Data.inicializar(1,mes,ano)
        inicio_proximo_mes = Data.incrementarMes(inicio_mes.valor)
        categorias = Categoria.objects.all()
        parcelas_mes = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user
                                                       , data__gte=inicio_mes.valor
                                                       , data__lt=inicio_proximo_mes.valor
                                                       )
        if tipo.lower() == 'receita':
            parcelas_mes = parcelas_mes.filter(transacao_fk__tipo='R')
            categorias = categorias.filter(tipo='R')
        elif tipo.lower() == 'despesa':
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
        inicio_proximo_mes = Data.incrementarMes(inicio_mes.valor).valor
        parcelas = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user
                                                     , data__gte=inicio_mes.valor
                                                     , data__lt= inicio_proximo_mes.valor
        )
        quantidade_dias = abs(inicio_proximo_mes.valor - inicio_mes.valor)

        dados = []
        for dia in range(1,quantidade_dias+1):
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
        receita = self.valorTotalDasCategorias(mes,ano,'receita')
        despesa = self.valorTotalDasCategorias(mes,ano,'despesa')
        categoria_maior = list(receita.keys())[0]
        categoria_menor = list(despesa.keys())[0]
        maior = list(receita.values())[0]
        menor = list(despesa.values())[0]
        if tipo[0].upper() == 'R':
            menor = maior
            categoria_menor = categoria_maior
            for categoria, total in receita:
                if total > maior: maior, categoria_maior = total, categoria_maior
                if total < menor: menor, categoria_menor = total, categoria_menor
        elif tipo[0].upper() == 'D':
            categoria_maior = categoria_menor
            maior = menor
            for categoria, total in despesa:
                if total > maior: maior, categoria_maior = total, categoria_maior
                if total < menor: menor, categoria_menor = total, categoria_menor
        return (categoria_maior,maior), (categoria_menor,menor)

    def mediaTransacoesMes(self, mes:int, ano:int):
        inicio_mes = Data.inicializar(1,mes,ano)
        proximo_mes = Data.incrementarMes(inicio_mes.valor)
        parcelas = ParcelasTransacao.buscaParcelasIntervalo(self.user, inicio_mes.valor, proximo_mes.valor)
        quantidade_dias = abs(proximo_mes.valor - proximo_mes.valor)
        return parcelas.count()/quantidade_dias

    def gastosPorDiaDaSemana(self, mes:int, ano:int):
        inicio_mes = Data.primeiroDiaMes(mes, ano)
        proximo_mes = Data.incrementarMes(inicio_mes.valor)
        parcelas = ParcelasTransacao.buscaParcelasIntervalo(self.user, inicio_mes.valor, proximo_mes.valor)
        return parcelas.filter(tipo="D").annotate(dia_semana=ExtractWeekDay('data')).values('dia_semana').annotate(total=Sum('valor')).order_by('dia_semana')
