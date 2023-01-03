from django.core.exceptions import ImproperlyConfigured

try:
    from extra_settings import settings
except ImproperlyConfigured:
    pass

default_app_config = "extra_settings.apps.ExtraSettingsConfig"
