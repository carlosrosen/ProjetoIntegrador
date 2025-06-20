from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import date
from decimal import Decimal

from apps.usuarios.models import CustomUser

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from common.dominio.data import Data


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
        encontrou = Categoria.objects.filter(nome=nome)
        if not encontrou:
            raise ValueError('Categoria não encontrada')

    @staticmethod
    def GetTodasCategorias():
        categorias = Categoria.objects.all()
        return categorias
    
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
    def buscaEntreDatas(data_inicio: date, data_fim: date):
        if data_inicio > data_fim:
            data_inicio, data_fim = data_fim, data_inicio
        return ParcelasTransacao.objects.filter(data__gt=data_inicio, data__lt=data_fim)

    @staticmethod
    def buscaParcelasIntervalo(user:CustomUser ,data_inicio: date, data_fim: date):
        if data_inicio > data_fim:
            data_inicio, data_fim = data_fim, data_inicio
        intervalo = ParcelasTransacao.objects.filter(transacao_fk__user_fk=user ,data__gte=data_inicio, data__lt=data_fim)
        if intervalo:
            intervalo = intervalo.order_by('data')
        return intervalo

    def __str__(self):
        return f'''
        transacao: {self.transacao_fk.id}
        - parcela: {self.id}
        - numero da parcela: {self.ordem_parcela}
        - pago: {self.pago}'''

class HistoricoSaldo(models.Model):
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='HistoricoSaldo')
    data = models.DateField(null=False)
    saldo = models.DecimalField(max_digits=12,decimal_places=2,null=False)

    @staticmethod
    def getSaldoInicioMes(user:CustomUser, mes:int ,ano:int):
        historico = HistoricoSaldo.objects.filter(user_fk=user)
        saldo =  Decimal
        data_busca = Data.inicializar(dia=1,mes=mes,ano=ano)
        try:
            saldo = historico.get(data=data_busca.valor).saldo
        except ObjectDoesNotExist:
            registro_mais_recente = historico.order_by('-data').first()
            registro_mais_antigo = historico.order_by('data').first()
            if data_busca.valor > registro_mais_recente.data:
                saldo = registro_mais_recente.saldo
                parcelas = ParcelasTransacao.objects.filter(transacao_fk__user_fk=user
                                                          , data__gte=registro_mais_recente.data
                                                          , data__lt=data_busca.valor
                )
                if parcelas.count() > 0:
                    for parcela in parcelas:
                        if parcela.transacao_fk.tipo == 'D':
                            saldo += parcela.valor
                        elif parcela.transacao_fk.tipo == 'D':
                            saldo -= parcela.valor
            elif data_busca.valor < registro_mais_antigo.data:
                saldo = Decimal('0')
        return saldo

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
