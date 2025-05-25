from django.contrib.auth.models import AbstractBaseUser

from financeiro.dominio import *
from common.dominio.data import Data
from financeiro.dominio import tipo
from financeiro.models import Categoria, ParcelasTransacao, Transacao


class InformacoesTransacao:
    def __init__(self, user, **kwargs):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario Invalido')
        self.user = user

        self.operacao = kwargs.get('operacao')

        self.transacao = kwargs.get('transacao')
        self.parcela = kwargs.get('parcela')
        self.valor = kwargs.get('valor')
        self.data = kwargs.get('data')
        self.tipo = kwargs.get('tipo')
        self.quantidade_parcelas = kwargs.get('quantidade_parcelas')
        self.descricao = kwargs.get('descricao')
        self.pago = kwargs.get('pago')
        self.categoria = kwargs.get('categoria')
