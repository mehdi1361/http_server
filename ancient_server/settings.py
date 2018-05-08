"""
Django settings for ancient_server project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q@+unt2eluw--4+uqdtuhi%411lfx@(^n2k3uad%39mq_620)@'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.149', '127.0.0.1', 'ancientsrevival.ir']

# Application definition

INSTALLED_APPS = [
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'objects',
    'django_cron',
    'simple_history',
    'shopping',
    'message',
    'dbbackup',
    'logs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'ancient_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ancient_server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'anc_db',
        'USER': 'postgres',
        'PASSWORD': '13610522',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100000/day',
        'user': '100000000/day'
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


DECK_COUNT = {
    'free': 3,
    'non_free': 4
}
SKIP_GEM = 25
SKIP_GEM_STEP = 50
OPENING_TIME_INDEX = 4

CRON_CLASSES = [
    "objects.crons.FreeChestCreatorJob",
    "objects.crons.Backup",
]

# CHEST_SEQUENCE = ['W', 'W', 'W', 'W', 'S', 'W', 'W', 'W', 'W', 'S', 'W', 'G', 'W', 'W', 'W', 'W', 'S', 'W', 'W', 'W',
#                   'W', 'S', 'W', 'G', 'W', 'W', 'W', 'C', 'W', 'W', 'W', 'S']

CHEST_SEQUENCE = ['W', 'W', 'W', 'W', 'S', 'W', 'W', 'W', 'W', 'S', 'W', 'G', 'W', 'W', 'W', 'W', 'S', 'W', 'W', 'W',
                  'W', 'S', 'W', 'G', 'W', 'W', 'W', 'C', 'W', 'W', 'W', 'S']

CHEST_SEQUENCE_TIME = {
    'W': 4,
    'S': 8,
    'G': 12,
    'C': 24
}

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATIC_URL = '/static/'

# ITEM_UPDATE = {
#     1: {'item_cards': 1, 'coins': 0, 'increase': 0.2},
#     2: {'item_cards': 5, 'coins': 250, 'increase': 0.4},
#     3: {'item_cards': 15, 'coins': 1000, 'increase': 0.6}
# }
#
# UNIT_UPDATE = {
#     1: {'unit_cards': 1, 'coins': 0, 'increase': 0.2},
#     2: {'unit_cards': 5, 'coins': 250, 'increase': 0.4},
#     3: {'unit_cards': 15, 'coins': 1000, 'increase': 0.6},
#     4: {'unit_cards': 30, 'coins': 5000, 'increase': 0.8},
#     5: {'unit_cards': 100, 'coins': 20000, 'increase': 1},
# }
#
# HERO_UPDATE = {
#     1: {'hero_cards': 1, 'coins': 0, 'increase': 0.2},
#     2: {'hero_cards': 5, 'coins': 250, 'increase': 0.4},
#     3: {'hero_cards': 15, 'coins': 1000, 'increase': 0.6}
# }

HERO_UPDATE = {
    1: {'hero_cards': 1, 'coins': 0, 'increase': 0.0},
    2: {'hero_cards': 2, 'coins': 500, 'increase': 0.1},
    3: {'hero_cards': 5, 'coins': 1000, 'increase': 0.21},
    4: {'hero_cards': 10, 'coins': 5000, 'increase': 0.33},
    5: {'hero_cards': 25, 'coins': 10000, 'increase': 0.46},
    6: {'hero_cards': 50, 'coins': 20000, 'increase': 0.61},
    7: {'hero_cards': 125, 'coins': 50000, 'increase': 0.77},
}

ITEM_UPDATE = {
    1: {'item_cards': 1, 'coins': 0, 'increase': 0.0},
    2: {'item_cards': 10, 'coins': 2500, 'increase': 0.1},
    3: {'item_cards': 30, 'coins': 7500, 'increase': 0.21}
}

UNIT_UPDATE = {
    1: {'unit_cards': 1, 'coins': 0, 'increase': 0.0},
    2: {'unit_cards': 2, 'coins': 100, 'increase': 0.1},
    3: {'unit_cards': 5, 'coins': 250, 'increase': 0.21},
    4: {'unit_cards': 10, 'coins': 500, 'increase': 0.33},
    5: {'unit_cards': 25, 'coins': 1000, 'increase': 0.46},
    6: {'unit_cards': 50, 'coins': 2000, 'increase': 0.61},
    7: {'unit_cards': 125, 'coins': 5000, 'increase': 0.77},
    8: {'unit_cards': 250, 'coins': 10000, 'increase': 0.94},
    9: {'unit_cards': 625, 'coins': 20000, 'increase': 1.14},
    10: {'unit_cards': 1250, 'coins': 50000, 'increase': 1.35},
}

JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3600)
}

# TEMPLATE_LOADERS = (
#     ('rtl.loaders.Loader', (
#         'django.template.loaders.filesystem.Loader',
#         'django.template.loaders.app_directories.Loader',
#     )),
# )

# DBBACKUP_STORAGE = 'dbbackup.storage.filesystem_storage'
DBBACKUP_STORAGE_OPTIONS = {'location': 'backup'}
