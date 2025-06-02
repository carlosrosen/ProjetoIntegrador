from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import date
from decimal import Decimal

from apps.usuarios.models import CustomUser


# Cria a tabela Categoria
class Categoria(models.Model):
    # inicializa as opções que vai ser limitado o tipo
    __escolhas_tipo = [
        # o primeiro valor da tupla é o valor a ser inserido no banco de dados e o segundo é para tornar legivel o que significa a inserção
        ('R', 'Receita'),
        ('D', 'Despesa')
    ]

    # Define os atributos da tabela de Categoria
    nome = models.CharField(max_length=50, null=False)
    tipo = models.CharField(max_length=1, choices=__escolhas_tipo, null=False)

    @staticmethod
    def verificacaoNomesCategoria(nome:str):
        nome = nome[0].upper() + nome[1:].lower()
        encontrou = Categoria.objects.filter(nome=nome)
        if not encontrou:
            raise ValueError('Categoria não encontrada')
    
    #formata o nome dos objetos de categoria
    def __str__(self):
        return f"{self.id} - {self.nome} - {next((nome for busca, nome in self.__escolhas_tipo if busca == self.tipo))}"
    
class Transacao(models.Model):
    # inicializa as opções que vai ser limitado o tipo e recorrencias
            # o funcionamento dessa limitição é parecido com as tuplas mas usa dicionarios em vez de tuplas
    __escolhas_tipo = [
        ('R', 'Receita'),
        ('D', 'Despesa')
    ]

    # Define os atributos da tabela transações
    
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Transacao')
    categoria_fk = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='Transacao')
    tipo = models.CharField(max_length=1, choices=__escolhas_tipo, null=False)
    quantidade_parcelas = models.IntegerField(default=1)
    descricao = models.CharField(max_length=100, null=True)

    # Formata o nome dos objetos de transação
    def __str__(self):
        return f'''id: {self.id}
    - user_id: {self.user_fk.id}
    - tipo: {next(palavra for letra, palavra in self.__escolhas_tipo if letra == self.tipo)}
    - quantidade parcelas: {self.quantidade_parcelas}
    - descricao: {self.descricao}'''

class ParcelasTransacao(models.Model):
    transacao_fk = models.ForeignKey(Transacao, on_delete=models.CASCADE, related_name='ParcelasTransacao')
    data = models.DateField(null=False)
    valor = models.DecimalField(max_digits=12,decimal_places=2,null=False) # Valor das parcelas
    ordem_parcela = models.PositiveIntegerField(null=False)
    pago = models.BooleanField(default=True)

    @staticmethod
    def buscaEntreDatas(data_inicio: date, data_fim: date) -> list:
        if data_inicio > data_fim:
            data_inicio, data_fim = data_fim, data_inicio
        return ParcelasTransacao.objects.filter(data__gt=data_inicio, data__lt=data_fim)

    @staticmethod
    def buscaIntervaloHistoricoSaldo(data_inicio: date, data_fim: date):
        if data_inicio > data_fim:
            data_inicio, data_fim = data_fim, data_inicio
        return ParcelasTransacao.objects.filter(data__gte=data_inicio, data__lt=data_fim)

    def __str__(self):
        return f'''
        transacao: {self.transacao_fk.id}
        - numero da parcela: {self.ordem_parcela}
        - pago: {self.pago}'''

class HistoricoSaldo(models.Model):
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='HistoricoSaldo')
    data = models.DateField(null=False)
    saldo = models.DecimalField(max_digits=12,decimal_places=2,null=False)

    @staticmethod
    def criarTupla(user:CustomUser, data:date, saldo:Decimal):
        if not isinstance(user, AbstractUser):
            raise TypeError('Usuario invalido')
        HistoricoSaldo.objects.create(user_fk=user, data=data, saldo=saldo)

    @staticmethod
    def inicializarPrimeiroValor(user):
        if not isinstance(user, AbstractUser):
            raise TypeError('Usuario invalido')
        HistoricoSaldo.objects.create(user_fk=user
                                      , data = date(date.today().year,date.today().month,1)
                                      , saldo = Decimal(0.0)
                                      )


    def __str__(self):
        return f'''
        usuario: {self.user_fk.id}
        - data: {self.data}
        - saldo: {self.saldo}'''
