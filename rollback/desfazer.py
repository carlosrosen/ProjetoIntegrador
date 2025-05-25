from django.contrib.auth.models import AbstractBaseUser

from rollback.dominio.pilha import Pilha
from rollback.processador import *

class Desfazer:
    __tipos_operacoes = {'transacao': }

    def __init__(self, user):
        if not isinstance(user, AbstractBaseUser):
            raise TypeError('Usuario Invalido.')
        self.user = user
        self.desfazer = Pilha(user=self.user)
        self.refazer = Pilha(user=self.user)


    def armazenarAcao(self,**kwargs):
        #chama a pilha desfazer e armazena o objeto criardo com os dados

        #caso tenha conteudo na pilha de refazer limpa a pilha

    def desfazerAcai(self):
        acao = self.desfazer.pop()
        self.refazer.push(acao)

        #chama a classe que tem a logica pra desfazer a acao







