# -*- coding: utf-8 -*-

from django.conf import settings


if not hasattr(settings, 'EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS'):
    settings.EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS = True

if not hasattr(settings, 'EXTRA_SETTINGS_FILE_UPLOAD_TO'):
    settings.EXTRA_SETTINGS_FILE_UPLOAD_TO = 'files'

if not hasattr(settings, 'EXTRA_SETTINGS_IMAGE_UPLOAD_TO'):
    settings.EXTRA_SETTINGS_IMAGE_UPLOAD_TO = 'images'
