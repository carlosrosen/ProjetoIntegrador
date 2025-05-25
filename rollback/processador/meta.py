from rollback.dominio.meta import InformacoesMeta

class ProcessadorMeta(InformacoesMeta):
    def __init__(self,user ,**kwargs):
        super().__init__(user, **kwargs)

    def desfazerCriar(self):
        pass

    def desfazerEditar(self):
        pass

    def desfazerDeletar(self):
        pass
