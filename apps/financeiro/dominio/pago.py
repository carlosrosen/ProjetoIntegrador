class Pago:
    def __init__(self,pago):
        self.status = self.__verificacaoPago(pago)

    def __verificacaoPago(self,pago):
        if pago.lower() == 'true':
            return True
        elif pago.lower() == 'false':
            return False
        raise ValueError('valor de pago invalido')
