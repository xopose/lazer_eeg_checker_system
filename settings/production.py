import os

from .base import *


DEBUG = config("DEBUG", default=False, cast=bool)

INTERNAL_IPS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "lazer-mne",
        "USER": "postgres",
        "PASSWORD": "xxxx",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
