from django.contrib.auth.models import AbstractBaseUser
from django.db import transaction

from apps.usuarios.models import CustomUser
from typing import cast

from apps.financeiro.models import Transacao, ParcelasTransacao, Categoria

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
        valor_parcela = valor.valorParcela(quantidade_parcelas= quantidade_parcelas.valorDecimal)

        historico = Historico(self.user.id)
        for i in range(quantidade_parcelas.valor):
            try:
                data_parcela = Data(data.proximoMes(quantidade_meses=i))

                parcela = ParcelasTransacao.objects.create(transacao_fk = transacao
                                                         , data = data_parcela.valor
                                                         , valor = abs(valor_parcela)
                                                         , ordem_parcela = i + 1
                                                         , pago = status_pago
                )
                if i == 0:
                    historico.inicializarTuplasParaParcelasAntigas(parcela=parcela)
                else:
                    historico.corrigirValoresHistorico(data_correcao_historico= data_parcela.valor
                                                 , valor_correcao= valor_parcela
                                                 , inversor=False
                    )
                if status_pago and data.valor <= date.today():
                    self.user.operarSaldoAtual(valor_parcela, transacao.tipo, inversor=False)

            except Exception as e:
                transacao.delete()
                raise Exception(f'Erro ao criar o parcela {e}')

    # Função de editar a parcela (Quando a quantidade de parcelas for > 1)
    def editarUmaParcela(self
                         , parcela: ParcelasTransacao
                         , novo_valor: ValorTransacao
                         , nova_data: Data
                         , categoria: Categoria  # Categoria não pode ser mais editada
                         , pago: Pago
                         , descricao: str
                         ):
        with transaction.atomic():
            if parcela.transacao_fk.quantidade_parcelas > 1:
                parcela.pago = pago.status
                parcela.descricao = descricao
                return

            pago_status_anterior = parcela.pago
            valor_antigo = parcela.valor
            data_antiga_parcela = parcela.data

            historico = Historico(self.user)

            atualizar_valores_historico = lambda: historico.corrigirValoresHistorico(data_correcao_historico= nova_data.valor
                                                                                   , valor_correcao= novo_valor.valor
                                                                                   , inversor=False
            )
            atualizar_valores_saldo = lambda: self.user.operarSaldoAtual(valor=novo_valor.valor
                                                                       , tipo=parcela.transacao_fk.tipo
                                                                       , inversor= False
            )
            cancelar_valores_historico = lambda: historico.corrigirValoresHistorico(data_correcao_historico= data_antiga_parcela
                                                                                  , valor_correcao= valor_antigo
                                                                                  , inversor=True
            )
            cancela_valores_saldo = lambda: self.user.operarSaldoAtual(valor=valor_antigo
                                                                     , tipo=parcela.transacao_fk.tipo
                                                                     , inversor=True
            )

            if  pago_status_anterior == True and pago.status == True:
                #pago -> pago

                #cancela o saldo de todos os registros a frente
                cancelar_valores_historico()
                #atualiza o saldo dos valores a frente da nova data
                atualizar_valores_historico()

                if data_antiga_parcela <= date.today() and nova_data.valor <= date.today():
                    #cancela os valores do saldo do valor antigo
                    cancela_valores_saldo()
                    #atualiza os valores do novo saldo
                    atualizar_valores_saldo()

                elif data_antiga_parcela <= date.today() and nova_data.valor > date.today():
                    cancela_valores_saldo()

                elif data_antiga_parcela > date.today() and nova_data.valor <= date.today():
                    atualizar_valores_saldo()

            elif pago_status_anterior == True and pago.status == False:
                #pago -> não pago
                if  data_antiga_parcela <= date.today() and nova_data.valor <= date.today():
                # cancela os valores antigos à frente e saldo do valor antigo
                    cancelar_valores_historico()
                    cancela_valores_saldo()

                elif data_antiga_parcela <= date.today() and nova_data.valor > date.today():
                    cancelar_valores_historico()
                    cancela_valores_saldo()

            elif pago_status_anterior == False and pago.status == True:
                #não pago -> pago
                if data_antiga_parcela <= date.today() and nova_data.valor <= date.today():
                    atualizar_valores_historico()
                    atualizar_valores_saldo()
                elif data_antiga_parcela > date.today() and nova_data.valor <= date.today():
                    atualizar_valores_historico()
                    atualizar_valores_saldo()

            parcela.valor = novo_valor.valor
            parcela.data = nova_data.valor
            parcela.pago = pago.status
            parcela.categoria_fk = categoria
            parcela.transacao_fk.descricao = descricao

            try:
                parcela.save()
            except Exception as e:
                raise Exception(f'Erro ao editar parcela')


    # Voce colocou para corrigir o valor do saldo quando a quantidade de parcelas fosse apenas uma

    def deletarUmaParcela(self, parcela: ParcelasTransacao):
        with transaction.atomic():
            transacao = parcela.transacao_fk
            historico = Historico(self.user)
            self.user.operarSaldoAtual(parcela.valor, transacao.tipo, inversor=True)
            if transacao.quantidade_parcelas == 1:
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
                try:
                    transacao.save()
                    parcela.delete()
                except Exception as e:
                    raise Exception(f'Erro deletar parcela')

    def deletarProximasParcelas(self, parcela: ParcelasTransacao):
        with transaction.atomic():
            parcelas = ParcelasTransacao.objects.filter(
            parcela__transacao_fk=parcela.transacao_fk,
            ordem_parcela__gte=parcela.ordem_parcela
        ).order_by('ordem_parcela')
        
        for parcela in parcelas:
            self.deletarUmaParcela(parcela)

    def deletarTodasParcelas(self,parcela: ParcelasTransacao):
        with transaction.atomic():
            parcelas = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user ,transacao_fk=parcela.transacao_fk)
            historico = Historico(self.user)
            #cancela o valor do saldo e do historico
            for parcela in parcelas:
                if parcela.data > date.today():
                    continue
                self.user.operarSaldoAtual(parcela.valor, parcela.transacao_fk.tipo, inversor=True)

                historico.corrigirValoresHistorico(data_correcao_historico=parcela.data
                                                            , valor_correcao=parcela.valor
                                                            , inversor=True
                )
                self.user.operarSaldoAtual(valor=parcela.valor
                                           , tipo=parcela.transacao_fk.tipo
                                           , inversor=True
                )

            try:
                parcela.transacao_fk.delete()
            except Exception as e:
                raise Exception(f'Erro inesperado ao deletar parcelas')

    def verificarParcelasPagas(self):
        with transaction.atomic():
            ultima_verificao = self.user.dataUltimaTransacaoVerificada
            if ultima_verificao == date.today():
                return
            intervalo = ParcelasTransacao.objects.filter(transacao_fk__user_fk=self.user
                                                       , data__gt=ultima_verificao
                                                       , data__lte=date.today()
                                                       , pago= True
            )

            for parcela in intervalo:
                self.user.operarSaldoAtual(tipo=parcela.transacao_fk.tipo
                                         , valor=parcela.valor
                                         , inversor=False
                )

            self.user.dataUltimaTransacaoVerificada = intervalo.latest('data')
            try:
                self.user.save()
            except Exception as e:
                raise Exception(f'Erro verificar parcelas pagas')