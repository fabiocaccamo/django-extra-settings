from django.core.exceptions import ValidationError
from django.test import TestCase

from extra_settings.models import Setting


def positive_int_validator(value):
    return value > 0


def alphanumeric_strings_validator(value):
    return value.isalnum()


class ExtraSettingsValidatorsTestCase(TestCase):
    def setUp(self):
        Setting.objects.bulk_create(
            [
                Setting(
                    name="TEST_VALIDATE_POSITIVE_INTEGER",
                    value_type=Setting.TYPE_INT,
                    value=10,
                    validator="tests.test_validators.positive_int_validator",
                ),
                Setting(
                    name="TEST_NO_VALIDATORS_INTEGER",
                    value_type=Setting.TYPE_INT,
                    value=10,
                ),
                Setting(
                    name="TEST_VALIDATE_STRINGS",
                    value_type=Setting.TYPE_STRING,
                    value="This is a correct String",
                    validator="tests.test_validators.alphanumeric_strings_validator",
                ),
            ]
        )

    def test_validators(self):
        positive_integer = Setting.objects.get(name="TEST_VALIDATE_POSITIVE_INTEGER")
        positive_integer.value = -10
        with self.assertRaises(ValidationError):
            positive_integer.full_clean()
        normal_integer = Setting.objects.get(name="TEST_NO_VALIDATORS_INTEGER")
        normal_integer.value = -10
        normal_integer.full_clean()
        alnum_string = Setting.objects.get(name="TEST_VALIDATE_STRINGS")
        alnum_string.value = "!@-10"
        with self.assertRaises(ValidationError):
            alnum_string.full_clean()
