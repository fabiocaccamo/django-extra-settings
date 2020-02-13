# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings

from extra_settings.models import Setting


class SettingForm(forms.ModelForm):

    class Meta:
        model = Setting
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        # resize text area
        if 'value_text' in self.fields:
            self.fields['value_text'].widget = forms.Textarea(
                attrs={'rows': 5, 'cols': 51})

    def clean_name(self):
        value = self.cleaned_data.get('name', '')
        if hasattr(settings, value):
            raise forms.ValidationError(
                'Invalid setting name, settings.{} already '
                'defined in django.conf.settings.'.format(value))
        return value
