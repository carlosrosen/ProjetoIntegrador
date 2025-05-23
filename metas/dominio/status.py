class Status:
    __opcoes_status = [
        {
            'ativo': 'A',
            'pausado': 'P',
            'concluido': 'C',
        }
    ]

    def __init__(self, status:str):
        self.valor = self.__formatarStatus(status)


    def __formatarStatus(self, status) -> bool | ValueError:
        if not status.lower() in self.__opcoes_status[0].keys():
            raise ValueError('Status incorreto')
        return self.__opcoes_status[0][status.lower()]


