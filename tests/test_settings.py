import os
import subprocess
import sys
from pathlib import Path

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

    def test_configure_defaults_does_not_alias_canonical_mutable(self):
        # A missing mutable default (the EXTRA_SETTINGS_DEFAULTS list) must be
        # a fresh copy: mutating what got set on settings must not corrupt the
        # canonical _CONFIG_DEFAULTS object.
        key = "EXTRA_SETTINGS_DEFAULTS"
        original = getattr(settings, key)
        delattr(settings, key)
        try:
            extra_settings_conf.configure_defaults()
            settings.EXTRA_SETTINGS_DEFAULTS.append("mutated")
            self.assertEqual(extra_settings_conf._CONFIG_DEFAULTS[key], [])
        finally:
            setattr(settings, key, original)

    def test_get_returns_independent_copy_of_missing_mutable(self):
        # get() on a missing mutable default must return a fresh copy each call,
        # not the shared canonical object.
        key = "EXTRA_SETTINGS_DEFAULTS"
        original = getattr(settings, key)
        delattr(settings, key)
        try:
            first = extra_settings_conf.get(key)
            first.append("mutated")
            self.assertEqual(extra_settings_conf.get(key), [])
            self.assertEqual(extra_settings_conf._CONFIG_DEFAULTS[key], [])
        finally:
            setattr(settings, key, original)


class AppConfigDefaultsTestCase(TestCase):
    def test_verbose_name_matches_configured_value(self):
        app_config = django_apps.get_app_config("extra_settings")
        self.assertEqual(app_config.verbose_name, settings.EXTRA_SETTINGS_VERBOSE_NAME)

    def test_all_defaults_present_after_ready(self):
        # ready() has already run for this process; every default must be set.
        for key in EXPECTED_DEFAULTS:
            with self.subTest(key=key):
                self.assertTrue(hasattr(settings, key))


class EarlyImportBootTestCase(TestCase):
    def test_setup_succeeds_with_early_package_import(self):
        # Booting Django with a settings module that imports from the
        # extra_settings package at import time must not break defaults
        # loading. Run in a fresh subprocess so this run's already-populated
        # app registry can't mask a regression.
        repo_root = Path(__file__).resolve().parent.parent
        env = {k: v for k, v in os.environ.items() if k != "DJANGO_SETTINGS_MODULE"}
        env["DJANGO_SETTINGS_MODULE"] = "tests.early_import_settings"
        script = (
            "import django; django.setup();"
            "from django.contrib import admin; admin.autodiscover();"
            "from django.conf import settings;"
            "assert settings.EXTRA_SETTINGS_VERBOSE_NAME == 'Extra Settings';"
            "assert settings.EXTRA_SETTINGS_ADMIN_APP == 'extra_settings';"
            "assert settings.EXTRA_SETTINGS_ENFORCE_UPPERCASE_SETTINGS is True"
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            cwd=repo_root,
            env=env,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
