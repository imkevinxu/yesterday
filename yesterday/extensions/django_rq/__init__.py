from django.apps import AppConfig


class ExtDjangoRQConfig(AppConfig):
    name = 'extensions.django_rq'
    label = 'Django RQ Extensions'

default_app_config = 'extensions.django_rq.ExtDjangoRQConfig'
