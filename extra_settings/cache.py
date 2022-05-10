# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.cache import cache, caches


def _get_cache():
    cache_name = settings.EXTRA_SETTINGS_CACHE_NAME
    return caches[cache_name] if cache_name in settings.CACHES else cache


def _get_cache_key(key):
    return "extra_settings_{}".format(key)


def del_cached_setting(key):
    _get_cache().delete(_get_cache_key(key))


def get_cached_setting(key):
    return _get_cache().get(_get_cache_key(key), None)


def set_cached_setting(key, value):
    _get_cache().set(_get_cache_key(key), value)
