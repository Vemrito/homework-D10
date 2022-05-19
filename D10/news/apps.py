from django.apps import AppConfig


class AppointmentConfig(AppConfig):
    name = 'news'

    def ready(self):
        import news.signals