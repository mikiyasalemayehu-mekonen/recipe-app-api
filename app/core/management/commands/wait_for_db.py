"""
Django command to wait for the database to be available.
"""
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until the database is available."""

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_up = False
        retries = 0
        max_retries = 60

        while not db_up and retries < max_retries:
            try:
                self.check(databases=["default"])
                db_up = True
            except (Psycopg2Error, OperationalError):
                retries += 1
                self.stdout.write(f"Database unavailable, waiting... ({retries}/{max_retries})")
                time.sleep(1)

        if not db_up:
            self.stdout.write(self.style.ERROR("Database not available after 30 seconds."))
            exit(1)
        else:
            self.stdout.write(self.style.SUCCESS("Database available!"))
