from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "market.orders"

    def ready(self):
        import market.orders.signals
