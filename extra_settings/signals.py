# -*- coding: utf-8 -*-

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from extra_settings.models import Setting
from extra_settings.cache import del_cached_setting, set_cached_setting


@receiver(post_delete, sender=Setting, dispatch_uid='post_delete_callback')
def post_delete_callback(sender, instance, **kwargs):
    del_cached_setting(instance.name)


@receiver(post_save, sender=Setting, dispatch_uid='post_save_callback')
def post_save_callback(sender, instance, **kwargs):
    if instance.name != instance.name_initial:
        del_cached_setting(instance.name_initial)
    set_cached_setting(instance.name, instance.value)
