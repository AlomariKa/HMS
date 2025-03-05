"""
Django settings for healthcare_management project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

from django.conf.global_settings import LOGIN_URL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY')
# Get the database configuration from environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# healthcare_management/settings.py
SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'django.contrib.sites',  # Required for password reset
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'healthcare_management.urls'
import os
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'healthcare_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "//"

# SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS // make sure that all data exchanged between the user and your website is encrypted and secure.
# SESSION_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS // This prevents the cookies from being sent over insecure connections, which could be intercepted by malicious actors.
# CSRF_COOKIE_SECURE = True  # Ensure CSRF cookies are only sent over HTTPS
#
# LOGGING = {
#     'version': 1,  # This is like setting the version of your diary template
#     'disable_existing_loggers': False,  # Keep other existing diaries (loggers) active
#     'handlers': {  # Define where to store your diary entries
#         'file': {
#             'level': 'DEBUG',  # Record all types of events, from minor details to critical issues
#             'class': 'logging.FileHandler',  # Write the entries in a file
#             'filename': 'django_debug.log',  # The name of the diary file
#         },
#     },
#     'loggers': {  # Define the sections of your diary
#         'django': {
#             'handlers': ['file'],  # Use the file handler to store entries
#             'level': 'DEBUG',  # Record all types of events
#             'propagate': True,  # Allow entries to be shared with other sections if needed
#         },
#     },
# }


