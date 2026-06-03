from django.shortcuts import render, get_object_or_404, redirect
from .models import Inquiry, Planet, RoomState, EngineRun, SystemSettings
from django.contrib import messages
from engine_bridge.services import EngineService
import io
import json
import re
from contextlib import redirect_stdout

def system_settings_view(request):
    """View to manage global engine and UI parameters."""
    settings = SystemSettings.get_settings()
    
    if request.method == "POST":
        settings.active_model = request.POST.get("active_model")
        settings.anthropic_api_key = request.POST.get("anthropic_api_key")
        settings.openai_api_key = request.POST.get("openai_api_key")
        settings.offline_mode = request.POST.get("offline_mode") == "on"
        settings.reasoning_depth = int(request.POST.get("reasoning_depth", 7))
        settings.enable_web_search = request.POST.get("enable_web_search") == "on"
        settings.strict_governance = request.POST.get("strict_governance") == "on"
        settings.save()
        messages.success(request, "System parameters updated successfully.")
        return redirect("discovery:settings")

    return render(request, "discovery/settings.html", {"settings": settings})

def system_map(request):
    """The main view of all inquiries."""
    inquiries = Inquiry.objects.all().order_by("-created_at")
    
    # Calculate meaningful metrics
    planets_resolved = Planet.objects.filter(status='COMPLETED').count()
    
    total_planets = Planet.objects.count()
    if total_planets > 0:
        system_health = (planets_resolved / total_planets) * 100
    else:
        system_health = 100.0 # Default to 100% if no operations yet
        
    context = {
        "inquiries": inquiries,
        "planets_resolved": planets_resolved,
        "system_health": f"{system_health:.1f}%"
    }
    return render(request, "discovery/index.html", context)

def initialize_inquiry(request):
    """POST view to start a new inquiry."""
    if request.method == "POST":
        case_id = request.POST.get("case_id")
        question = request.POST.get("question")
        
        inquiry = Inquiry.objects.create(
            case_id=case_id,
            core_question=question,
            current_question_state=question
        )
        
        # Layer 1: Setup hidden engine steps
        steps = [
            ("Step 1: Frame Validation", "fa-vial", 1),
            ("Step 2: Object Decomposition", "fa-dna", 2),
            ("Step 3: Normalization Layer", "fa-balance-scale", 3),
            ("Step 4: Hypothesis Construction", "fa-flask", 4),
            ("Step 5: Falsification Design", "fa-shield-virus", 5),
            ("Step 6: Multi-Scale Propagation", "fa-tower-broadcast", 6),
            ("Step 7: Outside-Frame Generation", "fa-expand", 7),
            ("Step 8: Stage-Gated Roadmap", "fa-route", 8),
            ("Step 9: Constraint Synthesis", "fa-link", 9),
            ("Step 10: Verdict Engine", "fa-gavel", 10),
            ("Step 11: Audit / Drift Layer", "fa-clipboard-check", 11),
        ]
        
        for i, (name, icon, order) in enumerate(steps):
            Planet.objects.create(
                inquiry=inquiry,
                name=name,
                icon_class=icon,
                order=order,
                status="NOT_STARTED"
            )
            
        return redirect("discovery:inquiry_detail", pk=inquiry.pk)
    
    return render(request, "discovery/initialize.html")

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

