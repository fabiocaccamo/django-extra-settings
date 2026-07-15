from django.apps import apps as django_apps
from django.conf import settings
from django.test import TestCase

from extra_settings import settings as extra_settings_conf

EXPECTED_DEFAULTS = {
    "EXTRA_SETTINGS_ADMIN_APP": "extra_settings",
    "EXTRA_SETTINGS_CACHE_NAME": "extra_settings",
    "EXTRA_SETTINGS_DEFAULTS": [],
    "EXTRA_SETTINGS_ENFORCE_UPPERCASE_SETTINGS": True,
    "EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS": True,
    "EXTRA_SETTINGS_FILE_UPLOAD_TO": "files",
    "EXTRA_SETTINGS_IMAGE_UPLOAD_TO": "images",
    "EXTRA_SETTINGS_SHOW_NAME_PREFIX_LIST_FILTER": False,
    "EXTRA_SETTINGS_SHOW_TYPE_LIST_FILTER": False,
    "EXTRA_SETTINGS_VERBOSE_NAME": "Extra Settings",
}


class ConfigDefaultsTestCase(TestCase):
    def test_config_defaults_match_expected(self):
        self.assertEqual(extra_settings_conf._CONFIG_DEFAULTS, EXPECTED_DEFAULTS)

    def test_get_returns_default_when_attribute_missing(self):
        key = "EXTRA_SETTINGS_ADMIN_APP"
        original = getattr(settings, key)
        delattr(settings, key)
        try:
            self.assertEqual(extra_settings_conf.get(key), "extra_settings")
        finally:
            setattr(settings, key, original)

    def test_get_returns_user_value_when_present(self):
        # tests/settings.py sets EXTRA_SETTINGS_DEFAULTS to a non-empty list.
        self.assertEqual(
            extra_settings_conf.get("EXTRA_SETTINGS_DEFAULTS"),
            settings.EXTRA_SETTINGS_DEFAULTS,
        )
        self.assertNotEqual(settings.EXTRA_SETTINGS_DEFAULTS, [])

    def test_configure_defaults_sets_missing_keys(self):
        key = "EXTRA_SETTINGS_VERBOSE_NAME"
        original = getattr(settings, key)
        delattr(settings, key)
        try:
            extra_settings_conf.configure_defaults()
            self.assertEqual(settings.EXTRA_SETTINGS_VERBOSE_NAME, "Extra Settings")
        finally:
            setattr(settings, key, original)

    def test_configure_defaults_does_not_overwrite_existing(self):
        key = "EXTRA_SETTINGS_VERBOSE_NAME"
        original = getattr(settings, key)
        setattr(settings, key, "Custom")
        try:
            extra_settings_conf.configure_defaults()
            self.assertEqual(settings.EXTRA_SETTINGS_VERBOSE_NAME, "Custom")
        finally:
            setattr(settings, key, original)

    def test_configure_defaults_is_idempotent(self):
        extra_settings_conf.configure_defaults()
        extra_settings_conf.configure_defaults()
        for key, _value in EXPECTED_DEFAULTS.items():
            with self.subTest(key=key):
                self.assertTrue(hasattr(settings, key))


class AppConfigDefaultsTestCase(TestCase):
    def test_verbose_name_matches_configured_value(self):
        app_config = django_apps.get_app_config("extra_settings")
        self.assertEqual(app_config.verbose_name, settings.EXTRA_SETTINGS_VERBOSE_NAME)

    def test_all_defaults_present_after_ready(self):
        # ready() has already run for this process; every default must be set.
        for key in EXPECTED_DEFAULTS:
            with self.subTest(key=key):
                self.assertTrue(hasattr(settings, key))
