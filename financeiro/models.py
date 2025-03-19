from django.db import models
from django.contrib.auth.models import User
from datetime import date

# cria uma tabela para linkar o user com o perfil
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")

#cria a tabela de receita com chave estrangeira, valor, descrição e data
class Receita(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="receitas")
    valor = models.DecimalField(default=0.0, decimal_places=2, max_digits=13, null=False)
    descricao = models.CharField(max_length=100)
    data = models.DateField(null=False)

#cria a tabela de despesa variavel a com chave estrangeira, valor, descrição e data
class DespesaVariavel(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="despesas_variaveis")
    valor = models.DecimalField(default=0.0, decimal_places=2, max_digits=13, null=False)
    descricao = models.CharField(max_length=100)
    data = models.DateField(null=False)

#cria a tabela de despesafixa com chave estrangeira, valor, descrição e data
class DespesaFixa(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="despesas_fixas")
    valor = models.DecimalField(default=0.0, decimal_places=2, max_digits=13, null = False)
    descricao = models.CharField(max_length=100)
    data = models.DateField(null=False)

class Metas(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name="Metas")
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(default=0.0, decimal_places=2, max_digits=13, null=False)
    data_inicio = models.DateField(auto_now_add=True)
    data_fim = models.DateField()
    descricao = models.CharField(max_length=100)