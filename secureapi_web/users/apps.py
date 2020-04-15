from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class SuitConfig(DjangoSuitConfig):
    layout = "vertical"


class UsersAppConfig(AppConfig):

    name = "secureapi_web.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass
