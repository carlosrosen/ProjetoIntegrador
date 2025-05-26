from django.db import models
from django.utils import timezone
from django.conf import settings
from apps.financeiro.models import Categoria

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
    descricao = models.CharField(max_length=100, null=True)

    # Inicializa o nome de cada objeto/atributos
    def __str__(self):
        return f"{self.user_fk.id} - {self.nome}"

