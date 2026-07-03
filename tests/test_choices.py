import os

from django.test import TestCase

from extra_settings.choices import SettingType

EXPECTED_TYPES = {
    "BOOL": "bool",
    "DATE": "date",
    "DATETIME": "datetime",
    "DECIMAL": "decimal",
    "DURATION": "duration",
    "EMAIL": "email",
    "FILE": "file",
    "FLOAT": "float",
    "IMAGE": "image",
    "INT": "int",
    "JSON": "json",
    "STRING": "string",
    "TEXT": "text",
    "TIME": "time",
    "URL": "url",
}


class SettingTypeChoicesTestCase(TestCase):
    def test_member_values_and_labels_are_lowercase(self):
        for member_name, value in EXPECTED_TYPES.items():
            with self.subTest(type=member_name):
                member = getattr(SettingType, member_name)
                self.assertEqual(member.value, value)
                self.assertEqual(member.label, value)

    def test_choices_match_expected(self):
        expected = [(value, value) for value in EXPECTED_TYPES.values()]
        self.assertEqual(list(SettingType.choices), expected)

    def test_importable_without_app_registry(self):
        # importing the module must not require django.setup(); this is the
        # AppRegistryNotReady scenario from issue #201.
        self.assertTrue(os.environ.get("DJANGO_SETTINGS_MODULE"))
        self.assertEqual(SettingType.STRING, "string")
