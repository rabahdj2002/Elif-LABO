from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.urls import reverse
from django.db.models import Sum
from .models import Inquiry, Planet, RoomState, EngineRun, SystemSettings, SpendRecord
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from engine_bridge.services import EngineService
from .tasks import run_engine_task
from celery.result import AsyncResult
import io
import json
import re
import time
import threading
from contextlib import redirect_stdout
from django.db import connection
from .utils import run_threaded_task

def _is_engine_busy(request):
    """
    Helper to check if the session lock is valid.
    Self-heals if the inquiry in the session is actually finished.
    """
    active_pk = request.session.get('active_engine_pk')
    if not active_pk:
        return False
        
    try:
        active_inq = Inquiry.objects.get(pk=active_pk)
        if active_inq.status in ['COMPLETED', 'FAILED', 'REFUSED']:
            # Stale lock - inquiry finished but session not updated
            del request.session['active_engine_pk']
            request.session.modified = True
            return False
        return True # Still busy
    except Inquiry.DoesNotExist:
        # Record gone - clear lock
        del request.session['active_engine_pk']
        request.session.modified = True
        return False

@login_required
def system_settings_view(request):
    """View to manage global engine and UI parameters."""
    settings = SystemSettings.get_settings()
    
    if request.method == "POST":
        settings.active_model = request.POST.get("active_model")
        settings.anthropic_api_key = request.POST.get("anthropic_api_key")
        settings.offline_mode = request.POST.get("offline_mode") == "on"
        settings.reasoning_depth = int(request.POST.get("reasoning_depth", 7))
        settings.auto_refresh_ms = int(request.POST.get("auto_refresh_ms", 5000))
        settings.save()
        messages.success(request, "System parameters updated successfully.")
        return redirect("discovery:settings")

    return render(request, "discovery/settings.html", {"settings": settings})

@login_required
def clear_engine_lock(request):
    """Admin-level override to clear the session lock."""
    if 'active_engine_pk' in request.session:
        del request.session['active_engine_pk']
        request.session.modified = True
        messages.success(request, "Engine lock cleared successfully.")
    else:
        messages.info(request, "No active engine lock found.")
    
    return redirect(request.META.get('HTTP_REFERER', 'discovery:system_map'))

@login_required
def documentation_view(request):
    """Protocol Documentation and Tutorials."""
    return render(request, "discovery/documentation.html")

