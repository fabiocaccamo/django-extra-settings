# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

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
    list_display = ('name', 'value_type', ) + value_fields_names + ('description_formatted', )
    if settings.EXTRA_SETTINGS_SHOW_TYPE_LIST_FILTER:
        list_filter = ('value_type', )
    list_editable = value_fields_names
    sortable_by = ('name', )

    def get_changelist_form(self, request, **kwargs):
        return SettingForm

    def get_fieldsets(self, request, obj=None):
        if obj:
            fields = ('name', 'description', obj.value_field_name, )
        else:
            fields = ('value_type', 'name', 'description', )
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
