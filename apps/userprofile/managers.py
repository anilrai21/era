from django.db import models
from django.db.models import QuerySet


class UserProfileManager(models.Manager):
    def user_cart_items(self) -> QuerySet:
        return super().get_queryset()
