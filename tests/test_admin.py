# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from extra_settings.admin import SettingAdmin
from extra_settings.forms import SettingForm
from extra_settings.models import Setting


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
            })
        self._site = AdminSite()

    def tearDown(self):
        pass

    def test_changelist_form(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        self.assertEqual(ma.get_changelist_form(request=None), SettingForm)

    def test_fieldsets(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        self.assertEqual(ma.get_fieldsets(request),
            ((None, {'classes': ('wide',), 'fields': ('name', 'value_type')}),) )
        self.assertEqual(ma.get_fieldsets(request, self._setting_obj),
            ((None, {'classes': ('wide',), 'fields': ('name', 'value_type', 'value_string')}),) )

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
