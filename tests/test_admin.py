# -*- coding: utf-8 -*-
import sys

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from extra_settings.admin import SettingAdmin
from extra_settings.forms import SettingForm
from extra_settings.models import Setting


def markdown_fn(value):
    return '<md>' + value + '</md>'

def markdown_mocked():
    pass

setattr(markdown_mocked, 'markdown', markdown_fn)

class MockRequest(object):
    pass

class MockSuperUser(object):
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()


class ExtraSettingsAdminTestCase(TestCase):

    def setUp(self):
        self._setting_obj, setting_created = Setting.objects.get_or_create(
            name='PACKAGE_NAME',
            defaults={
                'value_type':Setting.TYPE_STRING,
                'value_string':'django-extra-settings',
                'description': 'django-extra-description',
            })
        self._site = AdminSite()

        get_user_model().objects.create_superuser(
            username='admin-test',
            email='',
            password='secretsecret',
        )
        self.assertTrue(self.client.login(username='admin-test', password='secretsecret'))

    def tearDown(self):
        sys.modules['markdown'] = None

    def test_changelist_form(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        self.assertEqual(ma.get_changelist_form(request=None), SettingForm)

    def test_fieldsets(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        self.assertEqual(ma.get_fieldsets(request),
            ((None, {'classes': ('wide',), 'fields': ('value_type', 'name', 'description')}),) )
        self.assertEqual(ma.get_fieldsets(request, self._setting_obj),
            ((None, {'classes': ('wide',), 'fields': ('name', 'description', 'value_string')}),) )

    def test_modeladmin_save(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        ma.save_model(obj=Setting(), request=None, form=None, change=None)

    def test_modeladmin_str(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        self.assertEqual(str(ma), 'extra_settings.SettingAdmin')

    def test_readonly_fields(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        self.assertEqual(ma.get_readonly_fields(request), ())
        self.assertEqual(ma.get_readonly_fields(request, self._setting_obj), ('value_type', ))

    @override_settings(EXTRA_SETTINGS_DESCRIPTION_FORMAT=None)
    def test_list_display_description_plain(self):
        response = self.client.get('/admin/extra_settings/setting/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<td class="field-description_formatted">django-extra-description</td>',
            response.content.decode()
        )

    @override_settings(EXTRA_SETTINGS_DESCRIPTION_FORMAT='pre')
    def test_list_display_description_pre(self):
        response = self.client.get('/admin/extra_settings/setting/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<td class="field-description_formatted"><pre>django-extra-description</pre></td>',
            response.content.decode()
        )

    @override_settings(EXTRA_SETTINGS_DESCRIPTION_FORMAT='markdown')
    def test_list_display_description_markdown(self):
        sys.modules['markdown'] = markdown_mocked

        response = self.client.get('/admin/extra_settings/setting/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '<td class="field-description_formatted"><md>django-extra-description</md></td>',
            response.content.decode()
        )
