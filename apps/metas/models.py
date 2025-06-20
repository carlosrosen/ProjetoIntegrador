from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.conf import settings
from apps.financeiro.models import Categoria, Transacao, ParcelasTransacao

from decimal import Decimal

# Tabela para metas
class Metas(models.Model):
    __opcoes_tipo = [
        ('MAX', 'Limite máximo'),    # Meta de não ultrapassar (Despesa)
        ('MIN', 'Minimo desejado')   # Meta de alcançar (Receita)
    ]

    __opcoes_status = [
        ('A', 'Ativo'),
        ('U', 'Ultrapassado'),
        ('N', 'Não atingido'),
        ('C', 'Concluido'),
    ]

    # Define os atributos da tabela metas
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Metas')
    categoria_fk = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="Metas")
    tipo = models.CharField(max_length=3, choices=__opcoes_tipo, null=False)
    status = models.CharField(max_length=1, choices=__opcoes_status, default='A')
    valor = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(null=False)
    data_conclusao = models.DateField(null=True,blank=True)
    descricao = models.CharField(max_length=100, null=True)

    def valorAcumulado(self):
        valor_acumulado = ParcelasTransacao.objects.filter(
            transacao_fk__user_fk=self.user_fk,
            transacao_fk__categoria_fk=self.categoria_fk,
            data__gte=self.data_inicio,
            data__lte=self.data_fim,
            pago=True,
        ).aggregate(total=Sum('valor'))['total']
        return valor_acumulado or 0

    def porcentagem(self):
        valor_acumulado = self.valorAcumulado()
        return round((valor_acumulado / self.valor) * 100, 2)

    # Funções de formatação (Poderiamos já ter substituido o nome dos status direto em vez de usar só letras [Ai não teria necessidade de ficar formatando)

    def status_formatado(self):
        formatacao = {
            'A': 'Ativo',
            'U': 'Ultrapassado',
            'N': 'Não atingido',
            'C': 'Concluído'
        }
        return formatacao[self.status]

    def desempenho(self):
        formatacao = {
            'MAX': 'Gasto atual',
            'MIN': 'Economizado'
        }
        return formatacao[self.tipo]

    def tipagem(self):
        formatacao = {
            'MAX': 'Limite máximo',
            'MIN': 'Minimo desejado'
        }
        return formatacao[self.tipo]

    # Inicializa o nome de cada objeto/atributos
    def __str__(self):
        return f"user: {self.user_fk.id} - categoria:{self.categoria_fk.nome} - {self.status_formatado()}"