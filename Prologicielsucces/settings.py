"""
Django settings for Prologicielsucces project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4b4s@z1apg3h&&3w@-v^i#-096pk69q$so8x7^jlhr7&v_cv7v"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['127.0.0.1', 'localhost',  "http://localhost:39553"]

handler404 = "finances.views.custom_404_view"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'finances',
    'accounts',
    'corsheaders',
    'rest_framework',
    'widget_tweaks',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = "Prologicielsucces.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Prologicielsucces.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db.khaa',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "fr"
TIME_ZONE = "Africa/Abidjan"

USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
# Autres configurations ...image a la API

# Configuration pour les fichiers médias (images)
#MEDIA_URL = 'Mediatheques/'
#MEDIA_ROOT = os.path.join(BASE_DIR, '')


# Configuration pour les fichiers médias (images)
MEDIA_ROOT = os.path.join(BASE_DIR, 'Mediatheques')
MEDIA_URL = '/Mediatheques/'
# Configuration pour les documents



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.Utilisateurs"
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # pour Flutter Web
    "http://localhost:8000",  # pour le développement Django
    "http://localhost:34269"
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'OPTIONS',  # N'oubliez pas d'inclure OPTIONS pour gérer les requêtes préalables
]

CORS_ALLOW_HEADERS = [
    'Content-Type',
    'X-CSRFToken',  # Assurez-vous d'inclure X-CSRFToken
    # Ajoutez d'autres en-têtes autorisés si nécessaire
]

# settings.py
LOGIN_URL = '/accounts/login/'

#charte de style et couleurs
#couleur principale: style: TextStyle(color: Color(0xFF006B89))
#Couleur secondaire : jaune
#Colors.white, // Text color
#color: Color.fromARGB(255, 122, 124, 124),
#border: OutlineInputBorder(
#borderRadius: BorderRadius.circular(8),
#borderSide: BorderSide( color: Colors.grey,