def engine_events(request, pk):
    """
    Server-Sent Events (SSE) stream for engine progress.
    Provides real-time updates of Inquiry and Planet states.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)

    def event_stream():
        last_state = ""
        while True:
            # Re-fetch from DB to get latest state
            try:
                inquiry.refresh_from_db()
            except Exception:
                break # Model deleted or connection lost
                
            planets = inquiry.planets.all().order_by('order')
            
            # Construct a minimal representation of the whole pipeline state
            state_obj = {
                "inquiry_id": str(inquiry.id),
                "status": inquiry.status,
                "message": inquiry.current_status_msg,
                "steps": [
                    {
                        "order": p.order,
                        "name": p.name,
                        "status": p.status,
                    } for p in planets
                ]
            }
            
            current_state_json = json.dumps(state_obj)
            
            # Only send if state has changed (to save bandwidth)
            if current_state_json != last_state:
                yield f"data: {current_state_json}\n\n"
                last_state = current_state_json
            
            # Safety break if inquiry reached a terminal state
            if inquiry.status in ['COMPLETED', 'FAILED', 'REFUSED']:
                # Clear session tracker for this inquiry
                if request.session.get('active_engine_pk') == str(inquiry.pk):
                    del request.session['active_engine_pk']
                    request.session.modified = True
                
                # Send one last update then close
                yield f"data: {current_state_json}\n\n"
                break
                
            time.sleep(1) # Poll DB every 1s

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

@login_required
def engine_telemetry(request, pk):
    """Returns a full JSON status of the engine for polling fallback."""
    inquiry = get_object_or_404(Inquiry, pk=pk)
    planets = inquiry.planets.all().order_by('order')
    
    # If terminal state or stale, clear from session
    if inquiry.status in ['COMPLETED', 'FAILED', 'REFUSED']:
        if request.session.get('active_engine_pk') == str(pk):
            del request.session['active_engine_pk']
            request.session.modified = True
            print(f"DEBUG: Cleared session lock for Inquiry {pk} (Terminal State)")

    data = {
        "inquiry_id": str(inquiry.id),
        "status": inquiry.status,
        "message": inquiry.current_status_msg,
        "steps": [
            {
                "order": p.order,
                "name": p.name,
                "status": p.status,
            } for p in planets
        ]
    }
    return JsonResponse(data)

@login_required
def system_map(request):
    """The main view of all inquiries grouped by Topic."""
    all_inquiries = Inquiry.objects.all().order_by("-updated_at")

    # Group inquiries by topic
    topics_dict = {}
    for inq in all_inquiries:
        topic_name = inq.topic or "Uncategorized"

        # Determine if this inquiry is "Active" (has incomplete steps)
        completed_planets = inq.planets.filter(status='COMPLETED').count()
        is_active = completed_planets < 11

        if topic_name not in topics_dict:
            # Get the shared prefix number for this topic folder
            match = re.match(r"case_(\d+)_", inq.case_id)
            prefix = f"CASE_{match.group(1)}" if match else "CASE_XX"
            topics_dict[topic_name] = {
                "name": topic_name,
                "prefix": prefix,
                "inquiries": [],
                "active_count": 0,
                "last_updated": inq.updated_at
            }

        topics_dict[topic_name]["inquiries"].append(inq)
        if is_active:
            topics_dict[topic_name]["active_count"] += 1

        # Update last_updated if this inquiry is more recent
        if inq.updated_at > topics_dict[topic_name]["last_updated"]:
            topics_dict[topic_name]["last_updated"] = inq.updated_at

    # Sort topics by last_updated (descending)
    sorted_topics = sorted(topics_dict.values(), key=lambda x: x["last_updated"], reverse=True)

    # Metacognitive Statistics
    planets_resolved = Planet.objects.filter(status='COMPLETED').count()
    total_planets = Planet.objects.count()
    system_health = (planets_resolved / total_planets * 100) if total_planets > 0 else 100.0

    context = {
        "topics": sorted_topics,
        "total_inquiries": all_inquiries.count(),
        "planets_resolved": planets_resolved,
        "system_health": f"{system_health:.1f}%"
    }
    return render(request, "discovery/index.html", context)

@login_required
def topic_detail(request, topic_name):
    """
    Shows a timeline view of all inquiries within a specific topic folder.
    """
    inquiries_list = Inquiry.objects.filter(topic=topic_name).order_by("created_at")
    if not inquiries_list.exists():
        messages.error(request, f"Topic '{topic_name}' not found.")
        return redirect("discovery:system_map")
    
    # Annotate inquiries with their active status
    inquiries = []
    for inq in inquiries_list:
        completed = inq.planets.filter(status='COMPLETED').count()
        inq.is_active = completed < 11
        inquiries.append(inq)
    
    # Get the sequence prefix from the first inquiry
    match = re.match(r"case_(\d+)_", inquiries[0].case_id)
    topic_prefix = f"CASE_{match.group(1)}" if match else "CASE_XX"
    
    context = {
        "topic_name": topic_name,
        "topic_prefix": topic_prefix,
        "inquiries": inquiries, # Chronological order
    }
    return render(request, "discovery/topic_detail.html", context)

@login_required
def initialize_inquiry(request):
    """POST view to start a new inquiry."""
    # Emergency Lock Override: If user adds ?force=1, we clear the busy state
    if request.GET.get('force') == '1':
        if 'active_engine_pk' in request.session:
            del request.session['active_engine_pk']
            request.session.modified = True
            messages.info(request, "Engine lock manually cleared.")

    # Block concurrent engine runs for the same account
    if _is_engine_busy(request):
        messages.error(request, "Engine Busy: A cognitive process is already active. Please wait for completion.")
        return redirect("discovery:system_map")

    if request.method == "POST":
        question = request.POST.get("question")
        topic_input = request.POST.get("topic")
        
        # Build a case for every single input from a template generated based on the existing cases
        from engine_bridge.services import EngineService
        case_id, topic = EngineService.generate_case_id(question, topic=topic_input)

        inquiry = Inquiry.objects.create(
            case_id=case_id,
            topic=topic,
            core_question=question,
            current_question_state=question
        )
        
        # Trigger the engine run asynchronously via the new Distributed Workflow
        # The worker will handle pre-populating planets (Step 1-11)
        try:
            from .workflow_tasks import start_engine_workflow
            
            # Use CELERY_TASK_ALWAYS_EAGER check to provide immediate fallback if broker is dead
            from django.conf import settings as django_settings
            
            # Dispatch task
            if getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False):
                # If we are in Eager mode (likely local dev without Redis),
                # we MUST use a thread to prevent the UI from freezing.
                run_threaded_task(start_engine_workflow.delay, str(inquiry.id))
            else:
                # Standard Celery dispatch (non-blocking if Redis is running)
                start_engine_workflow.delay(str(inquiry.id))
            
            # Persist the active task state in session for UI persistence
            request.session['active_engine_pk'] = str(inquiry.pk)
            request.session.modified = True
            
            messages.info(request, f"Engine sequence {inquiry.case_id} initiated.")
        except Exception as e:
            import traceback
            error_msg = f"Failed to dispatch workflow: {str(e)}"
            print(f"ERROR: {error_msg}")
            print(traceback.format_exc())
            messages.error(request, error_msg)
            
        return redirect("discovery:inquiry_detail", pk=inquiry.pk)
    
    return render(request, "discovery/initialize.html")

@login_required
def task_status_view(request, task_id):
    """Endpoint to check the status of a Celery task."""
    result = AsyncResult(task_id)
    response_data = {
        "task_id": task_id,
        "status": result.status,
        "ready": result.ready(),
    }
    if result.ready():
        response_data["result"] = result.result if not isinstance(result.result, Exception) else str(result.result)
    
    return JsonResponse(response_data)

@login_required
def inquiry_detail(request, pk):
    """
    LAYER 3: EXPERIENCE LAYER (REDIRECT TO ROOMS)
    The main dash is now replaced by the Discovery Room.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)
    rooms_to_create = [r[0] for r in RoomState.ROOM_CHOICES]
    for r_type in rooms_to_create:
        RoomState.objects.get_or_create(inquiry=inquiry, room_type=r_type)

    return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

