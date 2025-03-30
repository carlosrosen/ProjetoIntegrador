from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
# Create your models here.
class Metas(models.Model):
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Metas')
    nome = models.CharField(max_length=100,null=False,unique=True)
    valor = models.DecimalField(max_digits=13,decimal_places=2,null=False)
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(null=False)
    status = models.BooleanField(default=True)
    descricao = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return f"{self.user_fk.id} - {self.nome}"
    
class Categoria(models.Model):
    escolhas_tipo = [
        ('r', 'receita'),
        ('d', 'despesa')
    ]
    nome = models.CharField(max_length=50, null=False)
    tipo = models.CharField(max_length=1, choices=escolhas_tipo, null=False)
    def __str__(self):
        return f"{self.id} - {self.nome} - {self.tipo}"
    
class Transacao(models.Model):
    escolhas_tipo = [
        ('r', 'receita'),
        ('d', 'despesa')
    ]
    escolhas_recorrencia =[
        ('m', 'mensal'),
        ('t', 'trimestral'),
        ('a', 'anual')
    ]
    
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Transacao')
    categoria_fk = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='Transacao')
    tipo = models.CharField(max_length=8, choices=escolhas_tipo, null=False)
    valor = models.DecimalField(max_digits=13,decimal_places=2,null=False)
    data_criacao = models.DateField(auto_now_add=True)
    data = models.DateField(null=False)
    eh_recorrente = models.BooleanField(default=False)
    recorrencia_tipo = models.CharField(max_length=10,choices=escolhas_recorrencia, default='m')
    status = models.BooleanField(default=True)
    descricao = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return f"{self.user_fk.id} - {self.tipo} - recorrencia: {self.eh_recorrente} - ativo: {self.status}"
