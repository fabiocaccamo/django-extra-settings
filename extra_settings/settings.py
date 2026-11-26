from django.conf import settings


def apply_defaults():
    defaults = {
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
    for name, value in defaults.items():
        if not hasattr(settings, name):
            setattr(settings, name, value)
