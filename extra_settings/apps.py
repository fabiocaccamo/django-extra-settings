from django.apps import AppConfig
from django.conf import settings


class ExtraSettingsConfig(AppConfig):
    name = "extra_settings"
    verbose_name = settings.EXTRA_SETTINGS_VERBOSE_NAME
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from extra_settings import signals  # noqa: F401
