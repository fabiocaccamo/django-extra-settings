[![](https://img.shields.io/pypi/pyversions/django-extra-settings.svg?color=3776AB&logo=python&logoColor=white)](https://www.python.org/)
[![](https://img.shields.io/pypi/djversions/django-extra-settings?color=0C4B33&logo=django&logoColor=white&label=django)](https://www.djangoproject.com/)

[![](https://img.shields.io/pypi/v/django-extra-settings.svg?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/django-extra-settings/)
[![](https://pepy.tech/badge/django-extra-settings)](https://pepy.tech/project/django-extra-settings)
[![](https://img.shields.io/github/stars/fabiocaccamo/django-extra-settings?logo=github)](https://github.com/fabiocaccamo/django-extra-settings/)
[![](https://badges.pufler.dev/visits/fabiocaccamo/django-extra-settings?label=visitors&color=blue)](https://badges.pufler.dev)
[![](https://img.shields.io/pypi/l/django-extra-settings.svg?color=blue)](https://github.com/fabiocaccamo/django-extra-settings/blob/master/LICENSE.txt)

[![](https://img.shields.io/travis/fabiocaccamo/django-extra-settings?logo=travis&label=build)](https://travis-ci.org/fabiocaccamo/django-extra-settings)
[![](https://img.shields.io/codecov/c/gh/fabiocaccamo/django-extra-settings?logo=codecov)](https://codecov.io/gh/fabiocaccamo/django-extra-settings)
[![](https://img.shields.io/codacy/grade/554c0505ed9844f3865bee975d1b894c?logo=codacy)](https://www.codacy.com/app/fabiocaccamo/django-extra-settings)
[![](https://img.shields.io/codeclimate/maintainability/fabiocaccamo/django-extra-settings?logo=code-climate)](https://codeclimate.com/github/fabiocaccamo/django-extra-settings/)
[![](https://requires.io/github/fabiocaccamo/django-extra-settings/requirements.svg?branch=master)](https://requires.io/github/fabiocaccamo/django-extra-settings/requirements/?branch=master)

# django-extra-settings
config and manage extra settings using just the django admin.

![](https://user-images.githubusercontent.com/1035294/74425761-81325400-4e54-11ea-9095-3d64e1420bfe.gif)

## Installation
-   Run `pip install django-extra-settings`
-   Add `extra_settings` to `settings.INSTALLED_APPS`
-   Run ``python manage.py migrate``
-   Run ``python manage.py collectstatic``
-   Restart your application server

## Usage

### Settings
All these settings are optional, if not defined in ``settings.py`` the default values (listed below) will be used.

```python
# if True the template tag will fallback to django.conf.settings,
# very useful to retrieve conf settings such as DEBUG.
EXTRA_SETTINGS_FALLBACK_TO_CONF_SETTINGS = True
```

```python
# the upload_to path value of settings of type 'file'
EXTRA_SETTINGS_FILE_UPLOAD_TO = 'files'
```

```python
# the upload_to path value of settings of type 'image'
EXTRA_SETTINGS_IMAGE_UPLOAD_TO = 'images'
```

### Admin
Just go to the admin where you can:
-   Create a new setting
-   Update an existing setting
-   Delete an existing setting

### Python
You can retrieve settings programmatically:
```python
from extra_settings.models import Setting

value = Setting.get('SETTING_NAME', default='django-extra-settings')
```

### Templates
You can retrieve settings in templates:
```html
{% load extra_settings %}

{% get_setting 'SETTING_NAME' default='django-extra-settings' %}
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

# run tests
tox
# or
python setup.py test
# or
python -m django test --settings "tests.settings"
```

---

## License
Released under [MIT License](LICENSE.txt).
