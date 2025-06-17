class Pilha:
    class __No:
        def __init__(self, objeto):
            self.valor = objeto
            self.proximo = None

    def __init__(self):
        self.tamanho = 0
        self.__topo = None

    def __criarNo(self, dicionario: dict):
        novo_no = self.__No(dicionario)
        return novo_no

    def push(self, dicionario: dict):
        novo = self.__criarNo(dicionario)
        novo.proximo = self.__topo
        self.__topo = novo
        self.tamanho += 1

    def top(self):
        return self.__topo.valor

    def pop(self):
        if self.__topo is None:
            return None
        else:
            dado = self.__topo.valor
            self.__topo = self.__topo.proximo
            self.tamanho -= 1
            return dado

    def free(self):
        self.__topo = None