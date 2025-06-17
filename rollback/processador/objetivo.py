from rollback.dominio.objetivo import Informacoesbjetivo

#Nesses metoddos que vao ficar a logica de reversão

class ProcessadorObjetivo(Informacoesbjetivo):
    def __init__(self, user, **kwargs):
        super().__init__(user, **kwargs)

    def desfazerCriar(self):
        pass

    def desfazerEditar(self):
        pass

    def desfazerRemover(self):
        pass
