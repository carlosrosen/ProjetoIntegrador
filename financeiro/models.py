from django.db import models
from django.conf import settings
from django.utils import timezone

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
    sub_categoria = models.CharField(max_length=50, null=False)
    tipo = models.CharField(max_length=1, choices=__escolhas_tipo, null=False)

    @staticmethod
    def verificacaoNomesCategoria(nome:str):
        encontrou = Categoria.objects.filter(nome=nome)
        if not encontrou:
            raise ValueError('Categoria não encontrada')
        return Categoria.objects.get(nome=nome)

    @staticmethod
    def verificacaoNomesSubCategoria(nome:str):
        encontrou = Categoria.objects.filter(sub_categoria=nome)
        if not encontrou:
            raise ValueError('Subcategoria não encontrada')
        return Categoria.objects.get(sub_categoria=nome)

    
    #formata o nome dos objetos de categoria
    def __str__(self):
        return f"{self.id} - {self.nome} - {next((nome for busca, nome in self.__escolhas_tipo if busca == self.tipo))}"
    
class Transacao(models.Model):
    # inicializa as opções que vai ser limitado o tipo e recorrencias
    __escolhas_tipo = [
        {
            # o funcionamento dessa limitição é parecido com as tuplas mas usa dicionarios em vez de tuplas
            'R': 'Receita',
            'D': 'Despesa'
        }
    ]

    # Define os atributos da tabela transações
    
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Transacao')
    tipo = models.CharField(max_length=1, choices=__escolhas_tipo, null=False)
    quantidade_parcelas = models.IntegerField(default=1)
    descricao = models.CharField(max_length=100, null=True)
    '''
    # Formata o nome dos objetos de transação
    def __str__(self):
        return f''''''id: {self.id}
    - user_id: {self.user_fk.id}
    - categoria: {self.categoria_fk.nome}
    - tipo: {self.__escolhas_tipo[0][self.tipo]}
    - valor:  {self.valor}
    - quantidade parcelas : {self.quantidade_parcelas}
    - descricao: {self.descricao}'''''''

    '''
class ParcelasTransacao(models.Model):
    transacao_fk = models.ForeignKey(Transacao, on_delete=models.CASCADE, related_name='ParcelasTransacao')
    categoria_fk = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='ParcelasTransacao')
    data = models.DateField(null=False)
    valor = models.DecimalField(max_digits=12,decimal_places=2,null=False) # Valor das parcelas
    ordem_parcela = models.PositiveIntegerField(null=False)
    pago = models.BooleanField(default=True)

    def __str__(self):
        return f'''
        transacao: {self.transacao_fk.id}
        - numero da parcela: {self.ordem_parcela}
        - pago: {self.pago}'''