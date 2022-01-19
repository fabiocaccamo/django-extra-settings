# -*- coding: utf-8 -*-
import sys
from unittest import mock

from django.test import TestCase, override_settings

from extra_settings.models import Setting

# New in Python 3.0
# Renamed module __builtin__ to builtins (removing the underscores, adding an ‘s’)
import_path = '__builtin__.__import__' if sys.version[0] == '2' else 'builtins.__import__'

orig_import = __import__


def import_markdown_mock(name, *args):
    if name == 'markdown':
        raise ModuleNotFoundError
    return orig_import(name, *args)


class ExtraSettingsModelsTestCase(TestCase):

    def setUp(self):
        Setting.objects.bulk_create([
            Setting(name='TEST_SETTING_BOOL', value_type=Setting.TYPE_BOOL),
            # Setting(name='TEST_SETTING_COLOR', value_type=Setting.TYPE_COLOR='color'),
            Setting(name='TEST_SETTING_DATE', value_type=Setting.TYPE_DATE),
            Setting(name='TEST_SETTING_DATETIME', value_type=Setting.TYPE_DATETIME),
            Setting(name='TEST_SETTING_DURATION', value_type=Setting.TYPE_DURATION),
            Setting(name='TEST_SETTING_DECIMAL', value_type=Setting.TYPE_DECIMAL),
            Setting(name='TEST_SETTING_EMAIL', value_type=Setting.TYPE_EMAIL),
            Setting(name='TEST_SETTING_FILE', value_type=Setting.TYPE_FILE),
            Setting(name='TEST_SETTING_FLOAT', value_type=Setting.TYPE_FLOAT),
            # Setting(name='TEST_SETTING_HTML', value_type=Setting.TYPE_HTML),
            Setting(name='TEST_SETTING_IMAGE', value_type=Setting.TYPE_IMAGE),
            Setting(name='TEST_SETTING_INT', value_type=Setting.TYPE_INT),
            # Setting(name='TEST_SETTING_JSON', value_type=Setting.TYPE_JSON),
            Setting(name='TEST_SETTING_STRING', value_type=Setting.TYPE_STRING),
            Setting(name='TEST_SETTING_TEXT', value_type=Setting.TYPE_TEXT),
            Setting(name='TEST_SETTING_TIME', value_type=Setting.TYPE_TIME),
            # Setting(name='TEST_SETTING_UUID', value_type=Setting.TYPE_UUID),
            Setting(name='TEST_SETTING_URL', value_type=Setting.TYPE_URL),
        ])

    def tearDown(self):
        pass

    def test_create_setting(self):
        # bool
        setting_value = True
        setting_obj = Setting(
            name='TEST_CREATE_DYNAMIC_SETTING_BOOL',
            value_type=Setting.TYPE_BOOL,
            value=setting_value,
        )
        setting_obj.save()
        self.assertEqual(setting_obj.value, setting_value)
        # url
        setting_value = 'https://github.com/fabiocaccamo/django-extra-settings'
        setting_obj = Setting(
            name='TEST_CREATE_DYNAMIC_SETTING_URL',
            value_type=Setting.TYPE_URL,
            value=setting_value,
        )
        setting_obj.save()
        self.assertEqual(setting_obj.value, setting_value)

    def test_getter_setter(self):
        setting_obj, setting_created = Setting.objects.get_or_create(
            name='TEST_GETTER_SETTER', defaults={ 'value_type':Setting.TYPE_STRING })
        self.assertEqual(setting_obj.value, '')
        setting_obj.value = 'string value'
        setting_obj.save()
        setting_obj = Setting.objects.get(name='TEST_GETTER_SETTER')
        self.assertEqual(setting_obj.value, 'string value')

    def test_get_with_valid_name(self):
        setting_value = Setting.get('TEST_SETTING_STRING')
        self.assertEqual(setting_value, '')

    def test_get_with_valid_name_and_default_value(self):
        setting_value = Setting.get('TEST_SETTING_STRING', default='default string value')
        self.assertEqual(setting_value, '')

    def test_get_with_invalid_name(self):
        setting_value = Setting.get('TEST_SETTING_STRING_INVALID')
        self.assertEqual(setting_value, None)

    def test_get_with_invalid_name_and_default_value(self):
        setting_value = Setting.get('TEST_SETTING_STRING_INVALID', default='default string value')
        self.assertEqual(setting_value, 'default string value')

    def test_get_num_queries(self):
        with self.assertNumQueries(1):
            setting_value = Setting.get('TEST_SETTING_STRING')
        with self.assertNumQueries(0):
            setting_value = Setting.get('TEST_SETTING_STRING')
        with self.assertNumQueries(0):
            setting_value = Setting.get('TEST_SETTING_STRING')

    def test_cache_updated_on_model_delete(self):
        setting_obj, setting_created = Setting.objects.get_or_create(
            name='TEST_GETTER_SETTER', defaults={ 'value_type':Setting.TYPE_STRING })
        setting_obj.value = 'string value'
        setting_obj.save()
        self.assertEqual(Setting.get('TEST_GETTER_SETTER'), 'string value')
        Setting.objects.filter(pk=setting_obj.pk).delete()
        self.assertEqual(Setting.get('TEST_GETTER_SETTER'), None)

    def test_cache_updated_on_model_name_changed(self):
        setting_obj, setting_created = Setting.objects.get_or_create(
            name='TEST_GETTER_SETTER', defaults={ 'value_type':Setting.TYPE_STRING })
        setting_obj.value = 'string value'
        setting_obj.save()
        self.assertEqual(Setting.get('TEST_GETTER_SETTER'), 'string value')
        setting_obj.name = 'TEST_GETTER_SETTER_RENAMED'
        setting_obj.save()
        self.assertEqual(Setting.get('TEST_GETTER_SETTER'), None)
        self.assertEqual(Setting.get('TEST_GETTER_SETTER_RENAMED'), 'string value')

    def test_repr(self):
        setting_obj, setting_created=Setting.objects.get_or_create(
            name='PACKAGE_NAME',
            defaults={
                'value_type':Setting.TYPE_STRING,
                'value_string':'django-extra-settings',
            })
        setting_repr='{} [{}]'.format(
            setting_obj.name, setting_obj.value_type)
        self.assertEqual('{0}'.format(setting_obj), setting_repr)

    @override_settings(EXTRA_SETTINGS_DESCRIPTION_FORMAT=None)
    def test_description_formatted_plain(self):
        setting_obj = Setting(
            name='TEST_DESCRIPTION_PLAIN',
            value_type=Setting.TYPE_BOOL,
            description='Plain description'
        )
        des = str(setting_obj.description_formatted)
        self.assertEqual(setting_obj.description, des)

    @override_settings(EXTRA_SETTINGS_DESCRIPTION_FORMAT='pre')
    def test_description_formatted_pre(self):
        setting_obj = Setting(
            name='TEST_DESCRIPTION_PRE',
            value_type=Setting.TYPE_BOOL,
            description='Pre description'
        )
        des = str(setting_obj.description_formatted)
        self.assertEqual('<pre>' + setting_obj.description + '</pre>', des)

    @override_settings(EXTRA_SETTINGS_DESCRIPTION_FORMAT='markdown')
    def test_description_formatted_markdown(self):
        setting_obj = Setting(
            name='TEST_DESCRIPTION_MARKDOWN',
            value_type=Setting.TYPE_BOOL,
            description='# description with markdown'
        )
        des = str(setting_obj.description_formatted)
        self.assertEqual('<h1>description with markdown</h1>', des)

    @override_settings(EXTRA_SETTINGS_DESCRIPTION_FORMAT='markdown')
    def test_description_formatted_markdown_with_import_error(self):
        setting_obj = Setting(
            name='TEST_DESCRIPTION_MARKDOWN_MISSING',
            value_type=Setting.TYPE_BOOL,
            description='# description with missing markdown'
        )
        with mock.patch(import_path, side_effect=import_markdown_mock):
            des = str(setting_obj.description_formatted)
        self.assertEqual('<pre>' + setting_obj.description + '</pre>', des)
