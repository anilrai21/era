from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = "apps.shop"

    def ready(self):
        from apps.shop.signals import notify_by_email  # noqa
