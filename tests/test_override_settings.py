from django.test import TestCase

from extra_settings.models import Setting
from extra_settings.test import override_settings


class ExtraSettingsOverrideSettingTestCase(TestCase):
    def setUp(self):
        Setting.objects.bulk_create(
            [
                Setting(
                    name="TEST_OVERRIDE_SETTING_BOOL",
                    value_type=Setting.TYPE_BOOL,
                    value=True,
                ),
                Setting(
                    name="TEST_OVERRIDE_SETTING_STRING",
                    value_type=Setting.TYPE_STRING,
                    value="not overridden...",
                ),
            ]
        )

    def tearDown(self):
        pass

    def test_without_override_settings(self):
        value = Setting.get("TEST_OVERRIDE_SETTING_BOOL")
        self.assertEqual(value, True)
        value = Setting.get("TEST_OVERRIDE_SETTING_STRING")
        self.assertEqual(value, "not overridden...")

    @override_settings(
        TEST_OVERRIDE_SETTING_BOOL=False,
        TEST_OVERRIDE_SETTING_STRING="overridden!",
    )
    def test_with_override_settings_decorator(self):
        value = Setting.get("TEST_OVERRIDE_SETTING_BOOL")
        self.assertEqual(value, False)
        value = Setting.get("TEST_OVERRIDE_SETTING_STRING")
        self.assertEqual(value, "overridden!")

    def test_with_override_settings_context_manager(self):
        with override_settings(
            TEST_OVERRIDE_SETTING_BOOL=False,
            TEST_OVERRIDE_SETTING_STRING="overridden!",
        ):
            value = Setting.get("TEST_OVERRIDE_SETTING_BOOL")
            self.assertEqual(value, False)
            value = Setting.get("TEST_OVERRIDE_SETTING_STRING")
            self.assertEqual(value, "overridden!")
