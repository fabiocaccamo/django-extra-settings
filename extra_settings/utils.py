# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.text import slugify


def enforce_uppercase_setting(name):
    return slugify(name).replace("-", "_").upper()
