from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from extra_settings import fields
from extra_settings.cache import get_cached_setting, set_cached_setting
from extra_settings.utils import enforce_uppercase_setting, import_function


class Setting(models.Model):
    """
    This class describes a Setting model.
    """

    @staticmethod
    def _cache_all_settings():
        settings_qs = Setting.objects.all()
        settings_list = list(settings_qs)
        for setting_obj in settings_list:
            setting_name = setting_obj.name
            setting_value = setting_obj.value
            set_cached_setting(setting_name, setting_value)

    @staticmethod
    def _get_from_cache(name):
        return get_cached_setting(name)

    @staticmethod
    def _get_from_database(name):
        try:
            setting_obj = Setting.objects.get(name=name)
            value = setting_obj.value
            set_cached_setting(name, value)
            return value
        except Setting.DoesNotExist:
            return None

    @staticmethod
    def _get_from_settings(name):
        if settings.EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS:
            return getattr(settings, name, None)
        return None

    @classmethod
    def get(cls, name, default=None):
        val = cls._get_from_cache(name)
        if val is None:
            val = cls._get_from_database(name)
            if val is None:
                val = cls._get_from_settings(name)
                if val is None:
                    val = default
            else:
                # value found, it means that cache was not set or expired.
                # cache all other settings to avoid multiple queries
                # in pages using the template more than once.
                cls._cache_all_settings()
        if val is not None:
            set_cached_setting(name, val)
        return val

    @classmethod
    def set_defaults(cls, defaults):
        if not isinstance(defaults, list):
            raise ValueError("Setting 'defaults' must be a list of dicts items.")
        if not defaults:
            return
        for item in defaults:
            if not isinstance(item, dict):
                raise ValueError("Setting 'defaults' item must be a dict.")
            try:
                name = item["name"]
                value_type = item["type"]
                value_type = value_type.replace("Setting.TYPE_", "").lower()
                value = item["value"]
            except KeyError as error:
                raise ValueError(
                    "Setting 'defaults' item must contain "
                    "'name', 'type' and 'value' keys."
                ) from error
            validator = item.get("validator", None)
            description = item.get("description", "")
            setting_obj, setting_created = cls.objects.get_or_create(
                name=name,
                defaults={
                    "value_type": value_type,
                    "description": description,
                    "validator": validator,
                },
            )
            if setting_created:
                setting_obj.value = value
                setting_obj.save()

    @classmethod
    def set_defaults_from_settings(cls, *args, **kwargs):
        cls.set_defaults(settings.EXTRA_SETTINGS_DEFAULTS)

    TYPE_BOOL = "bool"
    # TYPE_COLOR = "color" # TODO
    TYPE_DATE = "date"
    TYPE_DATETIME = "datetime"
    TYPE_DECIMAL = "decimal"
    TYPE_DURATION = "duration"
    TYPE_EMAIL = "email"
    TYPE_FILE = "file"
    TYPE_FLOAT = "float"
    # TYPE_HTML = "html"
    TYPE_IMAGE = "image"
    TYPE_INT = "int"
    TYPE_JSON = "json"
    TYPE_STRING = "string"
    TYPE_TEXT = "text"
    TYPE_TIME = "time"
    # TYPE_UUID = "uuid" # TODO
    TYPE_URL = "url"

    TYPE_CHOICES = (
        (TYPE_BOOL, TYPE_BOOL),
        # (TYPE_COLOR, TYPE_COLOR, ),
        (TYPE_DATE, TYPE_DATE),
        (TYPE_DATETIME, TYPE_DATETIME),
        (TYPE_DECIMAL, TYPE_DECIMAL),
        (TYPE_DURATION, TYPE_DURATION),
        (TYPE_EMAIL, TYPE_EMAIL),
        (TYPE_FILE, TYPE_FILE),
        (TYPE_FLOAT, TYPE_FLOAT),
        # (TYPE_HTML, TYPE_HTML, ),
        (TYPE_IMAGE, TYPE_IMAGE),
        (TYPE_INT, TYPE_INT),
        (TYPE_JSON, TYPE_JSON),
        (TYPE_STRING, TYPE_STRING),
        (TYPE_TEXT, TYPE_TEXT),
        (TYPE_TIME, TYPE_TIME),
        # (TYPE_UUID, TYPE_UUID, ),
        (TYPE_URL, TYPE_URL),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Name"),
        help_text=_("(e.g. SETTING_NAME)"),
    )
    value_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name=_(
            "Type",
        ),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
    )

    value_bool = models.BooleanField(
        default=False,
        verbose_name=_("Value"),
    )
    value_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Value"),
    )
    value_datetime = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Value"),
    )
    value_decimal = models.DecimalField(
        blank=True,
        max_digits=19,
        decimal_places=10,
        default=Decimal("0.0"),
        verbose_name=_("Value"),
    )
    value_duration = models.DurationField(
        blank=True,
        null=True,
        verbose_name=_("Value"),
    )
    value_email = models.EmailField(
        blank=True,
        verbose_name=_("Value"),
    )
    value_file = models.FileField(
        blank=True,
        upload_to=fields.upload_to_files,
        verbose_name=_("Value"),
    )
    value_float = models.FloatField(
        blank=True,
        default=0.0,
        verbose_name=_("Value"),
    )
    value_image = models.FileField(
        blank=True,
        upload_to=fields.upload_to_images,
        verbose_name=_("Value"),
    )
    value_int = models.IntegerField(
        blank=True,
        default=0,
        verbose_name=_("Value"),
    )
    value_json = models.JSONField(
        blank=True,
        default=dict,
        verbose_name=_("Value"),
    )
    value_string = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Value"),
    )
    value_text = models.TextField(
        blank=True,
        verbose_name=_("Value"),
    )
    value_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name=_("Value"),
    )
    value_url = models.URLField(
        blank=True,
        verbose_name=_("Value"),
    )
    validator = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_("Validator"),
        help_text=_(
            "Full python path to a validator function, "
            "eg. 'myapp.mymodule.my_validator'"
        ),
    )

    @property
    def value_field_name(self):
        return f"value_{self.value_type}"

    @property
    def value(self):
        return getattr(self, self.value_field_name, None)

    @value.setter
    def value(self, new_value):
        setattr(self, self.value_field_name, new_value)

    def __init__(self, *args, **kwargs):
        value = kwargs.pop("value", None)
        super().__init__(*args, **kwargs)
        if value is not None:
            self.value = value
        self.name_initial = self.name

    def validate(self):
        if not self.validator:
            return
        validator_func = import_function(self.validator)
        if not validator_func:
            raise ValueError(f"Invalid validator function path: {self.validator!r}")
        is_valid = validator_func(self.value)
        if not is_valid:
            raise ValidationError(
                f"Invalid value for setting {self.name!r}, "
                f"{self.value!r} is not validated by {self.validator!r} validator."
            )

    def save(self, *args, **kwargs):
        if settings.EXTRA_SETTINGS_ENFORCE_UPPERCASE_SETTINGS:
            self.name = enforce_uppercase_setting(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.validate()

    class Meta:
        ordering = ["name"]
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    def __str__(self):
        return force_str(f"{self.name} [{self.value_type}]")
