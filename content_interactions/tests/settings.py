# coding=utf-8

DEBUG = True

SITE_ID = 1

SECRET_KEY = 'blabla'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
    },
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'south',
    'widget_tweaks',
    'social_graph',
    'content_interactions_stats',
    'content_interactions_monitoring',
    'content_interactions',
    'content_interactions.tests'
]

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)


USE_I18N = True

USE_L10N = True


ROOT_URLCONF = 'content_interactions.tests.urls'


COMMENT_MAX_LENGTH = 3000