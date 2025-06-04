from decimal import Decimal

class QuantidadeParcelas:
    def __init__(self, quantidade_meses:str | int):
        self.__verificacaoQuantidadeParcelas(int(quantidade_meses))
        self.valor = int(quantidade_meses)
        self.valorDecimal = Decimal(self.valor)

    def __verificacaoQuantidadeParcelas(self, quantidade_meses: int):
        if quantidade_meses <= 0 or quantidade_meses >= 99:
            raise ValueError('quantidade de parcelas invalida, escolha um valor entre 0 e 99')