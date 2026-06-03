# ELIF Universe | Engine Bridge

This Django project serves as the interactive frontend for the ELIF Alpha Engine.

## Architecture
1. **Alpha Engine**: Located in `../src/elif_v0_1/`. It remains a pure-Python reasoning kernel.
2. **Engine Bridge**: Localized in `engine_bridge/services.py`. It imports the `ProcedureRunner` and executes it.
3. **Discovery App**: Manages the persistence of inquiries and planets using Django Models.
4. **Live Telemetry**: Uses `django-htmx` and Tailwind CSS to provide a real-time "Pulse" experience.

## Operational Commands
### 1. Launch Server
```powershell
python manage.py runserver
```

### 2. Reset Ecosystem
```powershell
rm db.sqlite3
python manage.py migrate
python seed_data.py
```

### 3. Initialize New Mission
Navigate to `/initialize/` or click "Initialize New Inquiry" on the dashboard.

## Planet States
- **NOT_STARTED**: The engine has not yet analyzed this room.
- **IN_PROGRESS**: The K-Pulse is currently active in this sector.
- **COMPLETED**: Data is saved and ready for branching or further validation.
