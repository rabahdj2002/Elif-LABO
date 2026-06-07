import os
import django
import sys
from django.core.management import call_command
from django.db import connections

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elif_platform.settings')
django.setup()

def run_migration():
    print("Starting targeted migration of 'discovery' app data...")
    
    # Ensure connections are active
    connections['default'].ensure_connection()
    connections['sqlite_source'].ensure_connection()

    temp_file = "discovery_dump.json"
    
    try:
        print(f"Dumping 'discovery' data from SQLite to {temp_file}...")
        with open(temp_file, "w", encoding='utf-8') as f:
            call_command('dumpdata', 'discovery', '--database=sqlite_source', indent=2, stdout=f)
        
        print("Data dumped successfully. Now loading into Postgres...")
        # We use a long timeout session for the loaddata
        with connections['default'].cursor() as cursor:
            cursor.execute("SET statement_timeout = 0;")
            cursor.execute("SET idle_in_transaction_session_timeout = 0;")
        
        call_command('loaddata', temp_file)
        print("Successfully migrated 'discovery' data to Postgres!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    run_migration()
