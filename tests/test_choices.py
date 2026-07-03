import os
import subprocess
import sys
from pathlib import Path

from django.test import TestCase

from extra_settings.choices import SettingType
from extra_settings.models import Setting

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
        # Importing the choices module must not require django.setup(); this is
        # the AppRegistryNotReady scenario from issue #201. Run in a fresh
        # subprocess with no DJANGO_SETTINGS_MODULE so this test run's already
        # initialized app registry can't mask a regression.
        repo_root = Path(__file__).resolve().parent.parent
        env = {k: v for k, v in os.environ.items() if k != "DJANGO_SETTINGS_MODULE"}
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "from extra_settings.choices import SettingType; "
                "assert SettingType.STRING == 'string'",
            ],
            capture_output=True,
            text=True,
            cwd=repo_root,
            env=env,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


class SettingTypeBackwardCompatTestCase(TestCase):
    def test_model_aliases_are_enum_members(self):
        # identity, not just equality: forces the model to source TYPE_* from the
        # enum. Before wiring, Setting.TYPE_BOOL is the plain str "bool", which is
        # NOT the singleton SettingType.BOOL, so assertIs fails.
        for member_name, value in EXPECTED_TYPES.items():
            with self.subTest(type=member_name):
                alias = getattr(Setting, f"TYPE_{member_name}")
                self.assertIs(alias, getattr(SettingType, member_name))
                self.assertEqual(alias, value)

    def test_type_choices_alias_matches_enum(self):
        self.assertEqual(list(Setting.TYPE_CHOICES), list(SettingType.choices))

    def test_set_defaults_accepts_settingtype_member(self):
        Setting.set_defaults(
            [
                {
                    "name": "TEST_DEFAULTS_SETTINGTYPE",
                    "type": SettingType.STRING,
                    "value": "hello",
                }
            ]
        )
        setting_obj = Setting.objects.get(name="TEST_DEFAULTS_SETTINGTYPE")
        self.assertEqual(setting_obj.value_type, SettingType.STRING)
        self.assertEqual(setting_obj.value_type, "string")
        self.assertEqual(setting_obj.value, "hello")
