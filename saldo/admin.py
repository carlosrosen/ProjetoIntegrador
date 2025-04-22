from django.contrib import admin
from .models import Metas, Transacao, Categoria

# Register your models here.
admin.site.register(Metas)
admin.site.register(Transacao)
admin.site.register(Categoria)
