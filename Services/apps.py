"""
The modules have imported for different purpose mentioned as below:
"""
from django.apps import AppConfig


class ServicesConfig(AppConfig):
    """
    ServicesConfig
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Services'

    def ready(self):
        import Services.signals
