"""
Django settings for myspending project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import sys
from pathlib import Path
import environ
import asyncio
import loguru

# Это отсюда https://django-environ.readthedocs.io/en/latest/quickstart.html
env = environ.Env(
    # set casting, default value
    DEBUG=(bool),     # Для переменной DEBUG указываем тип данных, когда достаём из .env
    SECRET_KEY=(str),
    DOMAIN_NAME=(str),
    REDIS_HOST=(str),
    REDIS_PORT=(str),
    DATABASE_NAME=(str),
    DATABASE_USER=(str),
    DATABASE_PASSWORD=(str),
    DATABASE_HOST=(str),
    DATABASE_PORT=(str),
    TG_API_ID=(str),
    TG_API_HASH=(str),
    BOT_TOKEN=(str),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
# Это отсюда https://django-environ.readthedocs.io/en/latest/quickstart.html
environ.Env.read_env(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']
DOMAIN_NAME = env('DOMAIN_NAME')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # собственные приложения
    'spending.apps.SpendingConfig',

    # сторонние приложения
    'rest_framework',
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

ROOT_URLCONF = 'myspending.urls'

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

WSGI_APPLICATION = 'myspending.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = '/media/'   # путь в адресной строке для получения медиа-файлов
MEDIA_ROOT = BASE_DIR / 'uploads'    # путь к медиа-файлам на диске


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery settings
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"    # Это адрес брокера сообщений (у нас Redis)
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}"    # Это адрес бэкэнда результатов (тоже у нас Redis)
CELERY_TIMEZONE = "Europe/Moscow"   # Временная зона для Celery
CELERY_BEAT_SCHEDULE = {    # Настройки шедуля
    'my_task': {
        'task': 'first_word.tasks.scheduled_task_example',
        'schedule': 60 * 60  # Время в секундах между запусками задач
    }
}

# Настройки логгера
MY_LOGGER = loguru.logger
MY_LOGGER.remove()  # Удаляем все предыдущие обработчики логов
MY_LOGGER.add(sink=sys.stdout, level='DEBUG')   # Все логи от DEBUG и выше в stdout
MY_LOGGER.add(  # системные логи в файл
    sink=f'{BASE_DIR}/logs/sys_log.log',
    level='DEBUG',
    rotation='10 MB',
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

# Настройки для pyrogram
TG_API_ID = env('TG_API_ID')
TG_API_HASH = env('TG_API_HASH')
BOT_TOKEN = env('BOT_TOKEN')
TELEGRAM_CLIENTS_DCT = dict()   # Тут храним объекты клиентов (нужно для авторизации)
TELEGRAM_AUTH_RESULTS = dict()  # Тут храним ответы на запросы (нужно для авторизации)

# Определяем event loop для асинхронной работы pyrogram
LOOP = asyncio.new_event_loop()
asyncio.set_event_loop(LOOP)
