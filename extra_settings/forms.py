from django import VERSION, forms
from django.conf import settings

from extra_settings.models import Setting
from extra_settings.utils import enforce_uppercase_setting


class _AssumeHTTPSURLField(forms.URLField):
    """
    URLField subclass that assumes HTTPS scheme for scheme-less URLs.
    Only since Django version 5.0.
    """

    def __init__(self, *args, **kwargs):
        if VERSION >= (5, 0):
            kwargs.setdefault("assume_scheme", "https")
        super().__init__(*args, **kwargs)


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = "__all__"
        field_classes = {"value_url": _AssumeHTTPSURLField}

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
