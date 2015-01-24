from django.apps import AppConfig


class ExtAuthtoolsConfig(AppConfig):
    name = 'extensions.authtools'
    label = 'Authtools Extensions'

default_app_config = 'extensions.authtools.ExtAuthtoolsConfig'
