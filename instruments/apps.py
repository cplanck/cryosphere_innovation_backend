from django.apps import AppConfig


class InstrumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'instruments'

    def ready(self):
        import instruments.signals  # Replace "your_app_name" with the actual name of your app
