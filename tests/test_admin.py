from django.contrib.admin.sites import AdminSite
from django.test import TestCase, override_settings

from unittest.mock import patch

from extra_settings.admin import SettingAdmin
from extra_settings.forms import SettingForm
from extra_settings.models import Setting


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class ExtraSettingsAdminTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setting_obj = Setting.objects.create(
            name="PACKAGE_NAME",
            value_type=Setting.TYPE_STRING,
            value_string="django-extra-settings",
        )
        cls._site = AdminSite()

    def test_changelist_form(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        self.assertEqual(ma.get_changelist_form(request=None), SettingForm)

    def test_fieldsets(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        self.assertEqual(
            ma.get_fieldsets(request),
            (
                (
                    None,
                    {
                        "classes": ("wide",),
                        "fields": ("name", "value_type"),
                    },
                ),
            ),
        )
        self.assertEqual(
            ma.get_fieldsets(request, self._setting_obj),
            (
                (
                    None,
                    {
                        "classes": ("wide",),
                        "fields": (
                            "name",
                            "value_type",
                            "value_string",
                            "validator",
                            "description",
                        ),
                    },
                ),
            ),
        )

    def test_modeladmin_save(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        ma.save_model(obj=Setting(), request=None, form=None, change=None)

    def test_modeladmin_str(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        self.assertEqual(str(ma), "extra_settings.SettingAdmin")

    def test_readonly_fields(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        self.assertEqual(ma.get_readonly_fields(request), ())
        self.assertEqual(
            ma.get_readonly_fields(request, self._setting_obj), ("value_type",)
        )

    @override_settings(
        EXTRA_SETTINGS_DEFAULTS=[
            {
                "name": "foo",
                "type": "string",
                "value": "bar",
            },
        ]
    )
    @patch("extra_settings.admin.redirect")
    @patch("extra_settings.admin.reverse")
    def test_modeladmin_reset(self, mock_redirect, mock_reverse):
        self.assertEqual(Setting.objects.count(), 1)
        self._setting_obj.value_string = "foo"
        self._setting_obj.save()
        Setting.objects.create(
            name="bar",
            value_type=Setting.TYPE_BOOL,
            value_bool=True,
        )
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        ma.reset_settings(request)
        self.assertEqual(Setting.objects.count(), 1)
        obj = Setting.objects.get(name="FOO")
        self.assertEqual(obj.value_type, Setting.TYPE_STRING)
        self.assertEqual(obj.value, "bar")

    @override_settings(EXTRA_SETTINGS_ADMIN_APP="app")
    def test_get_urls(self) -> None:
        reset_url = "app_setting_reset"
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        urls = [url.name for url in ma.get_urls()]
        self.assertTrue(reset_url in urls)
