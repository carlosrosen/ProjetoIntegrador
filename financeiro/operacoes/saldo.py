from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Max, Min

from financeiro.dominio import *
from common.dominio.data import Data
from financeiro.models import ParcelasTransacao
from financeiro.models import HistoricoSaldo

from datetime import date
from decimal import Decimal

class Historico:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario Invalido.')
        self.user = user


    def verificarInsercoesHistorico(self,valor) -> None:
        if HistoricoSaldo.objects.filter(user=self.user).count() <= 0:
            HistoricoSaldo.inicializarPrimeiroValor(self.user)
            return
        mes_atual = Data.inicializar(dia=1, mes=date.today().month, ano=date.today().year)
        historico = HistoricoSaldo.objects.filter(user_fk=self.user)
        data_mais_recente = historico.aggregate(ultima_data=Max('data'))['ultima_data']
        insercao_mais_recente = historico.get(data=data_mais_recente)
        data_insercao_mais_recente = Data(data_mais_recente)

        if data_insercao_mais_recente.valor == mes_atual.valor:
            return

        while data_insercao_mais_recente.valor < mes_atual.valor:
            data_novo_registro = Data.incrementarMes(data_insercao_mais_recente.valor)
            intervalo = ParcelasTransacao.buscaIntervaloHistoricoSaldo(data_inicio=data_insercao_mais_recente.valor
                                                                     , data_fim=data_novo_registro.valor)

            if not intervalo.exists():
                data_insercao_mais_recente.valor = data_novo_registro.valor
                continue

            novo_valor = ValorTransacao(insercao_mais_recente.saldo)

            for parcela in intervalo:
                if parcela.transacao_fk.tipo == 'R':
                    novo_valor.valor += parcela.valor
                elif parcela.transacao_fk.tipo == 'D':
                    novo_valor.valor -= parcela.valor

            HistoricoSaldo.criarTupla(self.user, data_novo_registro.valor, novo_valor.valor)
            data_insercao_mais_recente.valor = data_novo_registro.valor

    def corrigirValoresProximosMeses(self,data_transacao_editada: Data, valor_de_correcao: Decimal) -> None:
        historico = HistoricoSaldo.objects.filter(user_fk=self.user, data__gt=data_transacao_editada)

        for tupla in historico:
            tupla.saldo += valor_de_correcao
            tupla.save()

    def inicializarTuplasParaParcelasAntigas(self,parcela: ParcelasTransacao) -> None:
        data_transacao = Data(parcela.data)
        mes, ano = data_transacao.valor.mes, data_transacao.valor.ano
        data = Data.inicializar(dia=1, mes=mes, ano=ano)
        historico = HistoricoSaldo.objects.filter(user_fk=self.user)
        data_insercao_mais_antiga = Data(historico.aggregate(primeira_data=Min('data'))['primeira_data'])

        if data.valor >= data_insercao_mais_antiga.valor:
            return

        while data.valor < data_insercao_mais_antiga.valor:
            HistoricoSaldo.criarTupla(user=self, saldo=Decimal('0'), data=data)
            data = data.incrementarMes(data)

        valor_correcao = ValorTransacao(parcela.valor)
        if parcela.transacao_fk.tipo == 'D':
            valor_correcao.valor = -valor_correcao.valor

        self.corrigirValoresProximosMeses(data_transacao, valor_correcao.valor)

    def pegarSaldoMes(self,mes:int, ano:int) -> list:
        mes, ano = abs(mes), abs(ano)
        data = Data.inicializar(dia=1,mes=mes, ano=ano)
        proxima_data = data.incrementarMes(data.valor)
        dados = []

        intervalo_parcelas = ParcelasTransacao.buscaIntervaloHistoricoSaldo(data_inicio=data.valor
                                                                          , data_fim=proxima_data
        )
        quantidade_dias = abs(proxima_data.valor - data.valor).days

        try:
            historico = HistoricoSaldo.objects.get(user_fk=self.user, data=data)
        except ObjectDoesNotExist:
            for dia in range(1,quantidade_dias+1):
                dados.append(0)
            return dados
        except MultipleObjectsReturned:
            raise IndexError('Ocorreu um erro inesperado com a busca do valores do saldo.')

        saldo = historico.saldo

        for dia in range(1, quantidade_dias+1):
            parcelas_dia = intervalo_parcelas.filter(data=date(day=dia,month=mes,year=ano))
            if not parcelas_dia.exists():
                dados.append(saldo)
                continue
            for parcela in parcelas_dia:
                if parcela.transacao_fk.tipo == 'R':
                    saldo += parcela.valor
                elif parcela.transacao_fk.tipo == 'D':
                    saldo -= parcela.valor

            dados.append(saldo)
        return dados

    def pegarSaldoAno(self,ano: int) -> list:
        ano = abs(ano)
        dados = []
        for mes in range(1,13):
            dados.extend(self.pegarSaldoMes(mes=mes,ano=ano))
        return dados