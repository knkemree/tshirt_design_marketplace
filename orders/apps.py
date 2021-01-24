from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OrdersConfig(AppConfig):
    name = 'orders'

    def ready(self):
        import orders.signals  # noqa



    