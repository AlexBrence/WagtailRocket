from .base import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{PROJECT_DIR}.settings.production')

ALLOWED_HOSTS = ['*']
DEBUG = False
#CSRF_TRUSTED_ORIGINS = ['https://*.CHANGE_ME.com']
CSRF_TRUSTED_ORIGINS = ['https://*.wagtailrocket.com']
COMPRESS_ENABLED = True 
COMPRESS_OFFLINE = True 

# Postgres
DATABASES = {
    'default': {
        'ENGINE': env("SQL_ENGINE"),
        'NAME': env("SQL_DATABASE"),
        'USER': env("SQL_USER"),
        'PASSWORD': env("SQL_PASSWORD"),
        'HOST': env("SQL_HOST"),
        'PORT': env("SQL_PORT"),
    }
}


# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_errors.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
