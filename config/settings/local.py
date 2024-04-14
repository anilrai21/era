from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

# INSTALLED_APPS += (
#     'debug_toolbar', # and other apps for local development
# )

# MIDDLEWARE += [
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# ]

INTERNAL_IPS = ("127.0.0.1", "localhost")

CSRF_COOKIE_SECURE = False
