from django.contrib.auth.models import AbstractBaseUser
from django.db import transaction

from financeiro.models import Transacao, ParcelasTransacao, Categoria

from financeiro.dominio import *
from common.dominio.data import Data

from financeiro.operacoes.saldo import Historico
class OperacoesTransacao:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario invalido')
        self.user = user

    def criar(self
              , valor: ValorTransacao
              , data: Data
              , tipo: Tipo
              , quantidade_parcelas: QuantidadeParcelas
              , descricao: str
              , pago: Pago
              , categoria_objeto : Categoria
              ):

        transacao_objeto = Transacao.objects.create(user_fk= self.user
                                                    , tipo = tipo.valor
                                                    , quantidade_parcelas = quantidade_parcelas.valor
                                                    , descricao = descricao
        )
        with transaction.atomic():
            try:
                self.__criarParcelas(transacao=transacao_objeto
                                     , categoria=categoria_objeto
                                     , data=data
                                     , valor=valor
                                     , quantidade_parcelas=quantidade_parcelas
                                     , pago=pago
                                     , tipo=tipo
                )
            except Exception as e:
                raise Exception('Falha inesperada ao criar Transação')


    def __criarParcelas(self
                        , transacao: Transacao
                        , categoria: Categoria
                        , valor:ValorTransacao
                        , data:Data
                        , quantidade_parcelas: QuantidadeParcelas
                        , pago: Pago
                        , tipo:Tipo
    ):
        valor_parcela = valor.valorParcela(quantidade_parcelas=quantidade_parcelas.valorDecimal)

        historico = Historico(self.user)
        for i in range(quantidade_parcelas.valor):
            try:
                data_parcela = data.proximoMes(quantidade_meses=i)

                parcela = ParcelasTransacao.objects.create(transacao_fk = transacao
                                                         , categoria_fk=categoria
                                                         , data = data_parcela
                                                         , valor = abs(valor_parcela)
                                                         , ordem_parcela = i + 1
                                                         , pago = pago.status
                )
                if i == 0:
                    historico.inicializarTuplasParaParcelasAntigas(parcela=parcela)

                valor_correcao = valor_parcela
                if transacao.tipo == 'D':
                    valor_correcao = -valor_parcela

                historico.corrigirValoresProximosMeses(data_transacao_editada=data_parcela
                                                     , valor_de_correcao=valor_correcao
                )

            except Exception as e:
                transacao.delete()
                raise Exception(f'Erro ao criar o parcela')

            if pago.status and data.comparacaoDatasMenoresQueHoje(data_parcela):
                self.user.operarSaldoAtual(valor_parcela, tipo.valor)

    #CORRIGIR ALTERAÇÃO DE VALORES COM AS DEVIDAS DATAS
    def editarUmaParcela(self
                         , parcela_id: int
                         , novo_valor: ValorTransacao
                         , nova_data: Data
                         , categoria: Categoria
                         , pago: Pago
                         , descricao: str
                         ):
        with transaction.atomic():
            parcela = ParcelasTransacao.objects.get(id=int(parcela_id))

            pago_status_anterior = parcela.pago
            valor_antigo = parcela.valor

            historico = Historico(self.user)
            #caso tipo == despesa
            valor_cancela = parcela.valor
            if parcela.transacao_fk.tipo == 'R':
                valor_cancela = -parcela.valor

            if  pago_status_anterior == True and pago.status == True:
                #pago -> pago
                self.user.editarSaldoAtualComTipo(valor_antigo=valor_antigo
                                                , valor_novo=novo_valor.valor
                                                , tipo=parcela.transacao_fk.tipo
                )
                #cancela os valores antigos à frente
                historico.corrigirValoresProximosMeses(data_transacao_editada=Data(parcela.data)
                                                     , valor_de_correcao=valor_cancela
                )
                #atualiza os novos valores
                if parcela.transacao_fk.tipo == 'D':
                    novo_valor.valor = -novo_valor.valor
                historico.corrigirValoresProximosMeses(data_transacao_editada=nova_data.valor
                                                     , valor_de_correcao=novo_valor.valor)
            elif pago_status_anterior == True and pago.status == False:
                #pago -> não pago
                self.user.operarSaldoAtualInverso(valor=valor_antigo, tipo=parcela.transacao_fk.tipo)
                #so cancela os valores antigos ate a frente
                historico.corrigirValoresProximosMeses(data_transacao_editada=Data(parcela.data)
                                                       , valor_de_correcao=valor_cancela
                )
            elif pago_status_anterior == False and pago.status == True:
                #não pago -> pago
                self.user.operarSaldoAtual(novo_valor.valor, parcela.transacao_fk.tipo)
                if parcela.transacao_fk.tipo == 'D':
                    novo_valor.valor = -novo_valor.valor
                #so atualiza os novos valores
                historico.corrigirValoresProximosMeses(data_transacao_editada=nova_data.valor
                                                     , valor_de_correcao=novo_valor.valor
                )

            if novo_valor.valor < 0:
                novo_valor.valor = -novo_valor.valor

            parcela.valor = novo_valor.valor
            parcela.data = nova_data.valor
            parcela.pago = pago.status
            if parcela.transacao_fk.quantidade_parcelas == 1:
                parcela.categoria_fk = categoria
            parcela.transacao_fk.descricao = descricao

            try:
                parcela.save()
            except Exception as e:
                raise Exception(f'Erro ao editar parcela')


    def deletarUmaParcela(self, parcela: ParcelasTransacao):
        transacao = parcela.transacao_fk
        self.user.operarSaldoAtualInverso(parcela.valor, transacao.tipo)
        historico = Historico(self.user)
        with transaction.atomic():
            valor_cancela = parcela.valor
            if transacao.quantidade_parcelas == 1:
                if transacao.tipo == 'R':
                    valor_cancela = -valor_cancela
                historico.corrigirValoresProximosMeses(data_transacao_editada=Data(parcela.data)
                                                     , valor_de_correcao=valor_cancela
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
            if transacao.quantidade_parcelas <= 0:
                try:
                    transacao.delete()
                except Exception as e:
                    raise Exception(f'Erro deletar transção')

    def deletarTodasParcelas(self,transacao: Transacao):
        with transaction.atomic():
            parcelas = ParcelasTransacao.objects.filter(transacao_fk=transacao)
            historico = Historico(self.user)
            #cancela o valor do saldo e do historico
            for parcela in parcelas:
                if not Data.comparacaoDatasMenoresQueHoje(parcela.data):
                    continue
                self.user.operarSaldoAtualInverso(parcela.valor, transacao.tipo)

                valor_cancela = parcela.valor
                if transacao.tipo == 'R':
                    valor_cancela = -valor_cancela
                historico.corrigirValoresProximosMeses(data_transacao_editada=Data(parcela.data)
                                                     , valor_de_correcao=valor_cancela
                )

            try:
                transacao.delete()
            except Exception as e:
                raise Exception(f'Erro inesperado ao deletar parcelas')

    def verificarParcelasPagas(self, parcela: ParcelasTransacao):
        if parcela.transacao_fk.quantidade_parcelas <= 1:
            return
        with transaction.atomic():
            pass