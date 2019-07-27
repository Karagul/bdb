from .base import *
import os

DEBUG = False

assert SECRET_KEY is not None, ('Provide DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS += [os.getenv('DJANGO_ALLOWED_HOSTS'),]

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
