import types
from typing import Tuple

from django.db import models
from rest_framework import serializers
from rest_framework.fields import empty

# from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor


def get_base_serializer_class(
    model_class: models.Model,
) -> serializers.SerializerMetaclass:

    serializable_methods = (
        serializable
        for serializable in model_class.serializable()
        if isinstance(
            getattr(model_class, serializable, None), types.FunctionType
        )
    )

    # serializable_foreign_keys = (
    #     (serializable, getattr(model_class, serializable, None).field.model)
    #     for serializable in model_class.serializable()
    #     if isinstance(getattr(model_class, serializable, None), ForwardManyToOneDescriptor)
    # )

    property_methods = (
        serializable
        for serializable in model_class.serializable()
        if isinstance(
            getattr(model_class, serializable, None), type(property())
        )
    )

    class BaseSerializer(serializers.ModelSerializer):
        def __init__(self, instance=None, data=empty, **kwargs):

            for method in serializable_methods:
                setattr(self, method, serializers.SerializerMethodField())

            for method in property_methods:
                setattr(self, method, serializers.ReadOnlyField())
            # for (field, model) in serializable_foreign_keys:
            #     # setattr(self, field, get_base_serializer_class(model)(many=False))
            #     setattr(self, f"{field}__fk", serializers.RelatedField(source=field, read_only=True))

            super(BaseSerializer, self).__init__(instance, data, **kwargs)

        class Meta:
            model = model_class
            fields = model_class.serializable()
            # depth = 0

    return BaseSerializer
