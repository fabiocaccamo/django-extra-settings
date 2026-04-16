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


def get_file_storage():
    """Return the storage backend for file settings."""
    return _get_storage(settings.EXTRA_SETTINGS_FILE_STORAGE)


def get_image_storage():
    """Return the storage backend for image settings."""
    return _get_storage(settings.EXTRA_SETTINGS_IMAGE_STORAGE)


def _get_storage(storage_backend):
    """
    Return a storage instance for the given backend path.

    :param storage_backend: A dotted Python path to a storage class, or None.
    :return: A storage instance, or the default storage if no backend is given.
    """
    if storage_backend:
        from django.utils.module_loading import import_string

        return import_string(storage_backend)()
    from django.core.files.storage import default_storage

    return default_storage
