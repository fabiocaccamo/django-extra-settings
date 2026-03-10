from django import VERSION, forms
from django.test import TestCase

from extra_settings.forms import SettingForm
from extra_settings.models import Setting


class ExtraSettingsFormsTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_form_with_valid_data(self):
        form_data = {"name": "PACKAGE_NAME", "value_type": Setting.TYPE_BOOL}
        form_obj = SettingForm(data=form_data)
        self.assertTrue(form_obj.is_valid())

    def test_form_with_incomplete_data(self):
        form_data = {"name": "PACKAGE_NAME"}
        form_obj = SettingForm(data=form_data)
        self.assertFalse(form_obj.is_valid())

    def test_form_with_invalid_setting_name(self):
        form_data = {"name": "INSTALLED_APPS", "value_type": Setting.TYPE_BOOL}
        form_obj = SettingForm(data=form_data)
        self.assertFalse(form_obj.is_valid())

    def test_form_with_optional_data(self):
        form_data = {
            "name": "PACKAGE_NAME",
            "value_type": Setting.TYPE_BOOL,
            "description": "Yes/No",
        }
        form_obj = SettingForm(data=form_data)
        self.assertTrue(form_obj.is_valid())

    def test_form_assume_scheme(self):
        form_data = {
            "name": "PACKAGE_NAME",
            "value_type": Setting.TYPE_URL,
            "description": "A URL field",
            "value_url": "example.com",
        }
        form_obj = SettingForm(data=form_data)
        self.assertTrue(form_obj.is_valid())

        if VERSION >= (5, 0):
            self.assertEqual(form_obj.cleaned_data["value_url"], "https://example.com")
        else:
            self.assertEqual(form_obj.cleaned_data["value_url"], "http://example.com")

    def test_form_password_field(self):
        form_data = {
            "name": "PACKAGE_NAME",
            "value_type": Setting.TYPE_PASSWORD,
            "description": "A secret key",
            "value_password": "mysecret",
        }
        form_obj = SettingForm(data=form_data)
        self.assertTrue(form_obj.is_valid())
        self.assertEqual(form_obj.cleaned_data["value_password"], "mysecret")

        password_field = form_obj.fields["value_password"]
        self.assertIsInstance(password_field.widget, forms.PasswordInput)
        self.assertFalse(password_field.widget.render_value)
