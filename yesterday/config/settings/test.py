from __future__ import absolute_import

from .base import *


########## TEST RUNNER CONFIGURATION
# https://github.com/django-nose/django-nose
INSTALLED_APPS += (
    'django_nose',
)

TEST = DEBUG = True

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--where=%s' % PROJECT_FOLDER,
    '--exclude-dir=%s' % join(CONFIG_ROOT, 'settings'),
]
########## END TEST RUNNER CONFIGURATION


########## IN-MEMORY TEST DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_ROOT, 'test.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
########## END IN-MEMORY TEST DATABASE


########## EMAIL CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
########## END EMAIL CONFIGURATION


########## CACHE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'localhost:6379:0',
    }
}
########## END CACHE CONFIGURATION


########## REDIS QUEUE CONFIGURATION
# https://github.com/ui/django-rq#support-for-django-redis-and-django-redis-cache
RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
        'ASYNC': False
    },
    'high': {
        'USE_REDIS_CACHE': 'default',
        'ASYNC': False
    },
    'low': {
        'USE_REDIS_CACHE': 'default',
        'ASYNC': False
    }
}

RQ_SHOW_ADMIN_LINK = True
########## END REDIS QUEUE CONFIGURATION


########## LOGGING CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGERS = {
    # Log queue workers to null but file while testing
    'rq.worker': {
        'handlers': ['null', 'file_log'],
        'level': 'INFO',
        'propagate': False,
    },
    # Log nose test runner only INFO level and above
    'nose.plugins.manager': {
        'handlers': ['default', 'file_log'],
        'level': 'INFO',
        'propagate': False,
    },
}

LOGGING['loggers'].update(LOGGERS)
########## END LOGGING CONFIGURATION
