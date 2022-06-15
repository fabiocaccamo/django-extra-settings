[![](https://img.shields.io/pypi/pyversions/django-extra-settings.svg?color=3776AB&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/djversions/django-extra-settings?color=0C4B33&logo=django&logoColor=white&label=django)](https://www.djangoproject.com/)

[![](https://img.shields.io/pypi/v/django-extra-settings.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/django-extra-settings/)
[![](https://pepy.tech/badge/django-extra-settings/month)](https://pepy.tech/project/django-extra-settings)
[![](https://img.shields.io/github/stars/fabiocaccamo/django-extra-settings?logo=github)](https://github.com/fabiocaccamo/django-extra-settings/)
[![](https://badges.pufler.dev/visits/fabiocaccamo/django-extra-settings?label=visitors&color=blue)](https://badges.pufler.dev)
[![](https://img.shields.io/pypi/l/django-extra-settings.svg?color=blue)](https://github.com/fabiocaccamo/django-extra-settings/blob/master/LICENSE.txt)

[![](https://img.shields.io/github/workflow/status/fabiocaccamo/django-extra-settings/Test%20package?label=build&logo=github)](https://github.com/fabiocaccamo/django-extra-settings)
[![](https://img.shields.io/codecov/c/gh/fabiocaccamo/django-extra-settings?logo=codecov)](https://codecov.io/gh/fabiocaccamo/django-extra-settings)
[![](https://img.shields.io/codacy/grade/554c0505ed9844f3865bee975d1b894c?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/django-extra-settings)
[![](https://img.shields.io/codeclimate/maintainability/fabiocaccamo/django-extra-settings?logo=code-climate)](https://codeclimate.com/github/fabiocaccamo/django-extra-settings/)
[![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# django-extra-settings
config and manage typed extra settings using just the django admin.

![](https://user-images.githubusercontent.com/1035294/74425761-81325400-4e54-11ea-9095-3d64e1420bfe.gif)

## Installation
-   Run `pip install django-extra-settings`
-   Add `extra_settings` to `settings.INSTALLED_APPS`
-   Run `python manage.py migrate`
-   Run `python manage.py collectstatic`
-   Restart your application server

## Usage

### Admin
Just go to the admin where you can:
-   Create a new setting
-   Update an existing setting
-   Delete an existing setting

### Settings
All these settings are optional, if not defined in `settings.py` the default values (listed below) will be used.

```python
# the name of the cache to use, if not found the "default" cache will be used.
EXTRA_SETTINGS_CACHE_NAME = "extra_settings"
```

```python
# a list of settings that will be available by default, each item must contain "name", "type" and "value".
# check the #types section to see all the supported settings types.
EXTRA_SETTINGS_DEFAULTS = [
    {
        "name": "SETTING_NAME",
        "type": "string",
        "value": "Hello World",
    },
    # ...
]
```

```python
# if True, settings names will be forced to honor the standard django settings format
EXTRA_SETTINGS_ENFORCE_UPPERCASE_SETTINGS = True
```

```python
# if True, the template tag will fallback to django.conf.settings,
# very useful to retrieve conf settings such as DEBUG.
EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS = True
```

```python
# the upload_to path value of settings of type 'file'
EXTRA_SETTINGS_FILE_UPLOAD_TO = "files"
```

```python
# the upload_to path value of settings of type 'image'
EXTRA_SETTINGS_IMAGE_UPLOAD_TO = "images"
```

```python
# if True, settings type list filter will be shown in the admin changelist
EXTRA_SETTINGS_SHOW_TYPE_LIST_FILTER = False
```

```python
# the package name displayed in the admin
EXTRA_SETTINGS_VERBOSE_NAME = "Settings"
```

### Caching
You can customise the app caching options using `settings.CACHES["extra_settings"]` setting, otherwise the `"default"` cache will be used:

```python
CACHES = {
    # ...
    "extra_settings": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 60,
    },
    # ...
}
```

By default the `"extra_settings"` cache is used, if you want to use another cache you can set it using the `EXTRA_SETTINGS_CACHE_NAME` setting.

### Python
You can **create**, **read**, **update** and **delete** settings programmatically:

#### Types
This is the list of the currently supported setting types you may need to use:

-   `Setting.TYPE_BOOL`
-   `Setting.TYPE_DATE`
-   `Setting.TYPE_DATETIME`
-   `Setting.TYPE_DECIMAL`
-   `Setting.TYPE_DURATION`
-   `Setting.TYPE_EMAIL`
-   `Setting.TYPE_FILE`
-   `Setting.TYPE_FLOAT`
-   `Setting.TYPE_IMAGE`
-   `Setting.TYPE_INT`
-   `Setting.TYPE_JSON`
-   `Setting.TYPE_STRING`
-   `Setting.TYPE_TEXT`
-   `Setting.TYPE_TIME`
-   `Setting.TYPE_URL`

#### Create
```python
from extra_settings.models import Setting

setting_obj = Setting(
    name="SETTING_NAME",
    value_type=Setting.TYPE_STRING,
    value="django-extra-settings",
)
setting_obj.save()
```

#### Read
```python
from extra_settings.models import Setting

value = Setting.get("SETTING_NAME", default="django-extra-settings")
```

#### Update
```python
from extra_settings.models import Setting

setting_obj = Setting(
    name="SETTING_NAME",
    value_type=Setting.TYPE_BOOL,
    value=True,
)
setting_obj.value = False
setting_obj.save()
```

#### Delete
```python
from extra_settings.models import Setting

Setting.objects.filter(name="SETTING_NAME").delete()
```

### Templates
You can retrieve settings in templates:
```html
{% load extra_settings %}

{% get_setting 'SETTING_NAME' default='django-extra-settings' %}
```

### Tests
You can override specific settings during tests using `extra_settings.test.override_settings`.

It can be used both as decorator and as context-manager:
```python
from extra_settings.test import override_settings

# decorator
@override_settings(SETTING_NAME_1="value for testing 1", SETTING_NAME_2="value for testing 2")
def test_with_custom_settings(self):
    pass

# context manager
def test_with_custom_settings(self):
    with override_settings(SETTING_NAME_1="value for testing 1", SETTING_NAME_2="value for testing 2"):
        pass
```

## Testing
```bash
# create python virtual environment
virtualenv testing_django_extra_settings

# activate virtualenv
cd testing_django_extra_settings && . bin/activate

# clone repo
git clone https://github.com/fabiocaccamo/django-extra-settings.git src && cd src

# install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# run tests
tox
# or
python setup.py test
# or
python -m django test --settings "tests.settings"
```

## License
Released under [MIT License](LICENSE.txt).

---

## See also

- [`django-admin-interface`](https://github.com/fabiocaccamo/django-admin-interface) - the default admin interface made customizable by the admin itself. popup windows replaced by modals. 🧙 ⚡

- [`django-colorfield`](https://github.com/fabiocaccamo/django-colorfield) - simple color field for models with a nice color-picker in the admin. 🎨

- [`django-maintenance-mode`](https://github.com/fabiocaccamo/django-maintenance-mode) - shows a 503 error page when maintenance-mode is on. 🚧 🛠️

- [`django-redirects`](https://github.com/fabiocaccamo/django-redirects) - redirects with full control. ↪️

- [`django-treenode`](https://github.com/fabiocaccamo/django-treenode) - probably the best abstract model / admin for your tree based stuff. 🌳

- [`python-benedict`](https://github.com/fabiocaccamo/python-benedict) - dict subclass with keylist/keypath support, I/O shortcuts (base64, csv, json, pickle, plist, query-string, toml, xml, yaml) and many utilities. 📘

- [`python-codicefiscale`](https://github.com/fabiocaccamo/python-codicefiscale) - encode/decode Italian fiscal codes - codifica/decodifica del Codice Fiscale. 🇮🇹 💳

- [`python-fontbro`](https://github.com/fabiocaccamo/python-fontbro) - friendly font operations. 🧢

- [`python-fsutil`](https://github.com/fabiocaccamo/python-fsutil) - file-system utilities for lazy devs. 🧟‍♂️
