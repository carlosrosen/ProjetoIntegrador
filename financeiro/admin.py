from django.contrib import admin
from .models import Receita, Perfil, DespesaFixa, DespesaVariavel, Metas
# Register your models here.
admin.site.register(Perfil)
admin.site.register(Receita)
admin.site.register(DespesaVariavel)
admin.site.register(DespesaFixa)
admin.site.register(Metas)
