from decouple import config
import os
from django.conf import settings

DEBUG = False
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'infinity',
            'USER': 'infinity',
            'PASSWORD': 'infinity@snakescript',
            'HOST': 'localhost',
            'PORT': 5432,
        }
    }

STATIC_ROOT = os.path.join(settings.BASE_DIR, 'static')

CURRENCY_API_KEY = config('CURRENCY_API_KEY')
