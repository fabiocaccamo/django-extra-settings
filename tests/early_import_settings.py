# Reproduces the reported boot break: importing from the extra_settings
# package at the TOP of a settings module, i.e. while django.conf.settings
# is still being configured.
from extra_settings.choices import SettingType

SECRET_KEY = "django-extra-settings"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.messages",
    "extra_settings",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
USE_TZ = True

EXTRA_SETTINGS_DEFAULTS = [
    {"name": "FOO", "type": SettingType.STRING, "value": "bar"},
]
