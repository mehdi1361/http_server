# -*- coding: utf-8 -*-

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
from local_setting import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
TIME_ZONE = 'Asia/Tehran'
SECRET_KEY = 'q@+unt2eluw--4+uqdtuhi%411lfx@(^n2k3uad%39mq_620)@'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True


ALLOWED_HOSTS = ['192.168.1.149', '127.0.0.1', 'ancientsrevival.ir', 'localhost']

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
    'reports',
    'system_settings',
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
        'NAME': DATABASE,
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
    'free': 10,
    'non_free': 4
}
SKIP_GEM = 25
SKIP_GEM_STEP = 50
OPENING_TIME_INDEX = 4

CRON_CLASSES = [
    "objects.crons.FreeChestCreatorJob",
    "objects.crons.Backup",
    "objects.crons.LeagueReset",
    "objects.crons.FakeUserGame",
    "objects.crons.CafeBazarRefreshToken",
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

# PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
#
# STATIC_URL = '/static/'

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
    0: {'hero_cards': 1, 'coins': 0, 'increase': 0.0},
    1: {'hero_cards': 1, 'coins': 0, 'increase': 0.0},
    2: {'hero_cards': 2, 'coins': 500, 'increase': 0.1},
    3: {'hero_cards': 5, 'coins': 1000, 'increase': 0.21},
    4: {'hero_cards': 10, 'coins': 5000, 'increase': 0.33},
    5: {'hero_cards': 25, 'coins': 10000, 'increase': 0.46},
    6: {'hero_cards': 50, 'coins': 20000, 'increase': 0.61},
    7: {'hero_cards': 125, 'coins': 50000, 'increase': 0.77},
}

ITEM_UPDATE = {
    0: {'item_cards': 1, 'coins': 0, 'increase': 0.0},
    1: {'item_cards': 1, 'coins': 0, 'increase': 0.0},
    2: {'item_cards': 10, 'coins': 2500, 'increase': 0.1},
    3: {'item_cards': 30, 'coins': 7500, 'increase': 0.21}
}

