from django.apps import AppConfig


class MoneymappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'moneymapp'

    def ready(self):
        import moneymapp.signals