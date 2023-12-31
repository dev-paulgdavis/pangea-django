"""
Django settings for news project.

Generated by 'django-admin startproject' using Django 4.2.4.

"""
import os

from pathlib import Path

import pangea.exceptions as pe
from pangea.config import PangeaConfig
from pangea.services.vault.models.common import KeyPurpose
from pangea.services.vault.models.symmetric import SymmetricAlgorithm
from pangea.services.vault.vault import Vault
from pangea.utils import str2str_b64

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'replace with your own secret key'

# Setup Pangea imports
from dotenv import load_dotenv
load_dotenv()
import os,time
# There are two environmental parameters that you need to define 
# for the VAULT token and the Pangea domain
token = os.getenv("PANGEA_VAULT_TOKEN")
domain = os.getenv("PANGEA_DOMAIN")

try:
    config = PangeaConfig(domain=domain)
except:
    print("Failed to set domain")
    sys.exit(1)

try:    
    vault = Vault(token, config=config)
except:
    print("Failed to connect to vault")
    sys.exit(1)

name = f"Retrieve news website secrets {int(time.time())}"

# Retrieve the database password
response = vault.get(
    id="Replace with Secret vault id of your stored db password",
    version=1,
    verbose=True,
)
database_password = response.raw_result['current_version']['secret']

# We are retrieving the openai password
response = vault.get(
    id="Replace with your API key",
    version=1,
    verbose=True,
)

# Make sure to use all capitals if you want to share this value across models
OPENAI_API_KEY = response.raw_result['current_version']['secret']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['news.digitalexperience.agency', '127.0.0.1', '172.104.23.205']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'django_tables2',
    'widget_tweaks',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

# I use WSGI with Django and this specifies the wsgi file
WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Notice that I specify the PASSWORD and use the retrieved password from the vault

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'newsroom',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'newsreport01',
        'PASSWORD': database_password
    },
}


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


