from decimal import Decimal

class ValorObjetivo:
    def __init__(self,valor:str):
        self.valor = self.__formatarValor(valor)

    def __formatarValor(self,valor):
        valor = int(valor)
        if valor < 0:
            valor = -valor
        return Decimal(valor)

    @staticmethod
    def valorLimite(valor_objetivo,valor_guardado) -> abs:
        try:
            return abs(valor_objetivo - valor_guardado)
        except Exception as e:
            raise Exception('Erro inesperado ao calcular o valor limite')

