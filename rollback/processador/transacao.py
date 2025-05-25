from rollback.dominio.transacao import InformacoesTransacao
from financeiro.dominio import *

class ProcessadorTransacao(InformacoesTransacao):
    def __init__(self, user, **kwargs):
        super().__init__(user=user, **kwargs)

    def desfazerCriar(self):
        pass

    def desfazerAlterar(self):
        pass

    def desfazerRemover(self):
        pass
