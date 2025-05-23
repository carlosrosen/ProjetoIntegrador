from django.contrib.auth.models import AbstractBaseUser

from financeiro.dominio import tipo
from financeiro.models import Transacao, ParcelasTransacao, Categoria

from financeiro.dominio.tipo import Tipo
from financeiro.dominio.data import Data
from financeiro.dominio.valortransacao import Valor
from financeiro.dominio.pago import Pago
from financeiro.dominio.quantidadeparcelas import QuantidadeParcelas

class OperacoesTransacao:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario invalido')
        self.user = user

    def criar(self
              , valor: Valor
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
                        , valor:Valor
                        , data:Data
                        , quantidade_parcelas: QuantidadeParcelas
                        , pago: Pago
                        , tipo:Tipo
    ):
        valor_parcela = valor.valorParcela(quantidade_parcelas=quantidade_parcelas.valorDecimal)

        for i in range(quantidade_parcelas.valor):
            try:
                data_parcela = data.somarMes(quantidade_meses=i)
                ParcelasTransacao.objects.create(transacao_fk = transacao
                                                 , categoria_fk=categoria
                                                 , data = data_parcela
                                                 , valor = valor_parcela
                                                 , ordem_parcela = i + 1
                                                 , pago = pago.status
                )
            except Exception as e:
                transacao.delete()
                raise Exception(f'Erro ao criar o parcela {e} - ordem {i+1}')

            if pago.status and data.comparacaoDatasMenoresQueHoje(data_parcela):
                self.user.operarSaldoAtual(valor_parcela, tipo.status)

    def editarUmaParcela(self
                         , parcela_id: int
                         , valor: Valor
                         , data: Data
                         , categoria: Categoria
                         , pago: Pago
                         , descricao: str
                         ):
        parcela = ParcelasTransacao.objects.get(id=int(parcela_id))

        pago_status_anterior = parcela.pago
        valor_antigo = parcela.valor

        try:
            parcela.valor = valor.valor
            parcela.data = data.valor
            parcela.pago = pago.status
            parcela.categoria_fk = categoria
            parcela.transacao_fk.descricao = descricao
        except Exception as e:
            raise Exception(f'Erro ao editar parcela {e}')

        if  pago_status_anterior == True and pago.status == True:
            #pago -> pago
            self.user.editarSaldoAtualComTipo(valor_antigo=valor_antigo
                                              , valor_novo=valor.valor
                                              , tipo=parcela.transacao_fk.tipo
            )
        elif pago_status_anterior == True and pago.status == False:
            #pago -> não pago
            self.user.operarSaldoAtualInverso(valor_antigo, parcela.transacao_fk.tipo)
        elif pago_status_anterior == False and pago.status == True:
            #não pago -> pago
            self.user.operarSaldoAtual(valor.valor, parcela.transacao_fk.tipo)
        parcela.save()

    def deletarUmaParcela(self, parcela: ParcelasTransacao):
        transacao = parcela.transacao_fk
        self.user.operarSaldoAtualInverso(parcela.valor, transacao.tipo)
        if transacao.quantidade_parcelas == 1:
            transacao.delete()
        else:
            transacao.quantidade_parcelas -= 1
            transacao.save()
            parcela.delete()
            if transacao.quantidade_parcelas <= 0:
                transacao.delete()

    def deletarTodasParcelas(self,transacao: Transacao):
        parcelas = ParcelasTransacao.objects.filter(transacao_fk=transacao)
        for parcela in parcelas:
            if not Data.comparacaoDatasMenoresQueHoje(parcela.data):
                continue
            self.user.operarSaldoAtualInverso(parcela.valor, transacao.tipo)

        transacao.delete()