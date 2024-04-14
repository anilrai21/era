from django.db import models
from django.db.models import Q, QuerySet


class SocialMediaManager(models.Manager):
    def active(self) -> QuerySet:
        return super().get_queryset().filter(Q(active=True))
