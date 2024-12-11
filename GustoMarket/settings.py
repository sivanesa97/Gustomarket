"""
Django settings for GustoMarket project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from django.utils.translation import gettext_lazy as _
from pathlib import Path
import os
import environ
env = environ.Env()
environ.Env.read_env()
# from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'Services/templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-9do%^ulb0=h(_fux7o1kuz@5rm7_c&a@5mxb-vryxr!iqj2r1r'
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['platform.gustomarket.co',
                 'www.platform.gustomarket.co', 'localhost', '127.0.0.1', '192.168.1.7']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Services.apps.ServicesConfig',
    'django_filters',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'Services.middleware.CurrentUserMiddleware',
]
#     'language.DefaultLanguageMiddleware',
ROOT_URLCONF = 'GustoMarket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'Services.context_processors.context_processors.language_flags',
                'Services.context_processors.context_processors.profile_picture',
            ],
            'libraries': {
                'custom_tags': 'Services.templatetags.custom_tags'
            }
        },
    },
]

WSGI_APPLICATION = 'GustoMarket.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}


EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env('FROM_EMAIL')
EMAIL_HOST = env('HOST')
EMAIL_PORT = env('PORT', cast=int)
EMAIL_HOST_USER = env('HOST_USER')
EMAIL_HOST_PASSWORD = env('HOST_PASSWORD')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'
USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
    ('ar', _('Arabic')),
    ('es', _('Spanish')),
    ('zh', _('Chinese')),
    ('ja', _('Japanese')),
    ('fr', _('French')),
    ('de', _('German')),
    ('hi', _('Hindi')),
    ('iw', _('Hebrew')),
]
LANGUAGE_FLAGS = {
    'en': 'flag-icon-us',
    'ar': 'flag-icon-sa',
    'es': 'flag-icon-es',
    'zh': 'flag-icon-cn',
    'ja': 'flag-icon-jp',
    'fr': 'flag-icon-fr',
    'de': 'flag-icon-de',
    'hi': 'flag-icon-in',
    'iw': 'flag-icon-il',
}
LOCALE_PATHS = [
    # optional, if you want to store translations in a 'locale' directory
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# Directory for 'collectstatic' to store static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET')

GUSTOMARKET_FEE = 0.02
X_FRAME_OPTIONS = 'SAMEORIGIN'