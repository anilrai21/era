from django.apps import AppConfig


class UserprofileConfig(AppConfig):
    name = "apps.userprofile"

    def ready(self):
        from apps.userprofile.signals import create_userprofile  # noqa
