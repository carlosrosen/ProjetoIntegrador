from django.contrib.auth.models import AbstractBaseUser
from apps.usuarios.models import CustomUser
from typing import cast

from rollback.dominio.pilha import Pilha


class Desfazer:
    #__tipos_operacoes = {'transacao': }

    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario Invalido.')
        self.user = cast(CustomUser, user)
        self.desfazer = Pilha()
        self.refazer = Pilha()


    def armazenarAcao(self,**kwargs):
        #chama a pilha desfazer e armazena o objeto criardo com os dados

        #caso tenha conteudo na pilha de refazer limpa a pilha
        pass

    def desfazerAcai(self):
        acao = self.desfazer.pop()
        self.refazer.push(acao)

        #chama a classe que tem a logica pra desfazer a acao







