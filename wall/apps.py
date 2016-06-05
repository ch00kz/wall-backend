from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db.models.signals import post_migrate


def setup(sender, **kwargs):
    """Sets up the application by creating an admin superuser if one
    does not exist.
    """
    DEFAULT_ADMIN_PASSWORD = 'admin'
    auth_user_model = get_user_model()
    if not auth_user_model.objects.filter(username='admin').exists():
        admin_user = auth_user_model.objects.create_superuser(
            username='admin', first_name='Andrew', last_name='Thomas',
            email='xenium_ice@hotmail.com', password=DEFAULT_ADMIN_PASSWORD
        )


class WallConfig(AppConfig):
    name = 'wall'
    verbose_name = "Wall"

    def ready(self):
        post_migrate.connect(setup, sender=self)