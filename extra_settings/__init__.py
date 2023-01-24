from django.core.exceptions import ImproperlyConfigured

try:
    from extra_settings import settings  # noqa: F401
except ImproperlyConfigured:
    pass
