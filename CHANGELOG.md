# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.13.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.13.0) - 2025-02-11
-   Add `Python 3.13` and `Django 5.1` support.
-   Drop `Python 3.8`, `Python 3.9` and `Django 3.x` support.
-   Drop `jsonfield` dependency and use builtin `models.JSONField`. (by [@obdulia-losantos](https://github.com/obdulia-losantos) in #180).
-   Add Spanish localization. (by [@obdulia-losantos](https://github.com/obdulia-losantos) in #182)
-   Bump requirements
-   Bump `pre-commit` hooks
-   Bump GitHub actions.

## [0.12.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.12.0) - 2024-02-27
-   Avoid to execute database queries in app ready method. #121
-   Cache settings value even when they are retrieved from `django.conf.settings` to avoid database hits.
-   Replace `Black` and `isort` with `Ruff-format`.
-   Bump `pre-commit` hooks.

## [0.11.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.11.0) - 2023-12-05
-   Add `Python 3.12` support.
-   Add `Django 5.0` support.
-   Speed-up test workflow.
-   Bump requirements.
-   Bump `pre-commit` hooks.

## [0.10.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.10.0) - 2023-07-04
-   Add `Django 4.2` support.
-   Add Russian localization. By [@iredun](https://github.com/iredun) in #95.
-   Switch from `setup.cfg` to `pyproject.toml`.
-   Replace `flake8` with `Ruff`.
-   Fix tests on `Django < 3.2`.

## [0.9.1](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.9.1) - 2023-03-07
-   Fix wrong migration `help_text` causing need to make new migrations.

## [0.9.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.9.0) - 2023-03-03
-   Drop `Django 2.2` support.
-   Upgrade syntax for `Python >= 3.8`.
-   Add `metadata` module and read package attrs dynamically.
-   Add missing `validator` when calling `set_defaults`. By [@zackkh](https://github.com/zackkh) in #68.
-   Add `zh_Hans` language support. By [@twn39](https://github.com/twn39) in #70.
-   Move `flake8` config to `setup.cfg`.
-   Increase `flake8` checks.
-   Add `flake8-bugbear` to `pre-commit` hooks.
-   Run `flake8` also on tests files.
-   Code formatting.
-   Bump requirements.

## [0.8.1](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.8.1) - 2023-01-10
-   Fix signals not received when using admin dynamic model (dynamic `Setting` model  proxy subclass).

## [0.8.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.8.0) - 2023-01-10
-   Add `extra_settings.admin.register_extra_settings_admin` helper function.
-   Add `EXTRA_SETTINGS_ADMIN_APP` setting support.
-   Add `setup.cfg` (`setuptools` declarative syntax) generated using `setuptools-py2cfg`.
-   Add `pyupgrade` to `pre-commit` config.
-   Pin test requirements.
-   Bump test requirements.


## [0.7.0](https://github.com/fabiocaccamo/django-extra-settings/releases/tag/0.7.0) - 2022-12-13
-   Add `Python 3.11` and `django 4.1` support.
-   Drop `Python < 3.8` and `Django < 2.2` support. #49
-   Add `pre-commit`.
-   Replace `str.format` with `f-strings`.
-   Replace `setup.py test` in favor of `runtests.py`.
-   Increase the size of the `name` and `value_string` fields to 255. #37
-   Bump requirements and actions.

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
