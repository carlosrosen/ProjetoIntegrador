from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import calendar

class Data:
    def __init__(self, data: str | date) -> None:
        self.valor = self.__formatarData(data)


    @classmethod
    def variarMes(cls, mes:int , ano:int , quatidade_variacao):
        data_base = date(day=1,month=mes,year=ano)
        data = data_base + relativedelta(months=quatidade_variacao)
        return cls(data)

    @classmethod
    def inicializar(cls, dia:int, mes:int, ano:int) :
        dia, mes, ano = abs(dia), abs(mes), abs(ano)
        data = f'{ano}-{mes}-{dia}'
        return cls(data)

    @classmethod
    def incrementarMes(cls, data: str | date):
        if type(data) == str:
            data = datetime.strptime(data, "%Y-%m-%d").date()
        nova_data = data + relativedelta(months=1)
        return cls(nova_data)

    @classmethod
    def decrementarMes(cls, data:str | date):
        if type(data) == date:
            data = f'{data.year}-{data.month}-{data.day}'
        nova_data = data + relativedelta(months=-1)
        return cls(nova_data)

    def __formatarData(self,data):
        if type(data) == date:
            return data
        try:
            return datetime.strptime(data, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError('valor de data incorreto')

    def proximoMes(self, quantidade_meses: int):
        quantidade_meses = abs(quantidade_meses)
        return self.valor + relativedelta(months=quantidade_meses)

    def mesAnterior(self, quantidade_meses: int):
        quantidade_meses = abs(quantidade_meses)
        return self.valor + relativedelta(months=-quantidade_meses)

    @staticmethod
    def ultimoDiaMes(mes:int, ano:int):
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        return date(ano, mes, ultimo_dia)

    @staticmethod
    def primeiroDiaMes(mes:int,ano:int):
        return date(ano, mes, 1)

    @staticmethod
    def formatarMesAno(mes:int, ano:int):
        import locale
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        mes, ano = abs(mes), abs(ano)
        data = Data.inicializar(1, mes, ano)
        nome_mes = data.valor.strftime('%B')
        return nome_mes[0:3] + '/' + str(ano)[2:4]