UNIT_UPDATE = {
    0: {'unit_cards': 1, 'coins': 0, 'increase': 0.0},
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


COOL_DOWN_UNIT = {
    0: {'time': 200,  'skip_gem': 5,  'add_time': 2},
    1: {'time': 200,  'skip_gem': 5,  'add_time': 2},
    2: {'time': 300,  'skip_gem': 10, 'add_time': 5},
    3: {'time': 400,  'skip_gem': 15, 'add_time': 10},
    4: {'time': 500,  'skip_gem': 20, 'add_time': 20},
    5: {'time': 600,  'skip_gem': 25, 'add_time': 30},
    6: {'time': 700,  'skip_gem': 30, 'add_time': 45},
    7: {'time': 800,  'skip_gem': 35, 'add_time': 60},
    8: {'time': 900,  'skip_gem': 40, 'add_time': 90},
    9: {'time': 1000, 'skip_gem': 45, 'add_time': 120},
    10: {'time': 1100, 'skip_gem': 50, 'add_time': 180}
}


COOL_DOWN_TIME = 300

LEAGUE_LENGTH = 7

NUM_GAMES = 3

TAP_SELL_URL = "http://api.tapsell.ir/v2/suggestions/validate-suggestion"

TAPLIGH_URL = "http://api.tapligh.com/valid/token"
TAPLIGH_VERIFY_TOKEN = 'BO0D3I6NZM6FI8UHCYSZZBBDOLGBJS'
TAPLIGH_SDK_VERSION = '2.0.3'
TAPLIGH_PACKAGE_NAME = 'com.tapligh.sdk'


SUB_COOLDOWN_TROOP = 1800
SUB_OPENING_CHEST = 3600

ACCOUNT_REGISTER_BENEFIT = 100


FAKE_USER = ["محمود",
             "احمد",
             "احمد آقا",
             "مصطفی",
             "میر مهدی",
             "شب خوب",
             "چوگاس",
             "ولکوز",
             "گوی بلورین",
             "هشدرخان",
             "تتلو",
             "رضا",
             "سمیه",
             "دلار جهانگیری",
             "خرزو خان",
             "میر قاراشمیش",
             "پایتون",
             "کانتر لاجیک",
             "رندوم لاجیک",
             "آلفرد هیچکاک",
             "استاد اسدی",
             "شمائی زاده",
             "غول مرحله آخر",
             "صمصام",
             "کیانو",
             "عادل پور",
             "فردوپوس",
             "نتیجة الپراید",
             "غول نارمک",
             "پینک فلوید",
             "پژمان",
             "ولبورن",
             "مارشال",
             "پسقل",
             "چیترا",
             "میلاد",
             "بابک",
             "شعبون",
             "سجاد",
             "کارون",
             "شکوفه",
             "اقبال",
             "فرمانده",
             "شهرام",
             "تریتا",
             "یاس سفید",
             "پارسا",
             "مهربینا",
             "الوند",
             "سرو",
             "کامبو",
             "فازسه",
             "شکیلا",
             "اعظم",
             "صلاح",
             "شورانگیز",
             "لواشک",
             "گرگینه",
             "آفتاب شرقی",
             "پاندورا",
             "قیمت",
             "کروو اتانو",
             "امیلی کالدوین",
             "سیدر",
             "ابن سینا",
             "داش ابرام",
             "گاندو",
             "ژینوس",
             "آلفا",
             "رادیکال باز",
             "کروشه به توان دو ",
             "شاهکار",
             "سلیمان",
             "ونداد",
             "هستی",
             "همایون",
             "بهمنیار",
             "آگوست",
             "بنیامین",
             "محمدعلی",
             "قباد",
             "عمه ملوک",
             "معین",
             "آمنه",
             "دیبا",
             "صدرا",
             "پوست پیاز",
             "چنگیز ",
             "بیژن ",
             "امیر حسین",
             "محمد جواد ",
             "مش قنبر",
             "کیکاووس",
             "کامیار",
             "گل بانو",
             "کوکب",
             "صفدر",
             "اعلا",
             "طهمورث",
             "خشایار",
             "آرش کمانگیر",
             "غلام ",
             "قلی",
             "خسرو",
             "بهنام",
             "شکارچی شب",
             "پلنگ صورتی",
             "قلیدون",
             "شایان",
             "سیمین دخت",
             "کوژین",
             "نارما",
             "کفشدوزک",
             "قاصدک",
             "کولبر",
             "پاگنده",
             "بنز",
             "نوید",
             "امید",
             "چکامه",
             "فریبرز",
             "جواد",
             "رامین",
             "هرود",
             "آنخماهو",
             "چلیپا",
             "لیلی",
             "عبدعلی",
             "ثریا",
             "صمد",
             "ضیا",
             "سامانتا",
             "پیکان",
             "یوسف",
             "واهیک",
             "مه رو",
             "مبارک",
             "کادیلاک",
             "سپر سیاوش",
             "سیاووشان",
             "قداره",
             "دشنه",
             "دمپایی ابری",
             "اسفندیار",
             "بهرام",
             "ننه حسن",
             "اتلو",
             "کابوی",
             "پدرام",
             "پویا",
             "نریمان",
             "بابا طاهر عریان",
             "رویا",
             "وحید",
             "طاهر",
             "آتیلا",
             "تیلدا",
             "مراد",
             "خشم ژیان",
             "ناربیا",
             "هیولا ",
             "کریم",
             "مریم",
             "اژدر",
             "کوروش",
             "گرگ زخمی",
             "بردیا",
             "لیلا",
             "رستم",
             "سهراب",
             "مرد نامرئی",
             "تنها ",
             "کیارش",
             "علی",
             "امیرعلی",
             "ارسطو",
             "نقی",
             "قاتل حرفه ای",
             "لئون",
             "پیلتن",
             "پلنگ سیاه ",
             "مهدی",
             "میثاق",
             "بابک ",
             "پرویز",
             "ستاره ",
             "خرم الدین",
             "ارسلان ",
             "دلاور",
             "plaxis",
             "yalda999",
             "shirazkit",
             "B_irooni_B",
             "alalela",
             "Dante70",
             "curVo_IR",
             "melisa-vb",
             "Kingjoon",
             "FirePersian",
             "Sinajeyjey",
             "FonixLight",
             "Mamalili",
             "Kotlas",
             "Lordofflash",
             "Emam_Qome_Joom",
             "ee_man",
             "sa_sun",
             "mo_in",
             "m000_in",
             "pol_B_pol",
             "Do_Dost",
             "AR@M",
             "LOL._.LOL",
             "DotaDo",
             "2ta2",
             "VgaGames",
             "Signull",
             "Clashtoor",
             "yasamarde",
             "...@mi@...",
             "master-pro",
             "Need For Fight",
             "TyFoon",
             "Poyan-SN",
             "CallfD3",
             "PesMan",
             "FiFarhad",
             "..((Saga3))..",
             ":://nazanin\\::",
             "**Sa-Naz**",
             "ParwinLose",
             "ultradesigner",
             "Nivar",
             "Septic_96",
             "Elena_53",
             "Violet18",
             "Sevda2",
             "Aloochak",
             "__Mehri__",
             "Milad._.Red",
             "Amee(:)",
             "VooLeK",
             "Mahtab086",
             "Mirho3ein",
             "Mah_MM",
             "eeeeehsan",
             "Narjesd",
             "Patteerr",
             "MelodySoL",
             "8_B_8",
             "Par3",
             "Per3Polic",
             "SteQLaaL",
             "QuooLo",
             "javadix",
             "Navid6219",
             "Wisgoon2000",
             "MohamadBlue8",
             "aminig",
             "Livepor57",
             "LFCLiV8",
             "Omid@M",
             "DavidBeck@",
             "Mo.Salimi",
             "Sun_Sky11",
             "Just_Red",
             "armana",
             "Cati",
             "FaFar80",
             "Memolikka",
             "LimoooL",
             "S1a2m3",
             "Baraanaa",
             "QuQnuS",
             "MoooFerferi",
             "روسونری تهران",
             "موفرفری",
             "آوسین",
             "ژولیا 5",
             "سیمین-ناز",
             "ماهیرخ",
             "بابای آیدین"
             ]

CAFE_BAZAR_CLIENT_ID = 'ySK9GZE7hfrXP5rukViMmsGSCpg2dBJsQDhtzLzQ'
CAFE_BAZAR_CLIENT_SECRET = 'mVgkvbLFPjog2mw3o9LjefNBxenSh6bgUS8EYwCVNz1fh3FSipzXqmqPZuf9'
CAFE_BAZAR_REFRESH_TOKEN_URL = "https://pardakht.cafebazaar.ir/devapi/v2/auth/token/"

STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
#     # '/var/www/static/',
# ]
STATIC_ROOT = os.path.join(BASE_DIR, "static")
USE_THOUSAND_SEPARATOR = True

# LOGIN_REDIRECT_URL = '/employee/login'
