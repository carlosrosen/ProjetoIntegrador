from django.contrib.auth.models import AbstractBaseUser
from django.utils.lorem_ipsum import paragraph

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

        self.__criarParcelas(transacao=transacao_objeto
                             , categoria=categoria_objeto
                             , data=data
                             , valor=valor
                             , quantidade_parcelas=quantidade_parcelas
                             , pago=pago
                             , tipo=tipo
        )

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
                historico = Historico(self.user)
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
                raise Exception(f'Erro ao criar o parcela {e} - ordem {i+1}')

            if pago.status and data.comparacaoDatasMenoresQueHoje(data_parcela):
                self.user.operarSaldoAtual(valor_parcela, tipo.valor)

    def editarUmaParcela(self
                         , parcela_id: int
                         , novo_valor: ValorTransacao
                         , nova_data: Data
                         , categoria: Categoria
                         , pago: Pago
                         , descricao: str
                         ):
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
        parcela.categoria_fk = categoria
        parcela.transacao_fk.descricao = descricao

        try:
            #por questão de tempo infelizmente não foi possivel otimizar o cancelamento da ação por questão de tempo
            parcela.save()
        except Exception as e:
            #caso tipo == despesa:
            valor_descancela = -valor_cancela
            if parcela.transacao_fk.tipo == 'R':
                valor_descancela = -valor_cancela

            #fazer as operações inversas vao cancelar o saldo adicionado e evitar erros com Saldo atual e o historico
            if pago_status_anterior == True and pago.status == True:
                # pago -> pago
                tipo_inverso = parcela.transacao_fk.tipo
                if tipo_inverso == 'R':
                    tipo_inverso = 'D'
                elif tipo_inverso == 'D':
                    tipo_inverso = 'R'
                self.user.editarSaldoAtualComTipo(valor_antigo=valor_antigo
                                                , valor_novo=novo_valor.valor
                                                , tipo=tipo_inverso
                )
                #cancela o novo valor
                if parcela.transacao_fk.tipo == 'R':
                    novo_valor.valor = -novo_valor.valor
                historico.corrigirValoresProximosMeses(data_transacao_editada=nova_data.valor
                                                       , valor_de_correcao=novo_valor.valor
                )
                #volta o valor original
                historico.corrigirValoresProximosMeses(data_transacao_editada=Data(parcela.data)
                                                     , valor_de_correcao=valor_descancela
                )
            elif pago_status_anterior == True and pago.status == False:
                # pago -> não pago
                self.user.operarSaldoAtual(valor=valor_antigo, tipo=parcela.transacao_fk.tipo)
                historico.corrigirValoresProximosMeses(data_transacao_editada=Data(parcela.data),
                                                       valor_de_correcao=valor_descancela)

            elif pago_status_anterior == False and pago.status == True:
                # não pago -> pago
                if parcela.transacao_fk.tipo == 'R':
                    novo_valor.valor = -novo_valor.valor
                #retira os novos valores
                self.user.operarSaldoAtualInverso(novo_valor.valor, parcela.transacao_fk.tipo)
                historico.corrigirValoresProximosMeses(data_transacao_editada=nova_data.valor,
                                                       valor_de_correcao=novo_valor.valor)
            raise Exception(f'Erro ao editar parcela')


    def deletarUmaParcela(self, parcela: ParcelasTransacao):
        transacao = parcela.transacao_fk
        self.user.operarSaldoAtualInverso(parcela.valor, transacao.tipo)
        historico = Historico(self.user)
        valor_cancela = parcela.valor
        if transacao.quantidade_parcelas == 1:
            if transacao.tipo == 'R':
                valor_cancela = -valor_cancela
            historico.corrigirValoresProximosMeses(data_transacao_editada=Data(parcela.data)
                                                 , valor_de_correcao=valor_cancela)

            transacao.delete()
        else:
            transacao.quantidade_parcelas -= 1
            transacao.save()
            parcela.delete()
            if transacao.quantidade_parcelas <= 0:
                transacao.delete()

    def deletarTodasParcelas(self,transacao: Transacao):
        parcelas = ParcelasTransacao.objects.filter(transacao_fk=transacao)
        historico = Historico(self.user)
        for parcela in parcelas:
            if not Data.comparacaoDatasMenoresQueHoje(parcela.data):
                continue
            valor_cancela = parcela.valor
            if transacao.tipo == 'R':
                valor_cancela = -valor_cancela
            historico.corrigirValoresProximosMeses(data_transacao_editada=Data(parcela.data)
                                                , valor_de_correcao=valor_cancela
            )
            self.user.operarSaldoAtualInverso(parcela.valor, transacao.tipo)

        transacao.delete()