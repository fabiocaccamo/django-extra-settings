from django.conf import settings
from django.test import SimpleTestCase

from extra_settings.settings import apply_defaults


class ApplyDefaultsTestCase(SimpleTestCase):
    def test_fills_missing_and_keeps_user_values(self):
        with self.settings(EXTRA_SETTINGS_VERBOSE_NAME="Custom"):
            del settings.EXTRA_SETTINGS_CACHE_NAME
            apply_defaults()
            self.assertEqual(settings.EXTRA_SETTINGS_CACHE_NAME, "extra_settings")
            self.assertEqual(settings.EXTRA_SETTINGS_VERBOSE_NAME, "Custom")
