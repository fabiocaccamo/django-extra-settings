# -*- coding: utf-8 -*-

import os

from django.conf import settings


def upload_to_files(obj, filename):
    """Provide upload path for a file."""
    return _upload_to(settings.EXTRA_SETTINGS_FILE_UPLOAD_TO, filename)


def upload_to_images(obj, filename):
    """Provide upload path for an image."""
    return _upload_to(settings.EXTRA_SETTINGS_IMAGE_UPLOAD_TO, filename)


def _upload_to(directory, filename):
    """
    Build a path from given parameters and joins them.

    :param directory: A directory for upload.
    :param filename: The filename is to be saved.
    :return: Complete upload path under the django MEDIA_ROOT.
    """
    return os.path.join(directory, filename)
