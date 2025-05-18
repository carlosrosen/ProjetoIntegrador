from django.contrib import admin
from .models import Transacao, ParcelasTransacao, Categoria

# Register your models here.
admin.site.register(ParcelasTransacao)
admin.site.register(Transacao)
admin.site.register(Categoria)
