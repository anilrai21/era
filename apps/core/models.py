from typing import Tuple

from django.db import models


class AbstractSerializerModel(models.Model):
    class Meta:
        abstract = True

    _serializable = ()
    _short_serializable = ()

    @classmethod
    def serializable(cls, short: bool = False) -> Tuple:
        if short:
            return cls._short_serializable
        else:
            return cls._serializable


class TimestampAbstractModel(AbstractSerializerModel):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    _serializable = ("created", "modified")
    _short_serializable = ("created", "modified")
