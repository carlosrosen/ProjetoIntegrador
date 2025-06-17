from django.apps import AppConfig


class SaldoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.financeiro'

    def ready(self):
        from . import signals
