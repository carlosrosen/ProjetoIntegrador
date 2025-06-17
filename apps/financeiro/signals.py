from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria

@receiver(post_migrate)
def InicializarCategorias(sender, **kwargs):
    valores_categorias = [
          ['Salário' , 'R']
        , ['Aposentadoria' , 'R']
        , ['Bolsa de estudos' , 'R']
        , ['Aluguel recebido' , 'R']
        , ['Rendimentos de investimentos' , 'R']
        , ['Freelance' , 'R']
        , ['Venda de produtos' , 'R']
        , ['Comissão' , 'R']
        , ['Prêmios' , 'R']
        , ['Presente' , 'R']
        , ['Doação' , 'R']
        , ['Herança' , 'R']
        , ['Outras receitas' , 'R']

        , ['Alimentação', 'D']
        , ['Transporte', 'D']
        , ['Educação', 'D']
        , ['Moradia', 'D']
        , ['Despesas Pessoais', 'D']
        , ['Saúde', 'D']
        , ['Impostos e tarifas', 'D']
        , ['Outras despesas', 'D']
    ]
    for name, tipo in valores_categorias:
        Categoria.objects.get_or_create(nome=name, tipo=tipo)
