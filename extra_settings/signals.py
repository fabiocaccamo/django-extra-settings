# -*- coding: utf-8 -*-

from django.conf import settings
from django.db.models.signals import post_delete, post_migrate, post_save
from django.dispatch import receiver

from extra_settings.models import Setting
from extra_settings.cache import del_cached_setting, set_cached_setting


@receiver(post_delete, sender=Setting, dispatch_uid="post_delete_callback")
def post_delete_callback(sender, instance, **kwargs):
    del_cached_setting(instance.name)


@receiver(post_migrate, sender=Setting, dispatch_uid="post_migrate_callback")
def post_migrate_callback(sender, instance, **kwargs):
    Setting.set_defaults(settings.EXTRA_SETTINGS_DEFAULTS)


@receiver(post_save, sender=Setting, dispatch_uid="post_save_callback")
def post_save_callback(sender, instance, **kwargs):
    if instance.name != instance.name_initial:
        del_cached_setting(instance.name_initial)
    set_cached_setting(instance.name, instance.value)


# post_migrate.connect(Setting.post_migrate_handler, sender=self)
# Setting.set_defaults(settings.EXTRA_SETTINGS_DEFAULTS)
