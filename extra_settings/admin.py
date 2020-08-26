# -*- coding: utf-8 -*-

from django.contrib import admin

from extra_settings.forms import SettingForm
from extra_settings.models import Setting


class SettingAdmin(admin.ModelAdmin):

    form = SettingForm
    value_fields_names = (
        'value_bool', 'value_date', 'value_datetime', 'value_decimal', 'value_duration',
        'value_email', 'value_file', 'value_float', 'value_image',
        'value_int', 'value_string', 'value_text', 'value_time', 'value_url',
    )
    search_fields = ('name', )
    list_display = ('name', 'value_type', ) + value_fields_names
    list_filter = ('value_type', )
    list_editable = value_fields_names
    sortable_by = ('name', )

    def get_changelist_form(self, request, **kwargs):
        return SettingForm

    def get_fieldsets(self, request, obj=None):
        fields = ('name', 'value_type', )
        if obj:
            fields += (obj.value_field_name, )
        return (
            (None, {
                'classes': ('wide', ),
                'fields': fields,
            }),
        )

    def get_readonly_fields(self, request, obj=None):
        return ('value_type', ) if obj else ()

    class Media:
        css = {'all': ('extra_settings/css/extra_settings.css',), }
        js = ['extra_settings/js/extra_settings.js']


admin.site.register(Setting, SettingAdmin)
