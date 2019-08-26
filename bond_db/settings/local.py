from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bonds_db',
        'USER': 'analyst',
        'PASSWORD': 'fakepassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

