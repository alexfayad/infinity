"""
Django settings for Shops project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='oxr#QHz4TRbqMw8G82uujfdsf213321')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config("DEBUG", default=True)
DEBUG = False

ALLOWED_HOSTS = [
    '*',
    '127.0.0.1',
    'localhost',
    'Shops.fbmqgxuxev.us-west-2.elasticbeanstalk.com',
    'infinity.supply',
    '159.65.220.179',
]

# Application definition

INSTALLED_APPS = [
    'django_redis',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'core',
    'django_celery_results',
    'django_celery_beat',
    'corsheaders',
    'Shops',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'Shops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Shops.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if not DEBUG:
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
else:
    # PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': os.path.join(PROJECT_DIR, 'infinity.db'),
    #     }
    # }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config("LOCAL_DATABASE_NAME", default="infinity"),
            'USER': config("LOCAL_DATABASE_USER", default="snake"),
            'PASSWORD': config("LOCAL_DATABASE_PASSWORD", default="snake"),
            'HOST': 'localhost',
            'PORT': 5432,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            config("REDIS_LOCATION", default="redis://127.0.0.1:6379/1")
        ],
        'OPTIONS': {
            # 'DB': 0,
            # 'MASTER_CACHE': config("MASTER_CACHE", default="redis://127.0.0.1:6379/1"),
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
    }
}

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379') 
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='django-db')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE


CELERY_CONFIGURATION = {
    'broker_url': config('CELERY_BROKER_URL', default='Elasticache') ,
    'beat_scheduler': "django_celery_beat.schedulers:DatabaseScheduler",
    'beat_schedule': {
        'parsing': {
            'task': 'core.tasks.parse',
            'schedule': 3 * 60.0 * 60.0
        }
    },

    'beat_sync_every': 1
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# API keys
#CURRENCY_API_KEY = config('CURRENCY_API_KEY')
CURRENCY_API_KEY = 'sfklsfslkdjfsldf'

from Shops.aws.conf import *  # noqa
