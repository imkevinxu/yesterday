"""Production settings and globals."""

from __future__ import absolute_import

from .base import *

import os


########## HOST CONFIGURATION
# https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = [PROJECT_DOMAIN, '.herokuapp.com', 'localhost', '127.0.0.1']
########## END HOST CONFIGURATION


########## SECRET CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = os.environ['SECRET_KEY']
########## END SECRET CONFIGURATION


########## EMAIL CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = '%s Team <contact@%s>' % (PROJECT_NAME, PROJECT_DOMAIN)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'smtp.gmail.com'

# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 587

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')

# https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {}
DATABASES['default'] = dj_database_url.config()
########## END DATABASE CONFIGURATION


########## TEMPLATE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
########## END TEMPLATE CONFIGURATION


########## LOGGING CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGERS = {
    # Log queue workers to console and file on development
    'rq.worker': {
        'handlers': ['default', 'file_log'],
        'level': 'INFO',
        'propagate': False,
    }
}

LOGGING['loggers'].update(LOGGERS)
########## END LOGGING CONFIGURATION


########## SECURITY CONFIGURATION
# http://django-secure.readthedocs.org/en/v0.1.2/settings.html
# INSTALLED_APPS += (
#     'djangosecure',
# )
#
# MIDDLEWARE_CLASSES += (
#     'djangosecure.middleware.SecurityMiddleware',
# )
#
# # Honor the 'X-Forwarded-Proto' header for request.is_secure()
# # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECURE_PROXY_SSL_HEADER
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#
# # Use this setting if SSL is being served through CloudFlare proxy
# SECURE_PROXY_SSL_HEADER = ('HTTP_CF_VISITOR', '{"scheme":"https"}',)
#
# # Set this to 30 seconds and then to 518400 when you can prove it works
# SECURE_HSTS_SECONDS = 30
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_FRAME_DENY = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
########## END SECURITY CONFIGURATION


########## CACHE/QUEUE CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
RQ_QUEUES = {}

if 'REDISCLOUD_URL' in os.environ:
    redis_url = os.environ['REDISCLOUD_URL']

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': '%s/%s' % (redis_url, 0),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

    RQ_QUEUES = {
        'default': {
            'USE_REDIS_CACHE': 'default'
        },
        'high': {
            'USE_REDIS_CACHE': 'default'
        },
        'low': {
            'USE_REDIS_CACHE': 'default'
        }
    }

    RQ_SHOW_ADMIN_LINK = True

    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
########## END CACHE/QUEUE CONFIGURATION


########## AMAZON S3 CONFIGURATION
# http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html
if 'AWS_ACCESS_KEY_ID' in os.environ:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    INSTALLED_APPS += (
        'storages',
        'collectfast'
    )

    AWS_S3_SECURE_URLS = True
    AWS_QUERYSTRING_AUTH = False
    AWS_PRELOAD_METADATA = True

    AWS_EXPIREY = 60 * 60 * 24 * 7
    AWS_HEADERS = {
        'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIREY, AWS_EXPIREY)
    }

    # Separate buckets for static files and media files
    AWS_STATIC_STORAGE_BUCKET_NAME = '%s-static' % PROJECT_NAME.lower()
    AWS_MEDIA_STORAGE_BUCKET_NAME = '%s-media' % PROJECT_NAME.lower()
    S3_STATIC_URL = '//%s.s3.amazonaws.com/' % AWS_STATIC_STORAGE_BUCKET_NAME
    S3_MEDIA_URL = '//%s.s3.amazonaws.com/' % AWS_MEDIA_STORAGE_BUCKET_NAME

    # Using django-pipeline along with S3 storage for staticfiles
    # https://django-pipeline.readthedocs.org/en/latest/storages.html#using-with-other-storages
    from django.contrib.staticfiles.storage import CachedFilesMixin
    from pipeline.storage import PipelineMixin
    from storages.backends.s3boto import S3BotoStorage

    class S3PipelineCachedStorage(PipelineMixin, CachedFilesMixin, S3BotoStorage):
        pass

    StaticRootS3BotoStorage = lambda: S3PipelineCachedStorage(bucket=AWS_STATIC_STORAGE_BUCKET_NAME)
    STATICFILES_STORAGE = 'config.settings.prod.StaticRootS3BotoStorage'
    STATIC_URL = S3_STATIC_URL

    MediaRootS3BotoStorage = lambda: S3BotoStorage(bucket=AWS_MEDIA_STORAGE_BUCKET_NAME)
    DEFAULT_FILE_STORAGE = 'config.settings.prod.MediaRootS3BotoStorage'
    MEDIA_URL = S3_MEDIA_URL
########## END AMAZON S3 CONFIGURATION
