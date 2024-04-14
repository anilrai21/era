import uuid

from django.utils.text import slugify


def get_valid_alias(instance) -> str:
    alias = slugify(instance.name)

    while True:
        model_class = type(instance)
        queryset = model_class.objects.filter(alias=alias).exclude(
            pk=instance.pk
        )

        if queryset:
            if instance.alias:
                alias = f"{instance.alias}{uuid.uuid4()}"
            else:
                alias = uuid.uuid4()
        else:
            return alias
