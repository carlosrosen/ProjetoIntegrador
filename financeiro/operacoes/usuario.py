from django.contrib.auth.models import AbstractBaseUser

from financeiro.dominio import tipo
from financeiro.models import Transacao, ParcelasTransacao, Categoria

from financeiro.dominio.tipo import Tipo
from financeiro.dominio.data import Data
from financeiro.dominio.valor import Valor
from financeiro.dominio.pago import Pago
from financeiro.dominio.quantidadeparcelas import QuantidadeParcelas

class OperacoesTransacao:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario invalido')
        self.user = user

    def criar(self
              , valor:str
              , data: str
              , valor_tipo:str
              , quantidade_parcelas:str
              , descricao:str
              , pago:str
              , categoria:str
              ):
        #Formatação dos dados
        tipo = Tipo(valor_tipo)
        data =  Data(data)
        valor = Valor(valor)
        pago = Pago(pago)
        quantidade_parcelas = QuantidadeParcelas(quantidade_parcelas)

        categoria_objeto = Categoria.verificacao_nomes(categoria)

        transacao_objeto = Transacao.objects.create(user_fk= self.user
                                                    , categoria_fk = categoria_objeto
                                                    , tipo = tipo.valor
                                                    , quantidade_parcelas = quantidade_parcelas.valor
                                                    , descricao = descricao
        )

        self.__criarParcelas(transacao=transacao_objeto
                             , data=data
                             , valor=valor.valor
                             , quantidade_parcelas=quantidade_parcelas
                             , pago=pago
                             , tipo=tipo
        )

    def __criarParcelas(self
                        , transacao: Transacao
                        , valor:Valor
                        , data:Data
                        , quantidade_parcelas: QuantidadeParcelas
                        , pago: Pago
                        , tipo:Tipo
    ):

        valor_parcela = valor.valorParcela(quantidade_parcelas=quantidade_parcelas.valorDecimal),

        for i in range(quantidade_parcelas.valor):
            try:
                data_parcela = data.somarMes(quantidade_meses=i)
                ParcelasTransacao.objects.create(transacao_fk = transacao
                                                , data = data_parcela
                                                , valor = valor_parcela
                                                , ordem_parcela = i + 1
                                                , pago = pago.status
                )
            except Exception as e:
                raise Exception('Erro ao criar o parcela')

            if pago.status and data.comparacaoDatasMenoresQueHoje(data_parcela):
                if tipo.valor == 'R':
                    self.user.saldoAtual += valor_parcela
                else:
                    self.user.saldoAtual -= valor_parcela
                self.user.save()

    def editarUmaParcela(self
                         , parcela_id: str
                         , valor: str
                         , data: str
                         , categoria: str
                         , sub_categoria: str
                         , pago: str
                         , descricao: str
                         ):
        parcela = ParcelasTransacao.objects.get(id=int(parcela_id))
        valor = Valor(valor)
        data = Data(data)
        categoria = Categoria.verificacaoNomesCategoria(categoria)
        sub_categoria = Categoria.verificacaoNomesSubCategoria(sub_categoria)
        pago = Pago(pago)

        pago_status_anterior = parcela.pago
        valor_antigo = parcela.valor

        try:
            parcela.valor = valor.valor
            parcela.data = data.valor
            parcela.categoria = categoria
            parcela.sub_categoria = sub_categoria
            parcela.pago = pago.status
            parcela.Transacao.descricao = descricao
        except Exception as e:
            raise Exception('Erro ao editar parcela')


        if  pago_status_anterior == True and pago.status == True:
            #pago -> pago
            if parcela.Transacao.tipo == 'R':
                self.user.editarReceita(valor_antigo, valor.valor)
            else:
                self.user.editarDespesa(valor_antigo, valor.valor)
        elif pago_status_anterior == True and pago.status == False:
            #pago -> não pago
            if parcela.Transacao.tipo == 'R':
                self.user.subtrairSaldoAtual(valor.valor)
            else:
                self.user.somarSaldoAtual(valor.valor)
        elif pago_status_anterior == False and pago.status == True:
            #não pago -> pago
            if parcela.Transacao.tipo == 'R':
                self.user.somarSaldoAtual(valor.valor)
            else:
                self.user.subtrairSaldoAtual(valor.valor)
        parcela.save()