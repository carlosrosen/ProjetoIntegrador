from apps.metas.models import Metas
from apps.financeiro.models import ParcelasTransacao, Categoria

from django.contrib.auth.models import AbstractBaseUser
from apps.usuarios.models import CustomUser
from typing import cast

from django.db.models import Sum

from common.dominio.data import Data
from decimal import Decimal
from datetime import date



class Meta:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario invalido')
        self.user = cast(CustomUser,user)

    def criarMeta(
            self,
            categoria: Categoria,
            tipo: str,
            valor: Decimal,
            data_inicio: Data,
            data_fim: Data,
            descricao: str
    ):
        # Tem que formatar os valores certinhos aqui no parametro

        if tipo not in ['MAX', 'MIN']:
            return "Tipo de meta inválido. Use 'MAX' para limite máximo ou 'MIN' para mínimo desejado."
        if data_fim < data_inicio:
            return "A data final não pode ser anterior à data inicial."
        if valor <= 0:
            return "Valor inserido menor que zero"

        Metas.objects.create(
            user_fk=self.user,
            tipo=tipo,
            categoria=categoria.id,
            valor=valor,
            data_inicio=data_inicio,
            data_fim=data_fim,
            descricao=descricao
        )

    def editarMeta(
            self,
            meta: Metas,
            categoria: str,
            tipo: str,
            valor: Decimal,
            data_inicio: Data,
            data_fim: Data,
            descricao: str,
    ):
        if not meta.status == 'A':
            return

        if data_fim.valor < data_inicio.valor:
            return "A data final não pode ser anterior à data inicial."
        elif data_fim.valor < meta.data_inicio:
            return "A data final não pode ser anterior à data inicial."

        meta.data_fim = data_fim
        meta.categoria = categoria
        meta.tipo = tipo
        meta.valor = valor
        meta.data_inicio = data_inicio.valor
        meta.descricao = descricao
        meta.save()

    def deletarMeta(self, meta: Metas):
        meta.delete()

    def atualizarStatusMeta(self, meta: Metas):
        # Se o status não for ativo ele não atualiza
        if not meta.status == 'A':
            return

        # Retorna um QuerySet [Uma lista de objetos do banco de dados que seguem algumas condições]
        parcelas = ParcelasTransacao.objects.filter(
            # O underline duplo é uma forma de navegar pelas chaves estrangeiras no Django
            transacao_fk__user_fk=self.user,
            categoria_fk__nome=meta.categoria_fk,
            data__gte=meta.data_inicio,             # __gte maior ou igual
            data__lte=meta.data_fim,                # __lte menor ou igual
            pago=True,
        )

        total = parcelas.aggregate(soma=Sum('valor'))['soma'] or Decimal('0.00')

        hoje = date.today()

        if meta.tipo == 'MAX':
            if total > meta.valor:
                meta.status = 'U'
            elif hoje > meta.data_fim and meta.status != 'U':
                meta.status = 'C'
        elif meta.tipo == 'MIN':
            if total >= meta.valor:
                meta.status = 'C'
            elif hoje > meta.data_fim and meta.status != 'C':
                meta.status = 'N'
        try:
            meta.save()
        except Exception:
            raise Exception('Erro inesperado ao atualizar metas')


    def ProgressoMeta(self, meta: Metas):

        valor_acumulado = ParcelasTransacao.objects.filter(
            transacao_fk__user_fk=self.user,
            categoria_fk__nome=meta.categoria_fk,
            data__gte=meta.data_inicio,
            data__lte=meta.data_fim,
            pago=True,
        ).aggregate(valor_total=Sum('valor'))['valor_acumulado']

        if meta.valor == Decimal('0.00'):
            percentual = Decimal('100.00')
        else:
            percentual = (valor_acumulado / meta.valor) * 100

        return [round(percentual, 2)]

    def metasEmDict(self, meta: Metas):
        return {
            "categoria": meta.categoria_fk.nome,
            "tipo": meta.tipo,
            "valor": Decimal(meta.valor),
            "data_inicio": meta.data_inicio,
            "data_fim": meta.data_fim,
            "descricao": meta.descricao,
            "status": meta.status
        }