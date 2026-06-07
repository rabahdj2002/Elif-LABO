import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elif_platform.settings')
django.setup()

with connection.cursor() as cursor:
    print("Fixing discovery_systemsettings column lengths...")
    cursor.execute("ALTER TABLE discovery_systemsettings ALTER COLUMN db_version TYPE varchar(512);")
    cursor.execute("ALTER TABLE discovery_systemsettings ALTER COLUMN anthropic_api_key TYPE varchar(512);")
    cursor.execute("ALTER TABLE discovery_systemsettings ALTER COLUMN deepseek_api_key TYPE varchar(512);")
    cursor.execute("ALTER TABLE discovery_systemsettings ALTER COLUMN stripe_public_key TYPE varchar(512);")
    cursor.execute("ALTER TABLE discovery_systemsettings ALTER COLUMN stripe_secret_key TYPE varchar(512);")
    cursor.execute("ALTER TABLE discovery_systemsettings ALTER COLUMN stripe_webhook_secret TYPE varchar(512);")
    
    print("Fixing discovery_inquiry column lengths...")
    cursor.execute("ALTER TABLE discovery_inquiry ALTER COLUMN case_id TYPE varchar(255);")
    cursor.execute("ALTER TABLE discovery_inquiry ALTER COLUMN final_verdict TYPE varchar(255);")
    cursor.execute("ALTER TABLE discovery_inquiry ALTER COLUMN specialization TYPE varchar(255);")
    
    connection.commit()
    print("Columns fixed successfully.")

    cursor.execute("""
        SELECT column_name, character_maximum_length 
        FROM information_schema.columns 
        WHERE table_name = 'discovery_systemsettings' 
          AND column_name IN ('db_version', 'anthropic_api_key')
    """)
    for row in cursor.fetchall():
        print(f"Postgres Column {row[0]} Length: {row[1]}")
