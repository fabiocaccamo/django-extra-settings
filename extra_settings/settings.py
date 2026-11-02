import copy

from django.conf import settings

_CONFIG_DEFAULTS = {
    "EXTRA_SETTINGS_ADMIN_APP": "extra_settings",
    "EXTRA_SETTINGS_CACHE_NAME": "extra_settings",
    "EXTRA_SETTINGS_DEFAULTS": [],
    "EXTRA_SETTINGS_ENFORCE_UPPERCASE_SETTINGS": True,
    "EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS": True,
    "EXTRA_SETTINGS_FILE_UPLOAD_TO": "files",
    "EXTRA_SETTINGS_IMAGE_UPLOAD_TO": "images",
    "EXTRA_SETTINGS_SHOW_NAME_PREFIX_LIST_FILTER": False,
    "EXTRA_SETTINGS_SHOW_TYPE_LIST_FILTER": False,
    "EXTRA_SETTINGS_VERBOSE_NAME": "Extra Settings",
}


def configure_defaults():
    for key, value in _CONFIG_DEFAULTS.items():
        if not hasattr(settings, key):
            # deepcopy so mutable defaults (e.g. the EXTRA_SETTINGS_DEFAULTS
            # list) are never aliased to the canonical _CONFIG_DEFAULTS object.
            setattr(settings, key, copy.deepcopy(value))


def get(key):
    if hasattr(settings, key):
        return getattr(settings, key)
    return copy.deepcopy(_CONFIG_DEFAULTS[key])


configure_defaults()
