from django.contrib.auth.base_user import AbstractBaseUser


class Informacoesbjetivo:
    def __init__(self,user,**kwargs):
        if not isinstance(user,AbstractBaseUser):
            raise TypeError('Usuario Invalido')
        self.user = user

        #veja o padrao no transacao, vamos inicializar todos os valores para mexer com eles no processador