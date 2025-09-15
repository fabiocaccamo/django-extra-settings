from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from django.urls import path, reverse
from django.shortcuts import redirect

from extra_settings.forms import SettingForm
from extra_settings.models import Setting


class SettingNamePrefixFilter(admin.SimpleListFilter):
    title = _("Name Prefix")
    parameter_name = "name_prefix"

    def lookups(self, request, model_admin):
        sep = "_"
        names = list(set(Setting.objects.all().values_list("name", flat=True)))
        names_count = len(names)
        names_parts = [name.split(sep) for name in names]
        # generate all prefixes
        prefixes = {}
        for name_parts in names_parts:
            name_parts_steps = []
            for name_part in name_parts:
                name_parts_steps.append(name_part)
                prefix = sep.join(name_parts_steps)
                prefixes.setdefault(prefix, 0)
                prefixes[prefix] += 1
        # keep only prefixes that match more than one entry and less than all entries
        prefixes = {
            key: value
            for key, value in prefixes.items()
            if value > 1 and value < names_count
        }
        # remove parent names with the same number of children of a child
        names = set(prefixes.keys())
        for name in names:
            for other_name in names:
                if (
                    name != other_name
                    and name.startswith(other_name)
                    and prefixes.get(name) == prefixes.get(other_name)
                ):
                    prefixes.pop(other_name, None)
        # sort prefixes alphabetically
        names = sorted(prefixes.keys())
        return [(name, f"{name} ({prefixes[name]})") for name in names]

    def queryset(self, request, queryset):
        prefix = self.value()
        if prefix:
            return queryset.filter(name__istartswith=prefix)
        return queryset


class SettingAdmin(admin.ModelAdmin):
    form = SettingForm
    change_list_template = "extra_settings/changelist.html"
    value_fields_names = (
        "value_bool",
        "value_date",
        "value_datetime",
        "value_decimal",
        "value_duration",
        "value_email",
        "value_file",
        "value_float",
        "value_image",
        "value_int",
        "value_json",
        "value_string",
        "value_text",
        "value_time",
        "value_url",
    )
    search_fields = ("name",)
    list_display = ("name", "value_type") + value_fields_names + ("description",)

    # begin dynamic list filters

    list_filter_items = []

    if settings.EXTRA_SETTINGS_SHOW_NAME_PREFIX_LIST_FILTER:
        list_filter_items.append(SettingNamePrefixFilter)

    if settings.EXTRA_SETTINGS_SHOW_TYPE_LIST_FILTER:
        list_filter_items.append("value_type")

    if list_filter_items:
        list_filter = tuple(list_filter_items)

    # end dynamic list filters

    list_editable = value_fields_names
    sortable_by = ("name",)

    def get_changelist_form(self, request, **kwargs):
        return SettingForm

    def get_fieldsets(self, request, obj=None):
        if obj:
            fields = (
                "name",
                "value_type",
                obj.value_field_name,
                "validator",
                "description",
            )
        else:
            fields = (
                "name",
                "value_type",
            )
        return (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": fields,
                },
            ),
        )

    def get_readonly_fields(self, request, obj=None):
        return ("value_type",) if obj else ()

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "reset/",
                self.reset_settings,
                name=f"{settings.EXTRA_SETTINGS_ADMIN_APP}_setting_reset",
            ),
        ]
        return my_urls + urls

    def reset_settings(self, request):
        """Reset existing settings to default values"""
        Setting.reset_to_default()
        return redirect(
            reverse(f"admin:{settings.EXTRA_SETTINGS_ADMIN_APP}_setting_changelist")
        )

    class Media:
        css = {
            "all": ("extra_settings/css/extra_settings.css",),
        }
        js = ("extra_settings/js/extra_settings.js",)


def register_extra_settings_admin(
    app,
    queryset_processor=None,
    unregister_default=True,
):
    """
    Based on django dynamic models general-purpose approach.
    https://code.djangoproject.com/wiki/DynamicModels#Ageneral-purposeapproach
    """
    apps = settings.INSTALLED_APPS
    if app not in apps:
        if "." in app:
            app = app.split(".")[0]
        if app not in apps:
            raise ImproperlyConfigured(
                f"{app!r} application not listed in settings.INSTALLED_APPS."
            )

    # create dynamic proxy model
    class Meta:
        proxy = True

    attrs = {
        "__module__": app,
        "Meta": Meta,
    }

    SettingProxyModel = type("Setting", (Setting,), attrs)

    # create dynamic model admin
    @admin.register(SettingProxyModel)
    class SettingProxyAdmin(SettingAdmin):
        queryset_processor = None

        def get_queryset(self, request):
            qs = super().get_queryset(request)
            if self.queryset_processor and callable(self.queryset_processor):
                qs = queryset_processor(qs)
            return qs

    SettingProxyAdmin.queryset_processor = queryset_processor

    # register dynamic model admin and unregister default model admin

    if unregister_default:
        try:
            admin.site.unregister(Setting)
        except NotRegistered:
            pass


admin.site.register(Setting, SettingAdmin)


app = settings.EXTRA_SETTINGS_ADMIN_APP
if app and app != "extra_settings":
    register_extra_settings_admin(
        app=app,
        queryset_processor=None,
        unregister_default=True,
    )
