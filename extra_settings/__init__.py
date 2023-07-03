from django.core.exceptions import ImproperlyConfigured

from extra_settings.metadata import (
    __author__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __version__,
)

try:
    from extra_settings import settings  # noqa: F401
except ImproperlyConfigured:
    pass

default_app_config = "extra_settings.apps.ExtraSettingsConfig"

__all__ = [
    "__author__",
    "__copyright__",
    "__description__",
    "__license__",
    "__title__",
    "__version__",
]
