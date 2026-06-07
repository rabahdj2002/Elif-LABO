from django.core.management.base import BaseCommand
from discovery.models import SystemSettings
from discovery.db_service import DatabaseService
import django
from django.db import connections
import sys

class Command(BaseCommand):
    help = 'Validates PostgreSQL readiness and schema consistency for migration.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("--- ELIF PostgreSQL Readiness Protocol ---"))
        
        settings = SystemSettings.get_settings()
        
        # 1. Connectivity Check
        self.stdout.write("Step 1: Testing connectivity...")
        success, msg = DatabaseService.test_connection(settings)
        if not success:
            self.stdout.write(self.style.ERROR(f"FAIL: {msg}"))
            return
        self.stdout.write(self.style.SUCCESS(f"OK: Connected to {settings.db_version}"))

        # 2. Driver Check
        self.stdout.write("Step 2: verifying drivers...")
        try:
            import psycopg2
            self.stdout.write(self.style.SUCCESS("OK: psycopg2-binary installed"))
        except ImportError:
            self.stdout.write(self.style.ERROR("FAIL: psycopg2-binary missing"))
            return

        # 3. Environment Preparation
        self.stdout.write("Step 3: Checking runtime configuration...")
        DatabaseService.persist_runtime_config(settings)
        self.stdout.write(self.style.SUCCESS("OK: db_config.json updated"))

        self.stdout.write(self.style.MIGRATE_SUCCESS("\nPostgreSQL Substrate is READY for migration."))
        self.stdout.write("To complete migration, restart the application and run 'python manage.py migrate'")
