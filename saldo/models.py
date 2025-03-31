from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

#Cria a tabela metas
class Metas(models.Model): 
    # Define os atributos da tabela metas
    user_fk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Metas')
    nome = models.CharField(max_length=100,null=False,unique=True)
    valor = models.DecimalField(max_digits=13,decimal_places=2,null=False)
    data_inicio = models.DateField(default=timezone.now)
    data_fim = models.DateField(null=False)
    status = models.BooleanField(default=True)
    descricao = models.CharField(max_length=100,null=True)
    
    # Inicializa o nome de cada objeto/atributos
    def __str__(self):
        return f"{self.user_fk.id} - {self.nome}"
    
# Cria a tabela Categoria
class Categoria(models.Model):
    # inicializa as opções que vai ser limitado o tipo
    escolhas_tipo = [
        # o primeiro valor da tupla é o valor a ser inserido no banco de dados e o segundo é para tornar legivel o que significa a inserção
        ('r', 'Receita'),
        ('d', 'Despesa')
    ]
    
    # Define os atributos da tabela de Categoria
    nome = models.CharField(max_length=50, null=False)
    tipo = models.CharField(max_length=1, choices=escolhas_tipo, null=False)
    
    #formata o nome dos objetos de categoria
    def __str__(self):
        return f"{self.id} - {self.nome} - {next((nome for busca, nome in self.escolhas_tipo if busca == self.tipo))}"
    
class Transacao(models.Model):
    # inicializa as opções que vai ser limitado o tipo e recorrencias
    escolhas_tipo = [
        {
            # o funcionamento dessa limitição é parecido com as tuplas mas usa dicionarios em vez de tuplas
            'r': 'receita', 
            'd': 'despesa'
        }
    ]
    escolhas_recorrencia =[
        ('m', 'mensal'),
        ('t', 'trimestral'),
        ('a', 'anual')
    ]
    
    # Define os atributos da tabela transações
    
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
    
    # Formata o nome dos objetos de transação
    def __str__(self):
        return f'''id: {self.id}
    - user_id: {self.user_fk.id}
    - categoria: {self.categoria_fk.nome}
    - tipo: {self.escolhas_tipo[0][self.tipo]}
    - recorrencia: {self.eh_recorrente}
    - ativo: {self.status}'''
