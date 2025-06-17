from django.contrib import admin
from .models import Transacao, ParcelasTransacao, Categoria, HistoricoSaldo

# Register your models here.
admin.site.register(ParcelasTransacao)
admin.site.register(Transacao)
admin.site.register(Categoria)
admin.site.register(HistoricoSaldo)
