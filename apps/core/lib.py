from django.template.defaultfilters import slugify


def make_valid_alias(name: str) -> str:
    return slugify(name)
