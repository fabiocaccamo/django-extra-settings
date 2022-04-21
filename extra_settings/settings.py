# -*- coding: utf-8 -*-

from django.conf import settings


if not hasattr(settings, "EXTRA_SETTINGS_ENFORCE_UPPERCASE_SETTINGS"):
    settings.EXTRA_SETTINGS_ENFORCE_UPPERCASE_SETTINGS = True

if not hasattr(settings, "EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS"):
    settings.EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS = True

if not hasattr(settings, "EXTRA_SETTINGS_FILE_UPLOAD_TO"):
    settings.EXTRA_SETTINGS_FILE_UPLOAD_TO = "files"

if not hasattr(settings, "EXTRA_SETTINGS_IMAGE_UPLOAD_TO"):
    settings.EXTRA_SETTINGS_IMAGE_UPLOAD_TO = "images"

if not hasattr(settings, "EXTRA_SETTINGS_SHOW_TYPE_LIST_FILTER"):
    settings.EXTRA_SETTINGS_SHOW_TYPE_LIST_FILTER = False

if not hasattr(settings, "EXTRA_SETTINGS_VERBOSE_NAME"):
    settings.EXTRA_SETTINGS_VERBOSE_NAME = "Extra Settings"
