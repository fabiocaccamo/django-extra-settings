from inspect import isclass

from django.conf import settings
from django.db.models.signals import post_delete, post_migrate, post_save

from extra_settings.cache import del_cached_setting, set_cached_setting
from extra_settings.models import Setting


def __is_setting_signal(sender):
    return isclass(sender) and issubclass(sender, Setting)


def post_migrate_setting(sender, **kwargs):
    if not __is_setting_signal(sender):
        return
    Setting.set_defaults(settings.EXTRA_SETTINGS_DEFAULTS)


def post_save_setting(sender, instance, **kwargs):
    if not __is_setting_signal(sender):
        return
    if instance.name != instance.name_initial:
        del_cached_setting(instance.name_initial)
    set_cached_setting(instance.name, instance.value)


def post_delete_setting(sender, instance, **kwargs):
    if not __is_setting_signal(sender):
        return
    del_cached_setting(instance.name)


post_migrate.connect(
    post_migrate_setting,
    dispatch_uid="post_migrate_extra_settings_setting",
)
post_save.connect(
    post_save_setting,
    dispatch_uid="post_save_extra_settings_setting",
)
post_delete.connect(
    post_delete_setting,
    dispatch_uid="post_delete_extra_settings_setting",
)
