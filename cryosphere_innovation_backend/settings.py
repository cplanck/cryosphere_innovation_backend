"""
Django settings for cryosphere_innovation_backend project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('DEBUG') == 'False':
    DEBUG = False
else:
    DEBUG = True

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['localhost', 'api.cryospherex.com', 'api.cryosphereinnovation.com']

WEBSITE_ROOT = os.getenv('WEBSITE_ROOT')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework.schemas',
    'dj_rest_auth',
    'rest_framework_simplejwt',
    'django_extensions',
    'authentication',
    'instruments',
    'user_profiles',
    'general',
    'django_filters',
    'real_time_data',
    'stats',
    'documentation',
    'storages',
    'algoliasearch_django',
    'django_gsuite_email',
    'notifications'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_EXPOSE_HEADERS = ['Set-Cookie']

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = ['https://cryospherex.com', 'https://www.cryospherex.com','https://cryosphereinnovation.com', 'https://www.cryosphereinnovation.com', 'http://localhost:3000', 'https://dev.cryosphereinnovation.com']

CORS_ALLOW_HEADERS = list(default_headers) + ['Set-Cookie', 'Authorization']

# Added pre-deployment
if(os.getenv('DEBUG') == 'False'):
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False 
    SECURE_HSTS_SECONDS = 60 
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_PRELOAD = True

ROOT_URLCONF = 'cryosphere_innovation_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'cryosphere_innovation_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    },
}

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

DATABASES['default']['TEST'] = {'NAME': 'testdb'}

AWS_STORAGE_BUCKET_NAME = 'cryosphere-innovation-django'
AWS_S3_REGION_NAME = 'us-east-1'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_CUSTOM_DOMAIN = 'd15g1rufdjpafj.cloudfront.net'

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'accesss_token',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',
    'JWT_AUTH_SAMESITE': None,  # I think we need this
    'JWT_AUTH_SECURE': True,
    # This is needed to send the refresh token in the body (4/27/2023)
    'JWT_AUTH_HTTPONLY': True,
    'PASSWORD_RESET_SERIALIZER': 'general.serializers.CustomPasswordResetSerializer',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'authentication.email_authentication_backend.EmailBackend',
]

PASSWORD_RESET_TIMEOUT = 900  # Reset tokens expire after 15 mintues

ALGOLIA = {
    'APPLICATION_ID': '2VQU5R8BW0',
    'API_KEY': '8cfb959eaf00eb09e8e296ef747dae95'
}

EMAIL_BACKEND = 'django_gsuite_email.GSuiteEmailBackend'

DEFAULT_FROM_EMAIL = 'support@cryosphereinnovation.com'

GSUITE_CREDENTIALS_FILE = os.path.join(
    BASE_DIR, 'static/gsuite_email/gsuite_email_creds.json')

SITE_ID = 1

STANDALONE_FRONTEND_ROOT = os.getenv('STANDALONE_FRONTEND_ROOT')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_STORAGE_BUCKET_NAME = 'cryosphere-innovation-django'

AWS_S3_ENDPOINT_URL = 'https://s3.amazonaws.com'
