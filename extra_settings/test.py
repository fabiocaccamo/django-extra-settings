# -*- coding: utf-8 -*-

from extra_settings.cache import (
    del_cached_setting,
    get_cached_setting,
    set_cached_setting,
)
from extra_settings.models import Setting


class override_settings(object):
    """
    This class describes the override_settings decorator / context manager.
    """

    def __init__(self, **settings):
        self._settings = {}
        self._settings_override = settings.copy()

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            self._patch_settings()
            func(*args, **kwargs)
            self._reset_settings()

        return wrapped

    def __enter__(self):
        self._patch_settings()
        return self

    def __exit__(self, e_type, e_value, e_traceback):
        self._reset_settings()

    def _patch_settings(self):
        for key, value in self._settings_override.items():
            self._settings[key] = Setting.get(key)
            set_cached_setting(key, value)

    def _reset_settings(self):
        for key, _ in self._settings_override.items():
            del_cached_setting(key)
        for key, value in self._settings.items():
            set_cached_setting(key, value)
