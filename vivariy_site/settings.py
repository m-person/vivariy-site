"""
Django settings for project vivariy_site.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'web6*qg*0nf@$tswn83z(a6^8tu59g*@lr58f=37val(vvjgvu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

ADMINS = [('Andrey, andrey@localhost')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'debug_toolbar',
    'ckeditor',
    'ckeditor_uploader',
    'versatileimagefield',
    'tagging',
    'tagging_autocomplete',
    'smuggler',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vivariy_site.urls'

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

WSGI_APPLICATION = 'vivariy_site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vivariy_site',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '192.168.99.100',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#
MEDIA_ROOT = os.path.join(BASE_DIR, 'app', 'media')

MEDIA_URL = '/media/'

# ckeditor file uploader
CKEDITOR_UPLOAD_PATH = 'ck_uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'

LOCALE_PATHS = [os.path.join(BASE_DIR, 'app', 'locale')]

# django-smuggler setup (db backups)
SMUGGLER_FIXTURE_DIR = os.path.join(BASE_DIR, 'db_dumps')

# email settings:
if DEBUG:
    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST = '127.0.0.1'
    EMAIL_PORT = 2525
    DEFAULT_FROM_EMAIL = 'django-dev@localhost'
# EMAIL_HOST_PASSWORD
# EMAIL_HOST_USER
# EMAIL_SUBJECT_PREFIX
# EMAIL_USE_TLS
# EMAIL_USE_SSL
# EMAIL_SSL_CERTFILE
# EMAIL_SSL_KEYFILE
# EMAIL_TIMEOUT


# django-resized defaults:
# DJANGORESIZED_DEFAULT_QUALITY = 99
# DJANGORESIZED_DEFAULT_KEEP_META = False

# enable caching in database. The sorl-thumbnail requires it (or similar key-value storage: memcached, redis).
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'app_cache_table',
#         'TIMEOUT': 0,
#     }
# }


SESSION_SAVE_EVERY_REQUEST = True

# versatile image section
VERSATILEIMAGEFIELD_SETTINGS = {
    # The amount of time, in seconds, that references to created images
    # should be stored in the cache. Defaults to `2592000` (30 days)
    'cache_length': 3600 * 24 * 365,
    # The name of the cache you'd like `django-versatileimagefield` to use.
    # Defaults to 'versatileimagefield_cache'. If no cache exists with the name
    # provided, the 'default' cache will be used instead.
    'cache_name': 'versatileimagefield_cache',
    # The save quality of modified JPEG images. More info here:
    # http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html#jpeg
    # Defaults to 70
    'jpeg_resize_quality': 95,
    # The name of the top-level folder within storage classes to save all
    # sized images. Defaults to '__sized__'
    'sized_directory_name': '__sized__',
    # The name of the directory to save all filtered images within.
    # Defaults to '__filtered__':
    'filtered_directory_name': '__filtered__',
    # The name of the directory to save placeholder images within.
    # Defaults to '__placeholder__':
    'placeholder_directory_name': '__placeholder__',
    # Whether or not to create new images on-the-fly. Set this to `False` for
    # speedy performance but don't forget to 'pre-warm' to ensure they're
    # created and available at the appropriate URL.
    'create_images_on_demand': True
}

# VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
#     'image_gallery': [
#         ('gallery_large', 'crop__800x450'),
#         ('gallery_square_small', 'crop__50x50')
#     ],
#     'primary_image_detail': [
#         ('hero', 'crop__600x283'),
#         ('social', 'thumbnail__800x800')
#     ],
#     'primary_image_list': [
#         ('list', 'crop__400x225'),
#     ],
#     'headshot': [
#         ('headshot_small', 'crop__150x175'),
#     ]
# }

# django-tagging settings:
FORCE_LOWERCASE_TAGS = True

# django-tagging-autocomplete settings:
TAGGING_AUTOCOMPLETE_SEARCH_CONTAINS = True

# Deployment: import local_settings file to override
try:
    from .prod_settings import *
except ImportError:
    pass

    # try:
    #     INSTALLED_APPS += LOCAL_INSTALLED_APPS
    #     ALLOWED_HOSTS += LOCAL_ALLOWED_HOSTS
    # except:
    #     pass
