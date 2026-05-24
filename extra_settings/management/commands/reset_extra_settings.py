"""
Command to reset extra settings.
"""

import logging

from django.core.management import BaseCommand
from extra_settings.models import Setting

log = logging.getLogger(__name__)


class Command(BaseCommand):
    """Django-command for refreshing extra settings to default values"""

    help = """
    This command will remove all extra settings and recreate only those
    that described in `settings.EXTRA_SETTINGS_DEFAULTS`.
    """

    def handle(self, *_, **__) -> None:
        """
        Handle command.
        """
        log.info("Start refreshing extra settings...")
        Setting.reset_to_default()
        log.info("Refreshing of extra settings is done.")