def room_view(request, pk, room_type):
    """
    Universal Room Renderer for Layer 3.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)
    room_state, _ = RoomState.objects.get_or_create(inquiry=inquiry, room_type=room_type.upper())
    
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
        "room_type": room_type.upper(),
        "room_data": room_state.room_data,
        "nav_rooms": RoomState.ROOM_CHOICES
    }
    
    return render(request, template_map.get(room_type.upper(), "discovery/rooms/discovery.html"), context)

def sync_engine_pulse(request, pk):
    """
    Invokes Layer 1, Updates Layer 2, Refreshes Layer 3.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)
    inquiry.planets.all().update(status="IN_PROGRESS")
    
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            EngineService.run_full_procedure(inquiry)
        messages.success(request, "Engine propagation successful. All rooms updated.")
    except Exception as e:
        messages.error(request, f"Engine Failure: {str(e)}")
        # Log the traceback for debugging
        import traceback
        print(traceback.format_exc())
    
    # Refresh metadata
    inquiry.refresh_from_db()
    inquiry.history_log.append({
        "timestamp": str(inquiry.updated_at),
        "event": "Full Engine Re-run",
        "trigger": request.POST.get("reason", "Manual Refresh")
    })
    
    # Extract Confidence from Step 9
    step_9_planet = inquiry.planets.filter(name__icontains="Step 9").first()
    if step_9_planet and step_9_planet.data:
        raw_confidence = step_9_planet.data.get("confidence", "0")
        c_lower = str(raw_confidence).lower()
        if "high" in c_lower and "medium" not in c_lower:
            confidence_val = 85
        elif "medium-high" in c_lower or "high-medium" in c_lower:
            confidence_val = 72
        elif "medium" in c_lower and "high" not in c_lower and "low" not in c_lower:
            confidence_val = 55
        elif "low-medium" in c_lower:
            confidence_val = 40
        elif "low" in c_lower:
            confidence_val = 25
        else:
            match = re.search(r"(\d+)", str(raw_confidence))
            confidence_val = int(match.group(1)) if match else 50
            
        inquiry.confidence_evolution.append(confidence_val)
    
    inquiry.save()
    
    for room in RoomState.objects.filter(inquiry=inquiry):
        room.sync_from_planets()
    
    if request.htmx:
        from django_htmx.http import HttpResponseClientRefresh
        return HttpResponseClientRefresh()
        
    return redirect(request.META.get('HTTP_REFERER', 'discovery:inquiry_detail'))

def refine_inquiry(request, pk):
    """
    Takes user feedback, evolves the question using LLM, and re-runs the engine.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)
    directive = request.POST.get("directive", "")
    
    if request.method != "POST" or not directive:
        if not directive:
            messages.warning(request, "Please provide a refinement directive.")
        return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

    try:
        from engine_bridge.services import EngineService
        EngineService.refine_and_run(inquiry, directive)
        messages.success(request, "Inquiry evolved successfully. New roadmap generated.")
    except Exception as e:
        messages.error(request, f"Refinement Failed: {str(e)}")
        
    if request.htmx:
        from django_htmx.http import HttpResponseClientRefresh
        return HttpResponseClientRefresh()
        
    return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

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
    
    f = io.StringIO()
    try:
        from engine_bridge.services import EngineService
        original_q = inquiry.core_question
        inquiry.core_question = f"USER CHOICE: {family_desc}\n\n[ORIGINAL QUESTION]: {original_q}"
        
        with redirect_stdout(f):
            EngineService.run_full_procedure(inquiry)
        
        # Refresh to get engine output
        planet.refresh_from_db()
        
        # Re-attach the divergence history but DON'T delete the new axes 
        # returned by the engine (if any)
        planet.data["branch_active"] = True 
        planet.data["divergence_point"] = f"Current Thread: {family_id}"
        planet.save()

        inquiry.core_question = original_q
        inquiry.save()
        
        execution_logs = f.getvalue()
        combined_log = f"DIVERGENCE TRIGGERED: Path [{family_id}] resolved.\n\n{execution_logs}"
        
        return render(request, "discovery/partials/telemetry_entry.html", {
            "log": combined_log,
            "planet": planet, 
            "inquiry": inquiry, 
            "oob_swap": True
        })
    except Exception as e:
        return render(request, "discovery/partials/telemetry_entry.html", {
            "log": f"DIVERGENCE FAILURE: {str(e)}",
            "planet": planet, "inquiry": inquiry
        })

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

def delete_inquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    case_id = inquiry.case_id
    inquiry.delete()
    messages.success(request, f"Inquiry '{case_id}' has been purged from the universe.")
    return redirect("discovery:system_map")

