from django.apps import AppConfig
from django.db.models.signals import post_migrate

from extra_settings import settings as extra_settings_conf


class ExtraSettingsConfig(AppConfig):
    name = "extra_settings"
    verbose_name = extra_settings_conf.get("EXTRA_SETTINGS_VERBOSE_NAME")
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        extra_settings_conf.configure_defaults()

        from extra_settings import signals  # noqa: F401
        from extra_settings.models import Setting

        post_migrate.connect(Setting.set_defaults_from_settings, sender=self)
