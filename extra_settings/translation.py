# -*- coding: utf-8 -*-

import django
if django.VERSION >= (2, 0):
    from django.utils.translation import gettext_lazy
else:
    from django.utils.translation import ugettext_lazy as gettext_lazy
