from django.conf import settings
import psycopg2
from django.utils import timezone
import os
import json
from pathlib import Path
from django.core.management import call_command
import io

class DatabaseService:
    @staticmethod
    def dump_database_json():
        """Returns a JSON string of the current database (default)."""
        output = io.StringIO()
        # Exclude internal Django tables that might cause conflicts on restore
        call_command('dumpdata', exclude=['contenttypes', 'auth.permission'], indent=2, stdout=output)
        return output.getvalue()

    @staticmethod
    def load_database_json(json_content):
        """Loads data from a JSON string into the current database."""
        temp_file = Path(settings.BASE_DIR) / "temp_restore.json"
        try:
            with open(temp_file, "w", encoding='utf-8') as f:
                f.write(json_content)
            
            # Use --format=json explicitly
            call_command('loaddata', str(temp_file))
            return True, "Data restored successfully."
        except Exception as e:
            return False, str(e)
        finally:
            if temp_file.exists():
                os.remove(temp_file)

    @staticmethod
    def migrate_from_sqlite():
        """Dumps data from the 'sqlite_source' DB and loads it into 'default'."""
        temp_file = Path(settings.BASE_DIR) / "sqlite_dump.json"
        try:
            # Exclude contenttypes and auth.permission to avoid integrity errors
            with open(temp_file, "w", encoding='utf-8') as f:
                call_command('dumpdata', '--database=sqlite_source', exclude=['contenttypes', 'auth.permission'], indent=2, stdout=f)
            
            # Load into default
            call_command('loaddata', str(temp_file))
            return True, "Successfully migrated progress from SQLite."
        except Exception as e:
            return False, str(e)
        finally:
            if temp_file.exists():
                os.remove(temp_file)

    @staticmethod
    def get_pg_config():
        """Returns the internal PostgreSQL configuration from settings.py."""
        cfg = getattr(settings, 'POSTGRES_CONFIG', {})
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': cfg.get('NAME'),
            'USER': cfg.get('USER'),
            'PASSWORD': cfg.get('PASSWORD'),
            'HOST': cfg.get('HOST'),
            'PORT': cfg.get('PORT'),
            'OPTIONS': {
                'sslmode': cfg.get('SSL_MODE', 'prefer'),
                'connect_timeout': 5,
            }
        }

    @staticmethod
    def test_connection(settings_obj):
        """Tests connectivity using credentials from the SystemSettings model."""
        # Use model fields instead of settings.py for dynamic testing
        db_host = settings_obj.db_pg_host
        db_port = settings_obj.db_pg_port
        db_name = settings_obj.db_pg_name
        db_user = settings_obj.db_pg_user
        db_pass = settings_obj.db_pg_password
        db_ssl = settings_obj.db_pg_ssl_mode or 'prefer'
        
        print(f"Substrate Connection Test: Attempting connection to {db_host}:{db_port} (DB: {db_name})")
        
        try:
            if not db_host:
                raise ValueError("Database Host is not defined in the UI settings.")

            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_pass,
                host=db_host,
                port=db_port,
                sslmode=db_ssl,
                connect_timeout=5
            )
            
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                
                cursor.execute("SELECT pg_database_size(current_database());")
                size_bytes = cursor.fetchone()[0]
                size_mb = round(size_bytes / (1024 * 1024), 2)

            conn.close()
            
            settings_obj.db_last_status = "Connected"
            settings_obj.db_last_check = timezone.now()
            settings_obj.db_version = version
            settings_obj.db_error_log = f"Internal Connection Verified. DB Size: {size_mb} MB"
            settings_obj.save()
            
            return True, f"Success: {version}"
            
        except Exception as e:
            error_msg = str(e)
            settings_obj.db_last_status = "Failed"
            settings_obj.db_last_check = timezone.now()
            settings_obj.db_error_log = error_msg
            settings_obj.save()
            return False, error_msg

    @staticmethod
    def _get_config_path():
        """Returns the absolute path to db_config.json in the BASE_DIR."""
        # This matches BASE_DIR = Path(__file__).resolve().parent.parent in settings.py
        # because this file is in project/discovery/db_service.py
        current_dir = Path(__file__).resolve().parent
        return current_dir.parent / 'db_config.json'

    @staticmethod
    def persist_runtime_config(settings_obj):
        """
        Writes core integration configuration and DB path to a local JSON file.
        This allows settings.py to bootstrap even if the database is reset.
        """
        config_path = DatabaseService._get_config_path()
        
        data = {
            'use_postgres': settings_obj.use_postgres,
            # DB Credentials (exposed for manual modification in UI)
            'db_pg_host': settings_obj.db_pg_host,
            'db_pg_port': settings_obj.db_pg_port,
            'db_pg_name': settings_obj.db_pg_name,
            'db_pg_user': settings_obj.db_pg_user,
            'db_pg_password': settings_obj.db_pg_password,
            'db_pg_ssl_mode': settings_obj.db_pg_ssl_mode,
            
            # Core keys to prevent loss during DB switch
            'active_model': settings_obj.active_model,
            'anthropic_api_key': settings_obj.anthropic_api_key,
            'deepseek_api_key': settings_obj.deepseek_api_key,
            'stripe_public_key': settings_obj.stripe_public_key,
            'stripe_secret_key': settings_obj.stripe_secret_key,
            'stripe_webhook_secret': settings_obj.stripe_webhook_secret,
            'updated_at': str(timezone.now() if hasattr(timezone, 'now') else '')
        }
        
        try:
            with open(config_path, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error persisting runtime config: {e}")

    @staticmethod
    def load_runtime_config():
        """Reads the local JSON config for settings.py."""
        config_path = DatabaseService._get_config_path()
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return None
        return None
