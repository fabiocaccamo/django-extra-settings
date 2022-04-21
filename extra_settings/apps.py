# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.conf import settings


class ExtraSettingsConfig(AppConfig):

    name = "extra_settings"
    verbose_name = settings.EXTRA_SETTINGS_VERBOSE_NAME

    def ready(self):
        from extra_settings import signals
