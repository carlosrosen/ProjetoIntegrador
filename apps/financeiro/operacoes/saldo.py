
from apps.usuarios.models import CustomUser

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Max, Min, Sum

from apps.financeiro.dominio import *
from common.dominio.data import Data
from apps.financeiro.models import ParcelasTransacao, Categoria
from apps.financeiro.models import HistoricoSaldo

from datetime import date
from decimal import Decimal, ROUND_DOWN



class Historico:
    def __init__(self, user_id):
        self.user= CustomUser.objects.get(id=user_id)


    def verificarInsercoesHistorico(self) -> None:
        if HistoricoSaldo.objects.filter(user_fk=self.user).count() <= 0:
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
            intervalo = ParcelasTransacao.buscaParcelasIntervalo(user=self.user
                                                                , data_inicio=data_insercao_mais_recente.valor
                                                                , data_fim=data_novo_registro.valor
            )

            if not intervalo.exists():
                data_insercao_mais_recente.valor = data_novo_registro.valor
                HistoricoSaldo.criarTupla(user=self.user, data=data_novo_registro.valor, saldo=insercao_mais_recente.saldo)
                continue

            novo_valor = ValorTransacao(insercao_mais_recente.saldo)

            for parcela in intervalo:
                if parcela.transacao_fk.tipo == 'R':
                    novo_valor.valor += parcela.valor
                elif parcela.transacao_fk.tipo == 'D':
                    novo_valor.valor -= parcela.valor

            HistoricoSaldo.criarTupla(self.user, data_novo_registro.valor, novo_valor.valor)
            data_insercao_mais_recente.valor = data_novo_registro.valor

    def corrigirValoresHistorico(self
                                 , data_correcao_historico: date
                                 , valor_correcao: Decimal
                                 , inversor: bool = False
                                 ) -> None:
        historico = HistoricoSaldo.objects.filter(user_fk=self.user, data__gt=data_correcao_historico)

        if inversor == True:
            valor_correcao = -valor_correcao

        for tupla in historico:
            tupla.saldo += valor_correcao
            tupla.save()


    def inicializarTuplasParaParcelasAntigas(self, parcela: ParcelasTransacao) -> bool:
        data_transacao = Data(parcela.data)
        mes, ano = data_transacao.valor.month, data_transacao.valor.year
        data = Data.inicializar(dia=1, mes=mes, ano=ano)
        historico = HistoricoSaldo.objects.filter(user_fk=self.user)
        data_insercao_mais_antiga = Data(historico.aggregate(primeira_data=Min('data'))['primeira_data'])

        if data.valor >= data_insercao_mais_antiga.valor:
            return False

        while data.valor < data_insercao_mais_antiga.valor:
            HistoricoSaldo.criarTupla(user=self.user, saldo=Decimal('0.0'), data=data.valor)
            data = data.incrementarMes(data.valor)

        self.user.operarSaldoAtual(valor=parcela.valor, tipo=parcela.transacao_fk.tipo, inversor=True)

        self.corrigirValoresHistorico(data_correcao_historico= parcela.data
                                    , valor_correcao= parcela.valor
                                    , inversor=False
        )
        return True
    def inicializarTuplasParaParcelasFuturas(self, parcela: ParcelasTransacao) -> bool:
        data_transacao = Data(parcela.data)
        mes, ano = data_transacao.valor.month, data_transacao.valor.year
        data = Data.inicializar(dia=1, mes=mes, ano=ano)
        registro_mais_recente = HistoricoSaldo.objects.filter(user_fk=self.user).order_by('-data').first()
        data_historico_mais_recente = Data(registro_mais_recente.data)
        if data_historico_mais_recente.valor >= data.valor:
            return False

        saldo = registro_mais_recente.saldo

        while data_historico_mais_recente.valor <= data.valor:
            mes_seguinte = Data.incrementarMes(data_historico_mais_recente.valor)
            parcelas_mes = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user
                                                            , data__gte=data_historico_mais_recente.valor
                                                            , data__lt=mes_seguinte.valor
            )
            if parcelas_mes.count() <= 0:
                HistoricoSaldo.criarTupla(self.user,data.valor,saldo)
                data_historico_mais_recente = Data.incrementarMes(data_historico_mais_recente.valor)
                continue

            for parcela in parcelas_mes:
                if parcela.transacao_fk.tipo == 'R':
                    saldo += parcela.valor
                elif parcela.transacao_fk.tipo == 'D':
                    saldo -= parcela.valor

            data_historico_mais_recente = mes_seguinte
            HistoricoSaldo.criarTupla(self.user,mes_seguinte.valor,saldo)
        return True

    def verificarExistenciaRegistro(self, parcela: ParcelasTransacao) -> None:
        historico_mais_recente = HistoricoSaldo.objects.filter(user_fk=self.user).order_by('-data').first()
        data_parcela_inicializada = Data.inicializar(dia=1,mes=parcela.data.month,ano=parcela.data.year).valor
        saldo = historico_mais_recente.saldo
        if parcela.transacao_fk.tipo == 'R':
            saldo += parcela.valor
        elif parcela.transacao_fk.tipo == 'D':
            saldo -= parcela.valor
        if historico_mais_recente.data < data_parcela_inicializada:
            HistoricoSaldo.criarTupla(self.user,data_parcela_inicializada,saldo)