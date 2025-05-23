from decimal import Decimal

class Valor:
    def __init__(self, valor:str):
        self.valor = self.__formatacaoValor(valor)

    def __formatacaoValor(self,valor:str):
        return Decimal(valor)

    def valorParcela(self, quantidade_parcelas: Decimal) -> Decimal:
        try:
            return self.valor / quantidade_parcelas
        except Exception as e:
            raise Exception('Erro inesperado ao calcular o valor da parcela')