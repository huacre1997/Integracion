"""
Django settings for pjConsumer project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Leer variables 
# env = environ.Env(DEBUG=(bool, False))
# base = environ.Path(__file__)
# environ.Env.read_env(env_file=base('../../.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pnfnh$12%rkgz*kf81$1jbzc$f-5)i5ago4f!#7si6m0jr5_(c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False    

# ALLOWED_HOSTS = [".herokuapp.com"]
ALLOWED_HOSTS = ["*",".herokuapp.com"]

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    "environ",
    'storages',
    "collectfast",
    'simple_history',

]

LOCAL_APPS = [
 
    'Web',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

BOOTSTRAP4 = {
    'include_jquery': True,
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',


]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app.context_processor.permission',
            ],
        },
    },
]
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
WSGI_APPLICATION = 'app.wsgi.application'



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': "vg35",
#         # "HOST": "macbook-pro-de-jackeline.local",
#         "HOST":"localhost",
#         "USER": "root",
#         "PASSWORD": "",
#         "PORT": ""
#     }
# }

# DATABASES = {

#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': "bdprueba",
#         "HOST": "localhost",
#         "USER": "root",
#         "PASSWORD": "",
#         "PORT": ""
#     }
# }


# CACHES = {
#     'default': {
#         # Your default cache
#     },
#     'collectfast': {
#         # Your dedicated Collectfast cache
#     },
# }

COLLECTFAST_CACHE = 'collectfast'
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': "bdprueba",
#         "HOST": "localhost",
#         "USER": "postgres",
#         "PASSWORD": "123",
#         "PORT": 5432
#     }
# }

import dj_database_url
from decouple import config
DATABASES={
    "default":dj_database_url.config(
        default=config("DATABASE_URL")
    )
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Lima'

SITE_ID = 1

USE_I18N = True

USE_L10N = False
THOUSAND_SEPARATOR="."
USE_TZ = False
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

AWS_ACCESS_KEY_ID = 'AKIAVTWEJMBX5NYJYD6Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'vg365'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
# AWS_S3_ENDPOINT_URL="s3.sa-east-1.amazonaws.com"
AWS_DEFAULT_ACL=None
AWS_S3_REGION_NAME="sa-east-1"
AWS_S3_FILE_OVERWRITE=False
AWS_LOCATION = 'static'
AWS_QUERYSTRING_AUTH = False
LOGIN_REDIRECT_URL="/"
LOGIN_URL="/login/"
# STATIC_URL = "https://s3-sa-east-1.amazonaws.com/%s/static/" % AWS_STORAGE_BUCKET_NAME
STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
STATICFILES_LOCATION = 'static'
# STATICFILES_STORAGE = 'custom_storages.StaticStorage'
# COLLECTFAST_STRATEGY = "collectfast.strategies.boto3.Boto3Strategy"
STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_ROOT = ''
STATIC_ROOT=os.path.join(BASE_DIR,"staticfiles")
MEDIA_URL = "https://s3-sa-east-1.amazonaws.com/%s/media/" % AWS_STORAGE_BUCKET_NAME

AUTH_USER_MODEL="Web.Usuario"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
MAILER_EMAIL_BACKEND = EMAIL_BACKEND  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_HOST_PASSWORD = 'qskwjjelhrpkyyra'  
EMAIL_HOST_USER = 'huacreenciso97@gmail.com'  
EMAIL_PORT = 465  
EMAIL_USE_SSL = True  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER