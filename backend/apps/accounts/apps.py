from django.apps import AppConfig

class AccountsConfig(AppConfig):
    """
    Configuration class for the accounts application.
    Responsible for registering the app with Django.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
