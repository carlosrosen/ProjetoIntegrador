from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Tabela para objetivos
class Objetivos(models.Model):
    __opcoes_status = [
        {
            'A': 'Ativo',
            'P': 'Pausado',
            'C': 'Concluido',
        }
    ]

    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Objetivos')
    titulo = models.CharField(max_length=100, null=False)
    valor_objetivo = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    valor_guardado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    data_inicio = models.DateField(auto_now_add=True)
    data_fim = models.DateField(null=False)
    status = models.CharField(max_length=1, choices=__opcoes_status, default='A')

    def __str__(self):
        return f'titulo: {self.titulo} - status: {self.status}'

class TransacaoObjetivo(models.Model):
    __opcoes_tipo = [
        {
            'D': 'Deposito',
            'R': 'Resgate',
        }
    ]

    objetivo_fk = models.ForeignKey(Objetivos, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=__opcoes_tipo, null=False)
    valor = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    data = models.DateField(default=timezone.now)

    def __str__(self):
        pass
        # Preencher aqui depois

# Tabela para metas
class Metas(models.Model):
    __opcoes_tipo = [
        {
            'MAX': 'Limite máximo',    # Meta de não ultrapassar (Despesa)
            'MIN': 'Minimo desejado'   # Meta de alcançar (Receita)
        }
    ]
    # Define os atributos da tabela metas
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Metas')
    tipo = models.CharField(max_length=3, choices=__opcoes_tipo, null=False)
    categoria = models.CharField(max_length=100, null=False) # Uso a tabela de categoria aqui?
    valor = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(null=False)
    descricao = models.CharField(max_length=100, null=True)

    # Inicializa o nome de cada objeto/atributos
    def __str__(self):
        return f"{self.user_fk.id} - {self.nome}"
# Create your models here.
