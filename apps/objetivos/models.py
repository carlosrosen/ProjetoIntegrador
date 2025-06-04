from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.conf import settings

# Tabela para objetivos
class Objetivos(models.Model):
    __opcoes_status = [
        ('A', 'Ativo'),
        ('T', 'Atrasado'),
        ('P', 'Pausado'),
        ('C', 'Concluido')
    ]

    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Objetivos')
    titulo = models.CharField(max_length=100, null=False)
    valor_objetivo = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    valor_guardado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    data_inicio = models.DateField(auto_now_add=True)
    data_fim = models.DateField(null=False)
    status = models.CharField(max_length=1, choices=__opcoes_status, default='A')

    def porcentagem(self):
        if self.valor_guardado > 0:
            return round((self.valor_guardado/self.valor_objetivo)*100, 2)
        return 0

    def valor_faltante(self):
        return max(self.valor_objetivo - self.valor_guardado, Decimal('0'))

    def status_formatado(self):
        formatacao = {
              'A': 'Ativo'
            , 'T': 'Atrasado'
            , 'P': 'Pausado'
            , 'C': 'Concluido'
        }
        return formatacao[self.status]

    def __str__(self):
        return f'titulo: {self.titulo} - status: {self.status}'

class TransacaoObjetivo(models.Model):
    __opcoes_tipo = [
        ('D', 'Deposito'),
        ('R', 'Resgate')
    ]

    objetivo_fk = models.ForeignKey(Objetivos, on_delete=models.CASCADE, related_name='TransacaoObjetivo')
    tipo = models.CharField(max_length=1, choices=__opcoes_tipo, null=False)
    valor = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        pass
        # Preencher aqui depois
