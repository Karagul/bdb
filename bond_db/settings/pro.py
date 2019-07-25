from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bonds_db',
        'USER': 'analyst',
        'PASSWORD': 'downdown',
        'HOST': 'localhost',
        'PORT': '5432',

    }
}

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
