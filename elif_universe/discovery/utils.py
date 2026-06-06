import threading
from django.db import connection

def run_threaded_task(task_func, *args, **kwargs):
    """
    Helper to run a synchronous task function in a background thread.
    Used as an emergency fallback to prevent UI blocking when Celery is in Eager mode.
    """
    def wrapper():
        try:
            task_func(*args, **kwargs)
        except Exception as e:
            print(f"BACKGROUND THREAD ERROR: {str(e)}")
        finally:
            # Crucial for Django: connection is thread-local and needs to be closed
            # so it can be returned to the pool, preventing "Too many connections" errors.
            connection.close()

    t = threading.Thread(target=wrapper)
    t.daemon = True
    t.start()

from .models import SystemSettings

def collect_inquiry_report_data(inquiry):
    """
    Unified aggregator for Inquiry data across all layers.
    Returns a dictionary suitable for JSON, Markdown, or PDF rendering.
    """
    planets = inquiry.planets.all().order_by('order')
    room_states = inquiry.room_states.all()
    settings = SystemSettings.get_settings()
    
    report = {
        "metadata": {
            "id": str(inquiry.id),
            "case_id": inquiry.case_id,
            "topic": inquiry.topic,
            "created_at": inquiry.created_at.isoformat() if inquiry.created_at else None,
            "updated_at": inquiry.updated_at.isoformat() if inquiry.updated_at else None,
            "status": inquiry.status,
            "investigation_status": inquiry.investigation_status,
            "user": inquiry.user.username if inquiry.user else "Anonymous",
        },
        "frame": {
            "original_question": inquiry.core_question,
            "current_state": inquiry.current_question_state,
        },
        "reasoning_chain": [],
        "rooms": {},
        "artifacts": {
            "assumptions": inquiry.assumptions,
            "unresolved_zones": inquiry.unresolved_zones,
            "solution_families": inquiry.solution_families,
        },
        "system_settings": settings
    }

    # Extract Reasoning Chain (Planets)
    for planet in planets:
        report["reasoning_chain"].append({
            "step": planet.order,
            "name": planet.name,
            "status": planet.status,
            "data": planet.data or {}
        })

    # Extract Room States (Projections)
    # Ensure DISCOVERY always exists for template safety
    report["rooms"]["DISCOVERY"] = {
        "reformulation": inquiry.core_question,
        "verdict": "PENDING",
        "objects": []
    }
    for rs in room_states:
        report["rooms"][rs.room_type] = rs.room_data

    return report
