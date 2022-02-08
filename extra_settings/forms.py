# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings

from extra_settings.models import Setting
from extra_settings.utils import enforce_uppercase_setting


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
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
                "Invalid setting name, settings.{} already "
                "defined in django.conf.settings.".format(value)
            )
        return value
