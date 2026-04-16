import json

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

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
    def setUp(self):
        self._setting_obj, setting_created = Setting.objects.get_or_create(
            name="PACKAGE_NAME",
            defaults={
                "value_type": Setting.TYPE_STRING,
                "value_string": "django-extra-settings",
            },
        )
        self._site = AdminSite()

    def tearDown(self):
        pass

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

    def test_construct_change_message_add(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        form = SettingForm(
            data={
                "name": "NEW_SETTING",
                "value_type": Setting.TYPE_STRING,
            }
        )
        form.is_valid()
        result = ma.construct_change_message(request, form, formsets=None, add=True)
        # For add, should delegate to parent – result is the standard added message
        self.assertNotEqual(result, "[]")

    def test_construct_change_message_change(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        form = SettingForm(instance=self._setting_obj)
        # Simulate a changed field
        form.initial = {"value_string": "old-value"}
        form.changed_data = ["value_string"]
        form.cleaned_data = {"value_string": "new-value"}
        result = ma.construct_change_message(request, form, formsets=None, add=False)
        message = json.loads(result)
        self.assertEqual(len(message), 1)
        self.assertIn("changed", message[0])
        fields = message[0]["changed"]["fields"]
        self.assertEqual(len(fields), 1)
        self.assertIn("old-value", fields[0])
        self.assertIn("new-value", fields[0])

    def test_construct_change_message_change_empty_initial(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        form = SettingForm(instance=self._setting_obj)
        form.initial = {}
        form.changed_data = ["value_string"]
        form.cleaned_data = {"value_string": "new-value"}
        result = ma.construct_change_message(request, form, formsets=None, add=False)
        message = json.loads(result)
        fields = message[0]["changed"]["fields"]
        self.assertIn("(empty)", fields[0])
        self.assertIn("new-value", fields[0])

    def test_construct_change_message_no_changes(self):
        ma = SettingAdmin(model=Setting, admin_site=AdminSite())
        form = SettingForm(instance=self._setting_obj)
        form.initial = {"value_string": "same-value"}
        form.changed_data = []
        form.cleaned_data = {"value_string": "same-value"}
        result = ma.construct_change_message(request, form, formsets=None, add=False)
        self.assertEqual(json.loads(result), [])
