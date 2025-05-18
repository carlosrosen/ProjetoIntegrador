from datetime import date
from dateutil import relativedelta

class Data:
    def __init__(self, data:str):
        self.valor = self.__formatarData(data)

    def __formatarData(self,data):
        try:
            return date.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError('formatação de data incorreta')

    def somarMes(self, quantidade_meses: int):
        return self.valor + relativedelta(months=quantidade_meses)

    @staticmethod
    def comparacaoDatasMenoresQueHoje(data: date):
        if data <= date.today():
            return True
        return False