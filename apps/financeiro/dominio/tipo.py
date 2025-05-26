class Tipo:
    __opcoesTipo = {
        'receita': 'R',
        'despesa': 'D'
    }
    def __init__(self, tipo:str):
        self.valor = self.formatarTipo(tipo)

    def formatarTipo(self, tipo:str):
        try:
            return self.__opcoesTipo[tipo.lower()]
        except KeyError:
            raise ValueError(f'Falha na formatação do tipo, tipo invalido')
