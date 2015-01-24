from django.apps import AppConfig


class ExtRQSchedulerConfig(AppConfig):
    name = 'extensions.rq_scheduler'
    label = 'RQ Scheduler Extensions'

default_app_config = 'extensions.rq_scheduler.ExtRQSchedulerConfig'
