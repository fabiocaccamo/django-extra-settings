from django.utils.module_loading import import_string
from django.utils.text import slugify


def enforce_uppercase_setting(name):
    return slugify(name).replace("-", "_").upper()


def import_function(path):
    if not path:
        return None
    try:
        func = import_string(path)
        if callable(func):
            return func
        return None
    except ImportError:
        return None
