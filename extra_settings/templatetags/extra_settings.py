# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django import template

from extra_settings.models import Setting


register = template.Library()

try:
    assignment_tag = register.assignment_tag
except AttributeError:
    assignment_tag = register.simple_tag


@assignment_tag(takes_context=True)
def get_setting(context, name, default=''):
    return Setting.get(name, default)
