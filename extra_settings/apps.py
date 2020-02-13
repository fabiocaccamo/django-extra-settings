# -*- coding: utf-8 -*-

from django.apps import AppConfig

from extra_settings.translation import gettext_lazy as _


class ExtraSettingsConfig(AppConfig):

    name = 'extra_settings'
    verbose_name = _('Extra Settings')

    def ready(self):
        from extra_settings import signals
