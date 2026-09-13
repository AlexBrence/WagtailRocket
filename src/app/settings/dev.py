from .base import *


# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
ALLOWED_HOSTS = ['*']

# if 'DJANGO_ALLOWED_HOSTS' in os.environ:
#     ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(' ')

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = INSTALLED_APPS + [
    "debug_toolbar",
]

MIDDLEWARE = MIDDLEWARE + [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ('127.0.0.1',)

try:
    from .local import *
except ImportError:
    pass
