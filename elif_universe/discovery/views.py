from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Sum
from .models import Inquiry, Planet, RoomState, EngineRun, SystemSettings, SpendRecord
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from engine_bridge.services import EngineService
import io
import json
import re
from contextlib import redirect_stdout

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
def documentation_view(request):
    """Protocol Documentation and Tutorials."""
    return render(request, "discovery/documentation.html")

@login_required
def engine_telemetry(request, pk):
    """Returns the current engine status for an inquiry."""
    inquiry = get_object_or_404(Inquiry, pk=pk)
    return HttpResponse(inquiry.current_status_msg)

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
        
        # Trigger the engine run automatically on creation
        try:
            EngineService.run_full_procedure(inquiry)
            _process_inquiry_sync_results(inquiry, request)
        except Exception as e:
            print(f"Initial Engine Run Failed: {e}")
            
        return redirect("discovery:inquiry_detail", pk=inquiry.pk)
    
    return render(request, "discovery/initialize.html")

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
    prev_confidence = inquiry.confidence_evolution[-1] if inquiry.confidence_evolution else base_ai_confidence
    
    # CALCULATE COMPOSITE STABILITY (The "Truth Separator" logic)
    # Stability = (Structural * 0.4) + (Reasoning * 0.6) - Penalties + Rewards
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
            "description": f"Diverged toward Trajectory: {title}",
            "child_id": str(child.id)
        })
        parent.save()
        
        messages.success(request, f"DIVERGENCE INITIATED: Spawning branch for '{title}'...")
        
        # 3. Trigger immediate run for the child
        from django.http import HttpResponse
        
        # Pre-initialize logic
        if not child.planets.exists():
            from .models import Planet
            steps = [
                ("Step 1: Frame Validation", "fa-microscope", 1),
                ("Step 2: Object Decomposition", "fa-cubes", 2),
                ("Step 3: Normalization Layer", "fa-layer-group", 3),
                ("Step 4: Hypothesis Construction", "fa-vial", 4),
                ("Step 5: Falsification Design", "fa-shield-virus", 5),
                ("Step 6: Multi-Scale Propagation", "fa-tower-broadcast", 6),
                ("Step 7: Outside-Frame Generation", "fa-expand", 7),
                ("Step 8: Stage-Gated Roadmap", "fa-route", 8),
                ("Step 9: Constraint Synthesis", "fa-link", 9),
                ("Step 10: Verdict Engine", "fa-gavel", 10),
                ("Step 11: Audit / Drift Layer", "fa-clipboard-check", 11),
            ]
            for p_name, icon, order in steps:
                Planet.objects.get_or_create(
                    inquiry=child, name=p_name,
                    defaults={"icon_class": icon, "order": order, "status": "NOT_STARTED"}
                )

            ROOM_TYPES = ['DISCOVERY', 'FRAME', 'OBJECT', 'UNCERTAINTY', 'PROPAGATION', 'OUTSIDE', 'DECISION', 'AUDIT']
            for rt in ROOM_TYPES:
                RoomState.objects.get_or_create(inquiry=child, room_type=rt)

        # Trigger the engine run immediately
        try:
            EngineService.run_full_procedure(child)
            # Sync metadata (Confidence, History) for the CHILD
            _process_inquiry_sync_results(child, request, snapshot=None)
        except:
            pass

        response = HttpResponse()
        response['HX-Redirect'] = reverse("discovery:room_view", kwargs={"pk": child.id, "room_type": "DISCOVERY"})
        return response
    
    return redirect("discovery:room_view", pk=pk, room_type="DECISION")

@login_required
def sync_engine_pulse(request, pk):
    """
    Invokes Layer 1, Updates Layer 2, Refreshes Layer 3.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)
    
    # Initialize planets if they don't exist
    if not inquiry.planets.exists():
        from .models import Planet
        steps = [
            ("Step 1: Frame Validation", "fa-microscope", 1),
            ("Step 2: Object Decomposition", "fa-cubes", 2),
            ("Step 3: Normalization Layer", "fa-layer-group", 3),
            ("Step 4: Hypothesis Construction", "fa-vial", 4),
            ("Step 5: Falsification Design", "fa-shield-virus", 5),
            ("Step 6: Multi-Scale Propagation", "fa-tower-broadcast", 6),
            ("Step 7: Outside-Frame Generation", "fa-expand", 7),
            ("Step 8: Stage-Gated Roadmap", "fa-route", 8),
            ("Step 9: Constraint Synthesis", "fa-link", 9),
            ("Step 10: Verdict Engine", "fa-gavel", 10),
            ("Step 11: Audit / Drift Layer", "fa-clipboard-check", 11),
        ]
        for name, icon, order in steps:
            Planet.objects.create(
                inquiry=inquiry,
                name=name,
                icon_class=icon,
                order=order,
                status="NOT_STARTED"
            )

    inquiry.planets.all().update(status="IN_PROGRESS")
    
    # Capture Epistemic Snapshot for contraction calculation
    snapshot = {
        "unresolved_count": len(inquiry.unresolved_zones or []),
        "divergence_count": len(inquiry.divergences or []),
    }
    
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            from engine_bridge.services import EngineService
            EngineService.run_full_procedure(inquiry)
        messages.success(request, "Engine propagation successful. All rooms updated.")
    except Exception as e:
        messages.error(request, f"Engine Failure: {str(e)}")
        import traceback
        print(traceback.format_exc())
    
    # Process metadata (Confidence, History)
    _process_inquiry_sync_results(inquiry, request, snapshot=snapshot)
    
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
    inquiry = get_object_or_404(Inquiry, pk=pk)
    directive = request.POST.get("directive", "")
    
    if request.method != "POST" or not directive:
        if not directive:
            messages.warning(request, "Please provide a refinement directive.")
        return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

    try:
        from engine_bridge.services import EngineService
        
        # Capture snapshot for epistemic contraction
        snapshot = {
            "unresolved_count": len(inquiry.unresolved_zones or []),
            "divergence_count": len(inquiry.divergences or []),
        }
        
        EngineService.refine_and_run(inquiry, directive)
        
        # Process results with snapshot
        _process_inquiry_sync_results(inquiry, request, snapshot=snapshot)
        
        messages.success(request, "Inquiry evolved successfully. New roadmap generated.")
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
    
    f = io.StringIO()
    try:
        from engine_bridge.services import EngineService
        original_q = inquiry.core_question
        inquiry.core_question = f"USER CHOICE: {family_desc}\n\n[ORIGINAL QUESTION]: {original_q}"
        
        with redirect_stdout(f):
            EngineService.run_full_procedure(inquiry)
        
        # Process Results
        _process_inquiry_sync_results(inquiry, request, snapshot=snapshot)
        
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

