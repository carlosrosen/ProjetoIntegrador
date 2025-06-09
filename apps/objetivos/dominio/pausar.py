class Pausar:
    def __init__(self, pausar:str):
        self.valor = self.__verificarPausar(pausar)

    def __verificarPausar(self, pausar:str):
        if pausar is None:
            return False
        elif pausar == 'on':
            return True