from metas.models import Metas
from financeiro.models import ParcelasTransacao

from django.contrib.auth.models import AbstractBaseUser

from common.dominio.data import Data
from decimal import Decimal
from datetime import date


class Meta:
    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario invalido')
        self.user = user

    def criarMeta(
            self,
            categoria: str,
            tipo: str,
            valor: float,
            data_inicio: Data,
            data_fim: Data,
            descricao: str
    ):
        # Tem que formatar os valores certinhos aqui no parametro

        if tipo not in ['MAX', 'MIN']:
            raise ValueError("Tipo de meta inválido. Use 'MAX' para limite máximo ou 'MIN' para mínimo desejado.")
        if data_fim < data_inicio:
            raise ValueError("A data final não pode ser anterior à data inicial.")

        Metas.objects.create(
            user_fk=self.user,
            tipo=tipo,
            categoria=categoria,
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
            valor: float,
            data_inicio: Data,
            data_fim: Data,
            descricao: str,
    ):

        if data_fim < data_inicio:
            raise ValueError("A data final não pode ser anterior à data inicial.")
        elif data_fim < meta.data_inicio:
            raise ValueError("A data final não pode ser anterior à data inicial.")

        meta.data_fim = data_fim
        meta.categoria = categoria
        meta.tipo = tipo
        meta.valor = valor
        meta.data_inicio = data_inicio
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
            categoria_fk__nome=meta.categoria,
            data__gte=meta.data_inicio,             # __gte maior ou igual
            data__lte=meta.data_fim,                # __lte menor ou igual
            pago=True,
        )

        #Somatorio de todos os valores dos objetos encontrados nas condições acima
        total = sum(Decimal(p.valor) for p in parcelas)

        hoje = date.today()

        if meta.tipo == 'MAX':
            if total > meta.valor:
                meta.status = 'U'
            elif hoje > meta.data_fim:
                meta.status = 'C'
        elif meta.tipo == 'MIN':
            if total > meta.valor:
                meta.status = 'C'
            elif hoje > meta.data_fim:
                meta.status = 'N'

        # Tem que colocar aquele error caso tudo dê errado

        meta.save()


    # Será que integro essa função dentro do atualizarStatusMeta?
    def verificarProgressoMeta(self, meta: Metas):
        hoje = date.today()

        # Coloco a outra função aqui?

        parcelas = ParcelasTransacao.objects.filter(
            transacao_fk__user_fk=self.user,
            categoria_fk__nome=meta.categoria,
            data__gte=meta.data_inicio,
            data__lte=meta.data_fim,
            pago=True,
        )

        valor_acumulado = sum(Decimal(p.valor) for p in parcelas)

        if meta.valor == Decimal('0.00'):
            percentual = Decimal('100.00')
        else:
            percentual = (valor_acumulado / meta.valor) * 100

        StatusDescricao = {
            'A': 'Ativo',
            'P': 'Pausada',
            'U': 'Ultrapassada',
            'N': 'Não foi atingida',
            'C': 'Concluida',
        }

        TipoMeta = {
            'MAX': 'Limite máximo',
            'MIN': 'Minimo desejado'
        }

        return {
            'valor_meta': meta.valor,
            'tipo': TipoMeta.get(meta.tipo, 'Erro'),
            'valor_acumulado': valor_acumulado,
            # Principalmente estava apenas pensando em retornar essas informações abaixo
            'status': StatusDescricao.get(meta.status, 'Erro'),
            'percentual': round(percentual, 2),
        }