@login_required
def room_view(request, pk, room_type):
    """
    Universal Room Renderer for Layer 3.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)
    room_state, _ = RoomState.objects.get_or_create(inquiry=inquiry, room_type=room_type.upper())
    
    # Auto-sync projection if out of date or running
    room_state.sync_from_planets()

    # Map types to templates
    template_map = {
        "DISCOVERY": "discovery/rooms/discovery.html",
        "EVIDENCE": "discovery/rooms/evidence.html",
        "EXPLORATION": "discovery/rooms/exploration.html",
        "SOLUTION": "discovery/rooms/solution.html",
        "PROJECTION": "discovery/rooms/projection.html",
        "GOVERNANCE": "discovery/rooms/governance.html",
        "UNCERTAINTY": "discovery/rooms/uncertainty.html",
        "DECISION": "discovery/rooms/decision.html",
    }
    
    context = {
        "inquiry": inquiry,
        "planets": inquiry.planets.all().order_by('order'),
        "room_type": room_type.upper(),
        "room_data": room_state.room_data,
        "nav_rooms": RoomState.ROOM_CHOICES
    }
    
    response = render(request, template_map.get(room_type.upper(), "discovery/rooms/discovery.html"), context)
    # Force no-cache for live rooms
    if inquiry.status in ['RUNNING', 'PENDING']:
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
    return response

def _process_inquiry_sync_results(inquiry, request, snapshot=None):
    """
    Consolidated metadata update logic for both manual syncs and branching.
    Calculates Confidence based on Epistemic Stability (Article IV Sovereignty).
    Supports Epistemic Contraction rewards (Article VII).
    """
    inquiry.refresh_from_db()
    
    inquiry.history_log.append({
        "timestamp": str(inquiry.updated_at),
        "event": "Full Engine Re-run",
        "trigger": request.POST.get("reason", "Manual Refresh")
    })
    
    # 1. BASE AI CONFIDENCE (Epistemic Input - Step 9 Kernel)
    step_9_planet = inquiry.planets.filter(name__icontains="Step 9").first()
    if not step_9_planet or not step_9_planet.data or not step_9_planet.data.get("confidence"):
        step_9_planet = inquiry.planets.filter(name__icontains="Step 10").first()

    base_ai_confidence = 50
    if step_9_planet and step_9_planet.data:
        raw_confidence = step_9_planet.data.get("confidence") or \
                         step_9_planet.data.get("confidence_rating") or \
                         step_9_planet.data.get("stability_score") or "0"
        c_lower = str(raw_confidence).lower()
        if "high" in c_lower and "medium" not in c_lower: base_ai_confidence = 88
        elif "medium" in c_lower and "low" not in c_lower: base_ai_confidence = 55
        elif "low" in c_lower: base_ai_confidence = 28
        else:
            match = re.search(r"(\d+)", str(raw_confidence))
            if match:
                val = int(match.group(1))
                base_ai_confidence = val * 10 if val <= 10 else val

    # 2. UNCERTAINTY DENSITY (Penalty for unresolved components)
    unresolved_count = len(inquiry.unresolved_zones or [])
    uncertainty_penalty = min(unresolved_count * 7, 45) # Max 45% penalty
    
    # 3. DIVERGENCE VOLATILITY (Reality Forks indicate ambiguity)
    divergence_count = len(inquiry.divergences or [])
    divergence_penalty = min(divergence_count * 6, 30) # Max 30% penalty

    # 4. FRAME DRIFT (Similarity between core and current question)
    q1 = str(inquiry.core_question).lower()
    q2 = str(inquiry.current_question_state).lower()
    drift_score = 100
    if q1 and q2 and q1 != q2:
        overlap = sum(1 for char in q1 if char in q2)
        drift_score = (overlap / max(len(q1), 1)) * 100

    # 5. EPISTEMIC CONTRACTION (Sovereign Recovery Signals)
    recovery_bonus = 0
    
    if snapshot:
        # A. Uncertainty Resolution
        prev_unresolved = snapshot.get('unresolved_count', 0)
        if unresolved_count < prev_unresolved:
            recovery_bonus += (prev_unresolved - unresolved_count) * 12
            
        # B. Divergence Collapse (Pruning reality forks)
        prev_divergences = snapshot.get('divergence_count', 0)
        if divergence_count < prev_divergences:
            recovery_bonus += (prev_divergences - divergence_count) * 10
            
    # C. Convergence Bonus (Stable frame across cycles)
    if drift_score >= 95:
        recovery_bonus += 15
    elif drift_score >= 85:
        recovery_bonus += 8

    # D. Step 10 Completion Bonus (Verdict reached)
    verdict_planet = inquiry.planets.filter(name__icontains="Step 10", status="COMPLETED").exists()
    if verdict_planet:
        recovery_bonus += 20 

    # 6. TEMPORAL STABILITY (Similarity to previous run)
    prev_confidence = 25
    if inquiry.confidence_evolution and len(inquiry.confidence_evolution) > 0:
        prev_confidence = inquiry.confidence_evolution[-1]
    
    # CALCULATE COMPOSITE STABILITY (The "Truth Separator" logic)
    stability_val = (drift_score * 0.4) + (base_ai_confidence * 0.6)
    stability_val -= uncertainty_penalty
    stability_val -= divergence_penalty
    stability_val += recovery_bonus
    
    # Final clamping and moving average smoothing
    final_confidence = (stability_val * 0.75) + (prev_confidence * 0.25)
    final_confidence = max(min(int(final_confidence), 98), 5)

    if not inquiry.confidence_evolution or abs(inquiry.confidence_evolution[-1] - final_confidence) >= 1:
        inquiry.confidence_evolution.append(final_confidence)
        if len(inquiry.confidence_evolution) > 20:
            inquiry.confidence_evolution = inquiry.confidence_evolution[-20:]
    
    inquiry.save()
    
    for room in RoomState.objects.filter(inquiry=inquiry):
        room.sync_from_planets()

@login_required
def spawn_branch_view(request, pk):
    """Handles the creation of a new inquiry branch from a divergence."""
    parent = get_object_or_404(Inquiry, pk=pk)
    
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        
        # 1. Spawn the child
        child = EngineService.spawn_branch(parent, title, description)
        
        # 2. Add specific history to the parent
        parent.history_log.append({
            "timestamp": str(parent.updated_at),
            "event": "Branching Initiated",
            "description": f"Diverged toward Trajectory: {title} (Coupled to avoid drift)",
            "child_id": str(child.id)
        })
        parent.save()
        
        messages.success(request, f"DIVERGENCE INITIATED: Spawning branch for '{title}' (Coupled to parent)...")
        
        # 3. Trigger immediate run for the child
        try:
            from .workflow_tasks import start_engine_workflow
            from django.conf import settings as django_settings
            
            if getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False):
                run_threaded_task(start_engine_workflow.delay, str(child.id))
            else:
                start_engine_workflow.delay(str(child.id))
            
            # Persist tracking
            request.session['active_engine_pk'] = str(child.pk)
            request.session.modified = True
        except Exception as e:
            logger.error(f"Failed to trigger branch workflow: {e}")
            messages.error(request, f"Engine failed to start for branch: {e}")

        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = reverse("discovery:room_view", kwargs={"pk": child.id, "room_type": "DISCOVERY"})
            return response
        else:
            return redirect("discovery:room_view", pk=child.id, room_type="DISCOVERY")
    
    return redirect("discovery:room_view", pk=pk, room_type="DECISION")

@login_required
def sync_engine_pulse(request, pk):
    """
    Invokes Layer 1, Updates Layer 2, Refreshes Layer 3.
    """
    # Block concurrent engine runs for the same account
    if _is_engine_busy(request):
        if request.headers.get('HX-Request'):
            return HttpResponse('<div class="text-red-400 text-[10px] font-bold uppercase p-2 bg-red-500/10 rounded">Engine Busy</div>')
        messages.error(request, "Engine Busy: A cognitive process is already active.")
        return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

    inquiry = get_object_or_404(Inquiry, pk=pk)
    
    # Trigger the engine run asynchronously via Distributed Workflow
    try:
        from .workflow_tasks import start_engine_workflow
        from django.conf import settings as django_settings
        
        if getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False):
            run_threaded_task(start_engine_workflow.delay, str(inquiry.id))
        else:
            start_engine_workflow.delay(str(inquiry.id))
        
        # Persist the active task state in session for UI persistence
        request.session['active_engine_pk'] = str(inquiry.pk)
        request.session.modified = True

        messages.info(request, "Engine Pulse Synchronized. Procedure Re-started.")
    except Exception as e:
        messages.error(request, f"Failed to dispatch workflow: {str(e)}")
    
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Redirect'] = reverse("discovery:room_view", kwargs={"pk": inquiry.id, "room_type": "DISCOVERY"})
        return response

    return redirect("discovery:room_view", pk=inquiry.id, room_type="DISCOVERY")

@login_required
def refine_inquiry(request, pk):
    """
    Takes user feedback, evolves the question using LLM, and re-runs the engine.
    """
    # Block concurrent engine runs for the same account
    if _is_engine_busy(request):
        messages.error(request, "Engine Busy: Please wait for the current process to finish.")
        return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

    inquiry = get_object_or_404(Inquiry, pk=pk)
    directive = request.POST.get("directive", "")
    
    if request.method != "POST" or not directive:
        if not directive:
            messages.warning(request, "Please provide a refinement directive.")
        return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

    try:
        from engine_bridge.services import EngineService
        from .workflow_tasks import start_engine_workflow
        
        # 1. Update the question model
        EngineService.refine_question(inquiry, directive)
        
        # 2. Trigger asynchronous workflow
        from django.conf import settings as django_settings
        if getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False):
            run_threaded_task(start_engine_workflow.delay, str(inquiry.id))
        else:
            start_engine_workflow.delay(str(inquiry.id))
        
        request.session['active_engine_pk'] = str(inquiry.pk)
        request.session.modified = True
        
        messages.success(request, "Inquiry evolved. Re-mapping cognitive substrate in background...")
    except Exception as e:
        messages.error(request, f"Refinement Failed: {str(e)}")
        
    if request.htmx:
        from django_htmx.http import HttpResponseClientRefresh
        return HttpResponseClientRefresh()
        
    return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

@login_required
def branch_out_planet(request, pk):
    """HTMX endpoint to RE-RUN engine based on AI-provided options from Step 2."""
    planet = get_object_or_404(Planet, pk=pk)
    inquiry = planet.inquiry
    
    family_id = request.POST.get("family_id")
    family_desc = request.POST.get("family_desc")
    
    if not family_id:
        return render(request, "discovery/partials/telemetry_entry.html", {
            "log": "DIVERGENCE ERROR: Invalid path selection.",
            "planet": planet, "inquiry": inquiry
        })

    new_perspective = (
        f"DECISION MADE: User selected option [{family_id}]. \n"
        f"DESCRIPTION: {family_desc}\n\n"
        "ACTION: Evolve all downstream steps assuming this is TRUE. Bypass decomposition check."
    )
    
    from .models import ExplorationBranch
    ExplorationBranch.objects.create(
        inquiry=inquiry,
        parent_planet=planet,
        choice_made=f"Resolved via {family_id}",
        branch_data={"perspective_shift": new_perspective, "family_id": family_id}
    )
    
    planet.data["branch_active"] = True
    planet.data["divergence_point"] = f"Resolved via: {family_id}"
    planet.status = "COMPLETED"
    
    # We clear the resolution override during the re-run setup
    # so the engine can provide NEW decomposition axes if the new path 
    # encounters a different deadlock.
    keys_to_fix = ["verdict", "final_verdict", "validation", "analysis"]
    for k in keys_to_fix:
        if k in planet.data and "DECOMPOSITION" in str(planet.data[k]).upper():
            planet.data[k] = f"DIVERGENCE INITIATED: Path {family_id} selected."

    planet.save()
    
    # Mark downstream planets as needing refresh
    inquiry.planets.filter(order__gt=planet.order).update(status="IN_PROGRESS", data={})
    
    # Epistemic Snapshot
    snapshot = {
        "unresolved_count": len(inquiry.unresolved_zones or []),
        "divergence_count": len(inquiry.divergences or []),
    }
    
    try:
        from engine_bridge.services import EngineService
        from .workflow_tasks import start_engine_workflow
        
        original_q = inquiry.core_question
        inquiry.core_question = f"USER CHOICE: {family_desc}\n\n[ORIGINAL QUESTION]: {original_q}"
        inquiry.save()

        # Update planet state
        planet.data["branch_active"] = True 
        planet.data["divergence_point"] = f"Current Thread: {family_id}"
        planet.save()

        # Trigger Workflow
        from django.conf import settings as django_settings
        if getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False):
            run_threaded_task(start_engine_workflow.delay, str(inquiry.id))
        else:
            start_engine_workflow.delay(str(inquiry.id))
        
        request.session['active_engine_pk'] = str(inquiry.pk)
        request.session.modified = True

        return render(request, "discovery/partials/telemetry_entry.html", {
            "log": f"DIVERGENCE TRIGGERED: Path [{family_id}] resolved. Engine restarted in background.",
            "planet": planet, 
            "inquiry": inquiry, 
            "oob_swap": True
        })
    except Exception as e:
        return render(request, "discovery/partials/telemetry_entry.html", {
            "log": f"DIVERGENCE FAILURE: {str(e)}",
            "planet": planet, "inquiry": inquiry
        })

@login_required
def reset_inquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    # Layer 1: Reset Planets (Reasoning Engine Artifacts)
    inquiry.planets.all().update(status="NOT_STARTED", data={})
    
    # Layer 1 Audit: Clear Engine Runs history
    inquiry.engine_runs.all().delete()
    
    # Layer 2: Clear Explorations (Divergence Tree)
    inquiry.explorations.all().delete()
    
    # Layer 3: Reset Room Projections
    inquiry.room_states.all().update(room_data={})
    
    # Reset Inquiry Core State (Layer 2)
    inquiry.current_question_state = inquiry.core_question
    inquiry.assumptions = []
    inquiry.evidence_map = {}
    inquiry.hypothesis_set = {}
    inquiry.solution_families = []
    inquiry.unresolved_zones = []
    inquiry.constraints = []
    inquiry.confidence_evolution = []
    inquiry.state_data = {}
    
    inquiry.history_log = [{
        "timestamp": str(inquiry.updated_at),
        "event": "System Reset",
        "trigger": "Manual Override"
    }]
    
    inquiry.save()
    
    messages.success(request, f"Inquiry '{inquiry.case_id}' has been reset to base state.")
    
    return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

@login_required
def delete_inquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    case_id = inquiry.case_id
    
    # Clear session lock if this was the active engine
    if request.session.get('active_engine_pk') == str(pk):
        del request.session['active_engine_pk']
        request.session.modified = True

    inquiry.delete()
    messages.success(request, f"Inquiry '{case_id}' has been purged from the universe.")
    return redirect("discovery:system_map")

from .models import SpendRecord
from django.db.models import Sum

from django.core.paginator import Paginator

@login_required
def spend_history(request):
    """Real-time financial tracking for all reasoning runs."""
    records_list = SpendRecord.objects.all().order_by("-timestamp")
    
    # Pagination: 20 logs per page
    paginator = Paginator(records_list, 20)
    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)

    total_cost = records_list.aggregate(Sum('cost_usd'))['cost_usd__sum'] or 0.0
    total_tokens = records_list.aggregate(Sum('input_tokens'), Sum('output_tokens'))
    
    context = {
        "records": records,
        "total_cost": total_cost,
        "total_input_tokens": total_tokens['input_tokens__sum'] or 0,
        "total_output_tokens": total_tokens['output_tokens__sum'] or 0,
    }
    return render(request, "discovery/spend_history.html", context)

