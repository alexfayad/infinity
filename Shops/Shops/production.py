from decouple import config

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


CURRENCY_API_KEY = config('CURRENCY_API_KEY')
