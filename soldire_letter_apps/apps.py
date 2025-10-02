from django.apps import AppConfig


class SoldireLetterAppsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'soldire_letter_apps'
    
    def ready(self):
        import soldire_letter_apps.signals
