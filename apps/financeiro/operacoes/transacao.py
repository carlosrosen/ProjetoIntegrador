from decimal import Decimal

from django.contrib.auth.models import AbstractBaseUser
from django.db import transaction

from apps.usuarios.models import CustomUser
from typing import Callable

from apps.financeiro.models import Transacao, ParcelasTransacao, Categoria, HistoricoSaldo

from apps.financeiro.dominio import *
from common.dominio.data import Data

from apps.financeiro.operacoes.saldo import Historico

from datetime import date


class OperacoesTransacao:
    def __init__(self, user_id):
        self.user = CustomUser.objects.get(id=user_id)

    def criar(self
              , valor: ValorTransacao
              , data: Data
              , tipo: Tipo
              , quantidade_parcelas: QuantidadeParcelas
              , descricao: str
              , pago: Pago
              , categoria : Categoria
              ):
        with transaction.atomic():
            transacao = Transacao.objects.create(user_fk= self.user
                                                , categoria_fk=categoria
                                                , tipo = tipo.valor
                                                , quantidade_parcelas = quantidade_parcelas.valor
                                                , descricao = descricao
            )
            try:
                self.__criarParcelas(transacao=transacao
                                     , data= data
                                     , valor= valor
                                     , quantidade_parcelas= quantidade_parcelas
                                     , status_pago= pago.status
                )
            except Exception as e:
                raise Exception(e)

    def __criarParcelas(self
                        , transacao: Transacao
                        , valor: ValorTransacao
                        , data: Data
                        , quantidade_parcelas: QuantidadeParcelas
                        , status_pago: bool
    ):
        valor_parcela = valor.valorParcela(quantidade_parcelas=quantidade_parcelas.valorDecimal)

        historico = Historico(self.user.id)
        for i in range(quantidade_parcelas.valor):
            try:
                data_parcela = Data(data.proximoMes(quantidade_meses=i))

                if data_parcela.valor > date.today():
                    status_pago = False

                parcela = ParcelasTransacao.objects.create(transacao_fk = transacao
                                                         , data = data_parcela.valor
                                                         , valor = abs(valor_parcela)
                                                         , ordem_parcela = i + 1
                                                         , pago = status_pago
                )
                if i == 0:
                    if not historico.inicializarTuplasParaParcelasAntigas(parcela=parcela) and not historico.inicializarTuplasParaParcelasFuturas(parcela=parcela):
                        historico.corrigirValoresHistorico(data_correcao_historico=data_parcela.valor
                                                           , valor_correcao=valor_parcela
                                                           ,inversor=False
                        )
                else:
                    historico.verificarExistenciaRegistro(parcela=parcela)
                    historico.corrigirValoresHistorico(data_correcao_historico= data_parcela.valor
                                                 , valor_correcao= valor_parcela
                                                 , inversor=False
                    )
                if status_pago == True and data_parcela.valor <= date.today():
                    self.user.operarSaldoAtual(valor_parcela, transacao.tipo, inversor=False)
            except Exception as e:
                transacao.delete()
                raise Exception(f'Erro ao criar o parcela {e}')

    # Função de editar a parcela (Quando a quantidade de parcelas for > 1)

    def __ajustarSaldoEHistoricoNaEdicaoDaTransacao(self
                                                    , historico: Historico
                                                    , tipo_transacao: str
                                                    , valor_anterior: Decimal
                                                    , valor_novo: Decimal
                                                    , pago_status_anterior: bool
                                                    , pago_status_novo: bool
                                                    , data_anterior_parcela: date
                                                    , data_nova: date
                                                    ):

        atualizar_valores_historico = lambda: historico.corrigirValoresHistorico(data_correcao_historico=data_nova
                                                                                 , valor_correcao=valor_novo
                                                                                 , inversor=False
                                                                                 )
        atualizar_valores_saldo = lambda: self.user.operarSaldoAtual(valor=valor_novo
                                                                     , tipo=tipo_transacao
                                                                     , inversor=False
                                                                     )
        cancelar_valores_historico = lambda: historico.corrigirValoresHistorico(
            data_correcao_historico=data_anterior_parcela
            , valor_correcao=valor_anterior
            , inversor=True
        )
        cancelar_valores_saldo = lambda: self.user.operarSaldoAtual(valor=valor_anterior
                                                                   , tipo=tipo_transacao
                                                                   , inversor=True
                                                                   )
        if pago_status_anterior == True and pago_status_novo == True:
            # pago -> pago

            # cancela o saldo de todos os registros a frente
            cancelar_valores_historico()
            # atualiza o saldo dos valores a frente da nova data
            atualizar_valores_historico()

            if data_anterior_parcela <= date.today() and data_nova <= date.today():
                # cancela os valores do saldo do valor antigo
                cancelar_valores_saldo()
                # atualiza os valores do novo saldo
                if data_nova <= self.user.dataUltimaTransacaoVerificada or data_nova > date.today():
                    atualizar_valores_saldo()

            elif data_anterior_parcela <= date.today() and data_nova > date.today():
                cancelar_valores_saldo()

            elif data_anterior_parcela > date.today() and data_nova <= date.today():
                if data_nova <= self.user.dataUltimaTransacaoVerificada or data_nova > date.today():
                    atualizar_valores_saldo()

        elif pago_status_anterior == True and pago_status_novo == False:
            # pago -> não pago
            if data_anterior_parcela <= date.today() and data_nova <= date.today():
                # cancela os valores antigos à frente e saldo do valor antigo
                cancelar_valores_historico()
                cancelar_valores_saldo()

            elif data_anterior_parcela <= date.today() and data_nova > date.today():
                cancelar_valores_historico()
                cancelar_valores_saldo()

        elif pago_status_anterior == False and pago_status_novo == True:
            # não pago -> pago
            if data_anterior_parcela <= date.today() and data_nova <= date.today():
                atualizar_valores_historico()
                #para evitar colisões com o verificador de transação paga,
                #so altera o valor se estiver fora do intevalo de checkagem do verificador
                if data_nova <= self.user.dataUltimaTransacaoVerificada or data_nova > date.today():
                    atualizar_valores_saldo()
            elif data_anterior_parcela > date.today() and data_nova <= date.today():
                atualizar_valores_historico()
                if data_nova <= self.user.dataUltimaTransacaoVerificada or data_nova > date.today():
                    atualizar_valores_saldo()

    def editarTransacaoParcelada(self
                        , parcela: ParcelasTransacao
                        , novo_valor: ValorTransacao
                        , pago: Pago
                        , descricao: str
                        ):
        if parcela.transacao_fk.quantidade_parcelas == 1:
            return
        with transaction.atomic():
            historico = Historico(self.user.id)
            self.__ajustarSaldoEHistoricoNaEdicaoDaTransacao(  historico=historico
                                                             , tipo_transacao=parcela.transacao_fk.tipo
                                                             , valor_anterior=parcela.valor
                                                             , valor_novo=novo_valor.valor
                                                             , pago_status_anterior=parcela.pago
                                                             , pago_status_novo=pago.status
                                                             , data_anterior_parcela=parcela.data
                                                             , data_nova=parcela.data
            )
            parcela.valor = novo_valor.valor
            parcela.pago = pago.status
            parcela.transacao_fk.descricao = descricao

            try:
                parcela.transacao_fk.save()
                parcela.save()
            except Exception:
                raise Exception(f'Erro ao editar parcela')


    def editarTransacaoUnica(self
                         , parcela: ParcelasTransacao
                         , novo_valor: ValorTransacao
                         , nova_data: Data
                         , categoria: Categoria
                         , pago: Pago
                         , descricao: str
                         ):
        if parcela.transacao_fk.quantidade_parcelas > 1:
            return None
        with transaction.atomic():

            historico = Historico(self.user.id)
            self.__ajustarSaldoEHistoricoNaEdicaoDaTransacao(  historico=historico
                                                             , tipo_transacao=parcela.transacao_fk.tipo
                                                             , valor_anterior=parcela.valor
                                                             , valor_novo=novo_valor.valor
                                                             , pago_status_anterior=parcela.pago
                                                             , pago_status_novo= pago.status
                                                             , data_anterior_parcela=parcela.data
                                                             , data_nova=nova_data.valor
            )

            parcela.valor = novo_valor.valor
            parcela.data = nova_data.valor
            parcela.pago = pago.status
            parcela.categoria_fk = categoria
            parcela.transacao_fk.descricao = descricao

            try:
                parcela.transacao_fk.save()
                parcela.save()
            except Exception as e:
                raise Exception(f'Erro ao editar parcela')


    # Aqui é pra deletar uma parcela
    def deletarUmaParcela(self, parcela: ParcelasTransacao):
        with transaction.atomic():
            transacao = parcela.transacao_fk
            historico = Historico(self.user.id)

            if parcela.data <= date.today() and parcela.pago == True:
                self.user.operarSaldoAtual(parcela.valor, transacao.tipo, inversor=True)

            if transacao.quantidade_parcelas <= 1:
                historico.corrigirValoresHistorico(data_correcao_historico= parcela.data
                                                  , valor_correcao= parcela.valor
                                                  , inversor=True
                )
                try:
                    transacao.delete()
                except Exception as e:
                    raise Exception(f'Erro deletar Transação')
            else:
                transacao.quantidade_parcelas -= 1
                if transacao.quantidade_parcelas > 0:
                    parcelas = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user
                                                              , transacao_fk=transacao
                                                              , ordem_parcela__gt=parcela.ordem_parcela
                    )
                    if parcelas.count() > 0:
                        for parcela_transacao in parcelas:
                            parcela_transacao.ordem_parcela -= 1
                            parcela_transacao.save()


                historico.corrigirValoresHistorico(data_correcao_historico=parcela.data
                                                   , valor_correcao=parcela.valor
                                                   , inversor=True
                )
                try:
                    transacao.save()
                    parcela.delete()
                except Exception as e:
                    raise Exception(f'Erro deletar parcela')

    # Aqui é pra deletar uma parcela e as próximas após ele
    def deletarProximasParcelas(self, parcela: ParcelasTransacao):
        with transaction.atomic():
            parcelas = ParcelasTransacao.objects.filter(
            transacao_fk=parcela.transacao_fk,
            ordem_parcela__gte=parcela.ordem_parcela
        ).order_by('ordem_parcela')
        for parcela in parcelas:
            self.deletarUmaParcela(parcela)

    # Aqui é para deletar todas
    def deletarTodasParcelas(self,parcela: ParcelasTransacao):
        with transaction.atomic():
            parcelas = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user ,transacao_fk=parcela.transacao_fk)
            historico = Historico(self.user.id)
            #cancela o valor do saldo e do historico
            for parcela in parcelas:
                if parcela.data > date.today():
                    continue
                self.user.operarSaldoAtual(parcela.valor, parcela.transacao_fk.tipo, inversor=True)

                historico.corrigirValoresHistorico(data_correcao_historico=parcela.data
                                                            , valor_correcao=parcela.valor
                                                            , inversor=True
                )
            try:
                parcela.transacao_fk.delete()
            except Exception as e:
                raise Exception(f'Erro inesperado ao deletar parcelas')

    def verificarParcelasPagas(self):
        with transaction.atomic():
            ultima_verificao = self.user.dataUltimaTransacaoVerificada
            if not ultima_verificao:
                self.user.dataUltimaTransacaoVerificada = date.today()
                return
            if ultima_verificao == date.today():
                return
            intervalo = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user
                                                       , data__gt=ultima_verificao
                                                       , data__lte=date.today()
                                                       , pago= True
            )

            if intervalo.count() == 0:
                return

            for parcela in intervalo:
                self.user.operarSaldoAtual(tipo=parcela.transacao_fk.tipo
                                         , valor=parcela.valor
                                         , inversor=False
                )

            self.user.dataUltimaTransacaoVerificada = intervalo.latest('data').data
            try:
                self.user.save()
            except Exception as e:
                raise Exception(f'Erro verificar parcelas pagas')