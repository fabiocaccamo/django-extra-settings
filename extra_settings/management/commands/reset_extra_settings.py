"""
Command to reset extra settings.
"""
import logging

from django.core.management import BaseCommand
from django.db import connection
from extra_settings.models import Setting

log = logging.getLogger(__name__)


class Command(BaseCommand):
    """Django-command for refreshing extra settings"""

    help = """
    This command will remove all extra settings and recreate only those that exist 
    in 'settings.py'.
    """

    def handle(self, *_, **__) -> None:
        """
        Handle command.
        """
        log.info("Start refreshing extra settings...")

        Setting.objects.all().delete()
        Setting.set_defaults_from_settings()

        log.info("Refreshing of extra settings is done.")
