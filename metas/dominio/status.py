class Status:
    __opcoes_status = [
        {
            'ativo': 'A',
            'pausado': 'P',
            'concluido': 'C',
        }
    ]

    def __init__(self, status:str):
        if not self.__verificarStatus(status):
            raise ValueError('Status incorreto')
        self.status = self.__opcoes_status[status]

    def __verificarStatus(self, status):
        if status.lower() in self.__opcoes_status[0].keys():
            return True
        return False


