from metas.models import Metas

from django.contrib.auth.models import AbstractBaseUser

from common.dominio.data import Data


class Metas:
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