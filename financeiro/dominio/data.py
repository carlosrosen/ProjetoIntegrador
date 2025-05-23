from datetime import datetime
from dateutil.relativedelta import relativedelta

class Data:
    def __init__(self, data:str):
        self.valor = self.__formatarData(data)

    def __formatarData(self,data):
        try:
            return datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError('valor de data incorreto')

    def somarMes(self, quantidade_meses: int):
        quantidade_meses = abs()
        return self.valor + relativedelta(months=quantidade_meses)

    def subtrairMes(self, quantidade_meses: int):
        quantidade_meses = abs(quantidade_meses)
        return self.valor + relativedelta(months=-quantidade_meses)

    @staticmethod
    def comparacaoDatasMenoresQueHoje(data: datetime) -> bool:
        if data <= datetime.today().date():
            return True
        return False