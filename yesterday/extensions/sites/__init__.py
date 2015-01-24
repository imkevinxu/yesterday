from django.apps import AppConfig


class ExtSitesConfig(AppConfig):
    name = 'extensions.sites'
    label = 'Sites Extensions'

default_app_config = 'extensions.sites.ExtSitesConfig'
