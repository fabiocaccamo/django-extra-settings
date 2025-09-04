from django import VERSION, forms
from django.conf import settings
from django.db import models

from extra_settings.models import Setting
from extra_settings.utils import enforce_uppercase_setting


def urlfields_assume_scheme(field, **kwargs):
    """
    ModelForm.Meta.formfield_callback function to set assume_scheme for scheme-less
    domains in URLFields. Only since Django version 5.0.
    """
    if isinstance(field, models.URLField) and VERSION >= (5, 0):
        kwargs["assume_scheme"] = "https"

    return field.formfield(**kwargs)


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = "__all__"
        formfield_callback = urlfields_assume_scheme

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # resize text area
        if "description" in self.fields:
            self.fields["description"].widget = forms.Textarea(
                attrs={"rows": 3, "cols": 51}
            )
        if "value_text" in self.fields:
            self.fields["value_text"].widget = forms.Textarea(
                attrs={"rows": 5, "cols": 51}
            )

    def clean_name(self):
        value = self.cleaned_data.get("name", "")
        if settings.EXTRA_SETTINGS_ENFORCE_UPPERCASE_SETTINGS:
            value = enforce_uppercase_setting(value)
        if hasattr(settings, value):
            raise forms.ValidationError(
                f"Invalid setting name, settings.{value} already "
                "defined in django.conf.settings."
            )
        return value
