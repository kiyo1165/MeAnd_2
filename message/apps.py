from django.apps import AppConfig


class MessageConfig(AppConfig):
    name = 'message'

    def ready(self):
        from .signals.handlers import message
