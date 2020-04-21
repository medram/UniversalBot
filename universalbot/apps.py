from django.apps import AppConfig


class UniversalbotConfig(AppConfig):
    name = 'universalbot'
    verbose_name = 'Universal Bot'

    def ready(self):
    	from . import signals, tasks_signals
