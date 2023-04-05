from django.test import TestCase

from extra_settings.models import Setting


class ExtraSettingsModelsTestCase(TestCase):
    def setUp(self):
        Setting.objects.bulk_create(
            [
                Setting(
                    name="TEST_SETTING_BOOL",
                    value_type=Setting.TYPE_BOOL,
                ),
                # Setting(
                #     name="TEST_SETTING_COLOR",
                #     value_type=Setting.TYPE_COLOR,
                # ),
                Setting(
                    name="TEST_SETTING_DATE",
                    value_type=Setting.TYPE_DATE,
                ),
                Setting(
                    name="TEST_SETTING_DATETIME",
                    value_type=Setting.TYPE_DATETIME,
                ),
                Setting(
                    name="TEST_SETTING_DURATION",
                    value_type=Setting.TYPE_DURATION,
                ),
                Setting(
                    name="TEST_SETTING_DECIMAL",
                    value_type=Setting.TYPE_DECIMAL,
                ),
                Setting(
                    name="TEST_SETTING_EMAIL",
                    value_type=Setting.TYPE_EMAIL,
                ),
                Setting(
                    name="TEST_SETTING_FILE",
                    value_type=Setting.TYPE_FILE,
                ),
                Setting(
                    name="TEST_SETTING_FLOAT",
                    value_type=Setting.TYPE_FLOAT,
                ),
                # Setting(
                #     name="TEST_SETTING_HTML",
                #     value_type=Setting.TYPE_HTML,
                # ),
                Setting(
                    name="TEST_SETTING_IMAGE",
                    value_type=Setting.TYPE_IMAGE,
                ),
                Setting(
                    name="TEST_SETTING_INT",
                    value_type=Setting.TYPE_INT,
                ),
                Setting(
                    name="TEST_SETTING_JSON",
                    value_type=Setting.TYPE_JSON,
                ),
                Setting(
                    name="TEST_SETTING_STRING",
                    value_type=Setting.TYPE_STRING,
                ),
                Setting(
                    name="TEST_SETTING_TEXT",
                    value_type=Setting.TYPE_TEXT,
                ),
                Setting(
                    name="TEST_SETTING_TIME",
                    value_type=Setting.TYPE_TIME,
                ),
                # Setting(name='TEST_SETTING_UUID', value_type=Setting.TYPE_UUID),
                Setting(
                    name="TEST_SETTING_URL",
                    value_type=Setting.TYPE_URL,
                ),
            ]
        )

    def tearDown(self):
        pass

    def test_create_setting(self):
        # bool
        setting_value = True
        setting_obj = Setting(
            name="TEST_CREATE_DYNAMIC_SETTING_BOOL",
            value_type=Setting.TYPE_BOOL,
            value=setting_value,
        )
        setting_obj.save()
        self.assertEqual(setting_obj.value, setting_value)
        # url
        setting_value = "https://github.com/fabiocaccamo/django-extra-settings"
        setting_obj = Setting(
            name="TEST_CREATE_DYNAMIC_SETTING_URL",
            value_type=Setting.TYPE_URL,
            value=setting_value,
        )
        setting_obj.save()
        self.assertEqual(setting_obj.value, setting_value)

    def test_getter_setter(self):
        setting_obj, setting_created = Setting.objects.get_or_create(
            name="TEST_GETTER_SETTER", defaults={"value_type": Setting.TYPE_STRING}
        )
        self.assertEqual(setting_obj.value, "")
        setting_obj.value = "string value"
        setting_obj.save()
        setting_obj = Setting.objects.get(name="TEST_GETTER_SETTER")
        self.assertEqual(setting_obj.value, "string value")

    def test_get_with_valid_name(self):
        setting_string_value = Setting.get("TEST_SETTING_STRING")
        self.assertEqual(setting_string_value, "")

    def test_get_with_valid_name_and_default_value(self):
        setting_value = Setting.get(
            "TEST_SETTING_STRING", default="default string value"
        )
        self.assertEqual(setting_value, "")

    def test_get_with_invalid_name(self):
        setting_value = Setting.get("TEST_SETTING_STRING_INVALID")
        self.assertEqual(setting_value, None)

    def test_get_with_invalid_name_and_default_value(self):
        setting_value = Setting.get(
            "TEST_SETTING_STRING_INVALID", default="default string value"
        )
        self.assertEqual(setting_value, "default string value")

    def test_get_num_queries(self):
        with self.assertNumQueries(2):
            # first query get the setting
            # second query cache all settings
            # (executed only if the first one find a result)
            Setting.get("TEST_SETTING_STRING")
        with self.assertNumQueries(0):
            Setting.get("TEST_SETTING_STRING")
        with self.assertNumQueries(0):
            Setting.get("TEST_SETTING_STRING")

    def test_cache_updated_on_model_delete(self):
        setting_obj, setting_created = Setting.objects.get_or_create(
            name="TEST_GETTER_SETTER", defaults={"value_type": Setting.TYPE_STRING}
        )
        setting_obj.value = "string value"
        setting_obj.save()
        self.assertEqual(Setting.get("TEST_GETTER_SETTER"), "string value")
        Setting.objects.filter(pk=setting_obj.pk).delete()
        self.assertEqual(Setting.get("TEST_GETTER_SETTER"), None)

    def test_cache_updated_on_model_name_changed(self):
        setting_obj, setting_created = Setting.objects.get_or_create(
            name="TEST_GETTER_SETTER", defaults={"value_type": Setting.TYPE_STRING}
        )
        setting_obj.value = "string value"
        setting_obj.save()
        self.assertEqual(Setting.get("TEST_GETTER_SETTER"), "string value")
        setting_obj.name = "TEST_GETTER_SETTER_RENAMED"
        setting_obj.save()
        self.assertEqual(Setting.get("TEST_GETTER_SETTER"), None)
        self.assertEqual(Setting.get("TEST_GETTER_SETTER_RENAMED"), "string value")

    def test_repr(self):
        setting_obj, setting_created = Setting.objects.get_or_create(
            name="PACKAGE_NAME",
            defaults={
                "value_type": Setting.TYPE_STRING,
                "value_string": "django-extra-settings",
            },
        )
        setting_repr = f"{setting_obj.name} [{setting_obj.value_type}]"
        self.assertEqual(f"{setting_obj}", setting_repr)

    def test_set_defaults_from_settings(self):
        self.assertEqual(
            Setting.get("TEST_DEFAULT_URL"),
            "https://github.com/fabiocaccamo/django-extra-settings",
        )

    def test_set_defaults(self):
        Setting.set_defaults([])
        defaults = [
            {
                "name": "TEST_DEFAULT_STRING",
                "type": "string",
                "value": "ok",
            },
            {
                "name": "TEST_DEFAULT_INT",
                "type": "int",
                "value": 2,
            },
        ]
        Setting.set_defaults(defaults)
        self.assertEqual(Setting.get("TEST_DEFAULT_STRING"), "ok")
        self.assertEqual(Setting.get("TEST_DEFAULT_INT"), 2)

    def test_set_defaults_with_invalid_setting(self):
        defaults = {
            "TEST_DEFAULT_STRING": {
                "name": "TEST_DEFAULT_STRING",
                "type": "string",
                "value": "ok",
            },
            "TEST_DEFAULT_INT": {
                "name": "TEST_DEFAULT_INT",
                "type": "int",
                "value": 2,
            },
        }
        with self.assertRaises(ValueError):
            Setting.set_defaults(defaults)
        defaults = [
            {
                "name": "TEST_DEFAULT_STRING",
                "value": "ok",
            },
            {
                "name": "TEST_DEFAULT_INT",
                "value": 2,
            },
        ]
        with self.assertRaises(ValueError):
            Setting.set_defaults(defaults)

    def test_setting_type_json(self):
        # getter & setter
        setting_obj, setting_created = Setting.objects.get_or_create(
            name="TEST_SETTING_JSON", defaults={"value_type": Setting.TYPE_JSON}
        )
        self.assertEqual(setting_obj.value, {})
        setting_obj.value = {"level": "L2", "role": "Admin"}
        setting_obj.save()
        setting_obj = Setting.objects.get(name="TEST_SETTING_JSON")
        self.assertEqual(setting_obj.value, {"level": "L2", "role": "Admin"})
