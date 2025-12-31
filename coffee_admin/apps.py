from django.apps import AppConfig


class CoffeeAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coffee_admin'
    verbose_name = 'Coffee Admin'

    def ready(self):
        """
        This method is called when Django starts.
        Use this for any admin-specific initialization.
        """
        pass
