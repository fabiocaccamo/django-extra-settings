# -*- coding: utf-8 -*-

import django
from django.test import TestCase
from django.template import Context, Template

from extra_settings.models import Setting


class ExtraSettingsTemplateTagsTestCase(TestCase):

    def setUp(self):
        setting_obj, setting_created = Setting.objects.get_or_create(
            name='PACKAGE_NAME',
            defaults={
                'value_type':Setting.TYPE_STRING,
                'value_string':'django-extra-settings',
            })

    def tearDown(self):
        pass

    def _render_template(self, string, context=None):
        return Template(string).render(Context(context or {}))

    def test_get_setting(self):
        rendered = self._render_template(
            '{% load extra_settings %}'\
            '{% get_setting "PACKAGE_NAME" %}')
        self.assertEqual(rendered, 'django-extra-settings')

    def test_get_setting_assignment(self):
        if django.VERSION >= (1, 9):
            rendered = self._render_template(
                '{% load extra_settings %}'\
                '{% get_setting "PACKAGE_NAME" as package_name %}'\
                '{{ package_name }}')
            self.assertEqual(rendered, 'django-extra-settings')

    def test_get_setting_default(self):
        rendered = self._render_template(
            '{% load extra_settings %}'\
            '{% get_setting "INVALID_SETTING_NAME" default="ok" %}')
        self.assertEqual(rendered, 'ok')

    def test_get_setting_with_fallback_auto(self):
        rendered = self._render_template(
            '{% load extra_settings %}'\
            '{% get_setting "EXTRA_SETTINGS_TEST_FALLBACK_VALUE" %}')
        self.assertEqual(rendered, 'fallback-value')

    def test_get_setting_with_fallback(self):
        with self.settings(EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS=True):
            rendered = self._render_template(
                '{% load extra_settings %}'\
                '{% get_setting "EXTRA_SETTINGS_TEST_FALLBACK_VALUE" %}')
            self.assertEqual(rendered, 'fallback-value')

    def test_get_setting_without_fallback(self):
        with self.settings(EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS=False):
            rendered = self._render_template(
                '{% load extra_settings %}'\
                '{% get_setting "EXTRA_SETTINGS_TEST_FALLBACK_VALUE" %}')
            self.assertEqual(rendered, '')

    def test_get_setting_without_fallback_default(self):
        with self.settings(EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS=False):
            rendered = self._render_template(
                '{% load extra_settings %}'\
                '{% get_setting "EXTRA_SETTINGS_TEST_FALLBACK_VALUE" default="fallback-default" %}')
            self.assertEqual(rendered, 'fallback-default')
