# from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            # 'static': staticfiles_storage.url,
            "url": reverse,
        }
    )
    return env
