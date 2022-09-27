# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.1](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.6.1) - 2022-07-05
-   Add missing migration. Fix #33 by [@domeniconappo](https://github.com/domeniconappo) in #35.

## [0.6.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.6.0) - 2022-07-05
-   Add custom validator support to settings. Fix #33 by [@domeniconappo](https://github.com/domeniconappo) in #34.

## [0.5.1](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.5.1) - 2022-07-05
-   Fixed admin static css media bug.

## [0.5.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.5.0) - 2022-07-01
-   Added `settings.EXTRA_SETTINGS_SHOW_NAME_PREFIX_LIST_FILTER` setting (default `False`). #31

## [0.4.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.4.0) - 2022-06-15
-   Added `override_settings` decorator / context-manager. #20
-   Added `settings.EXTRA_SETTINGS_DEFAULTS` support. #21
-   Fixed missing migration warning by adding explicit `default_auto_field` app setting. #23
-   Fixed possibility to pass `value` to the `Setting` model constructor.

## [0.3.2](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.3.2) - 2022-05-10
-   Added `EXTRA_SETTINGS_CACHE_NAME` setting.
-   Reduced database hits when using the template tag more than once in the same page.
-   Improved admin fieldsets.

## [0.3.1](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.3.1) - 2022-04-21
-   Added `EXTRA_SETTINGS_VERBOSE_NAME` setting.

## [0.3.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.3.0) - 2022-01-27
-   Added `Setting.TYPE_JSON` support. #15 #19 - Credits: [@aymaneMx](https://github.com/aymaneMx)

## [0.2.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.2.0) - 2022-01-18
-   Added `description` to setting model. #16 - Credits: [@obdulia-losantos](https://github.com/obdulia-losantos)
-   Added `EXTRA_SETTINGS_ENFORCE_UPPERCASE_SETTINGS` setting (default `True`).
-   Added `EXTRA_SETTINGS_SHOW_TYPE_LIST_FILTER` setting (default `False`).
-   Fixed missing comma in tests settings `MIDDLEWARE_CLASSES`. #14

## [0.1.4](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.1.4) - 2021-12-08
-   Added `python 3.10` support.
-   Added `django 4.0` support.
-   Fixed tests settings warnings.
-   Fixed setup warning.

## [0.1.3](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.1.3) - 2021-10-08
-   Changed `upload_to` to callable. #11 - thanks to @thlnndrs
-   Fixed `setup.py` unicode error.
-   Added `python 3.9` and `django 3.2` to `tox` and `travis`.

## [0.1.2](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.1.2) - 2020-09-04
-   Added `models.DurationField` support.

## [0.1.1](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.1.1) - 2020-02-13
-   Fixed `django 1.8` compatibility.
-   Improved code quality.

## [0.1.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.1.0) - 2020-02-13
-   Released package, installation `pip install django-extra-settings`.
