from .base import *
import os

DEBUG = True

SECRET_KEY = '0nvp)2o93(=7f$j5siuu9e$v-w^2_ho7*fpiitfyfuh(*1)v34'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
