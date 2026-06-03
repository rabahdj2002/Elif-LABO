import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elif_platform.settings')
django.setup()

from discovery.models import Inquiry, RoomState
from engine_bridge.services import EngineService

try:
    inquiry = Inquiry.objects.get(id='93cca52f-9cc9-444d-aed8-0789068ae879')
    print(f"Running engine for {inquiry.case_id}...")
    EngineService.run_full_procedure(inquiry)
    print("Engine finished. Syncing rooms...")
    for r in RoomState.objects.filter(inquiry=inquiry):
        r.sync_from_planets()
        r.save()
    print("Sync complete.")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
