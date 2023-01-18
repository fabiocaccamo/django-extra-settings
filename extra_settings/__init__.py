from django.core.exceptions import ImproperlyConfigured

try:
    from extra_settings import settings
except ImproperlyConfigured:
    pass
