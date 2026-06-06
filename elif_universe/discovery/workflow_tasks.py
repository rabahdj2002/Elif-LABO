import logging
from celery import shared_task, chain
from django.db import transaction
from django.conf import settings as django_settings
from datetime import datetime
from .models import Inquiry, Planet
from engine_bridge.services import EngineService
import time
import re

logger = logging.getLogger(__name__)

STEP_IDS = [
    "step_1", "step_2", "step_3", "step_4", "step_5", 
    "step_6", "step_7", "step_8", "step_9", "step_10", "step_11"
]

STEP_NAMES = {
    "step_1": "Frame Validation",
    "step_2": "Object Decomposition",
    "step_3": "Normalization Layer",
    "step_4": "Hypothesis Construction",
    "step_5": "Falsification Design",
    "step_6": "Multi-Scale Propagation",
    "step_7": "Outside-Frame Generation",
    "step_8": "Stage-Gated Roadmap",
    "step_9": "Constraint Synthesis",
    "step_10": "Verdict Engine",
    "step_11": "Audit / Drift Layer",
}

@shared_task(name='discovery.start_engine_workflow')
def start_engine_workflow(inquiry_id):
    """
    Kicks off a distributed Celery chain for the ELIF engine.
    Supports both Celery worker (Async) and Eager Mode (Sync) execution.
    """
    logger.info(f"STARTING WORKFLOW FOR INQUIRY: {inquiry_id}")
    try:
        is_eager = getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False)
        inquiry = Inquiry.objects.get(pk=inquiry_id)
        
        # Ensure Planets exist for tracking before starting the chain
        with transaction.atomic():
            inquiry.status = 'RUNNING'
            inquiry.current_status_msg = "Distributed Workflow Initialized. Starting Step 1..."
            inquiry.save(update_fields=['status', 'current_status_msg'])

            # Pre-create or reset planets so the UI has a consistent timeline
            for step_id, display_name in STEP_NAMES.items():
                order = int(step_id.split('_')[1])
                Planet.objects.update_or_create(
                    inquiry=inquiry, 
                    order=order,
                    defaults={'name': display_name, 'status': 'NOT_STARTED'}
                )
        
        logger.info(f"PLANETS CREATED FOR {inquiry_id}")

        if is_eager:
            logger.info(f"SYNC EAGER MODE: Executing steps sequentially for {inquiry_id}")
            res = "START"
            for s_id in STEP_IDS:
                res = execute_engine_step_task(res, inquiry_id, s_id)
            finalize_engine_workflow_task(res, inquiry_id)
            return {"status": "completed_sync", "inquiry_id": str(inquiry_id)}

        # Create the chain for Async Mode
        workflow = chain(
            execute_engine_step_task.s("START", inquiry_id, "step_1"),
            execute_engine_step_task.s(inquiry_id, "step_2"),
            execute_engine_step_task.s(inquiry_id, "step_3"),
            execute_engine_step_task.s(inquiry_id, "step_4"),
            execute_engine_step_task.s(inquiry_id, "step_5"),
            execute_engine_step_task.s(inquiry_id, "step_6"),
            execute_engine_step_task.s(inquiry_id, "step_7"),
            execute_engine_step_task.s(inquiry_id, "step_8"),
            execute_engine_step_task.s(inquiry_id, "step_9"),
            execute_engine_step_task.s(inquiry_id, "step_10"),
            execute_engine_step_task.s(inquiry_id, "step_11"),
            finalize_engine_workflow_task.s(inquiry_id)
        )
        res = workflow.apply_async()
        logger.info(f"CHAIN DISPATCHED FOR {inquiry_id}. Task Group ID: {res.id}")
        return {"status": "started", "inquiry_id": str(inquiry_id), "task_id": res.id}
    except Exception as e:
        logger.exception(f"ERROR: Failed to start workflow for Inquiry {inquiry_id}")
        try:
            Inquiry.objects.filter(pk=inquiry_id).update(
                status='FAILED',
                current_status_msg=f"Workflow dispatch error: {str(e)}"
            )
        except: pass
        return {"status": "error", "message": str(e)}

@shared_task(bind=True, name='discovery.execute_engine_step_task', max_retries=1)
def execute_engine_step_task(self, prev_result, inquiry_id, step_id):
    """
    Independent Celery task for a single procedure step.
    Supports retries, eager-mode arg shifting, and incremental state updates.
    """
    # Arg shifting for Eager Mode / Direct calls
    if isinstance(self, (str, type(None))) or not hasattr(self, 'request'):
        step_id_actual = inquiry_id
        inquiry_id_actual = prev_result
        prev_result_actual = self
        step_id, inquiry_id, prev_result = step_id_actual, inquiry_id_actual, prev_result_actual
        self = None

    if prev_result in ["error", "skipped", False]:
        return "skipped"

    start_time = time.time()
    try:
        inquiry = Inquiry.objects.get(pk=inquiry_id)
        if inquiry.status in ['REFUSED', 'FAILED', 'DELETED']:
            return "skipped"

        display_name = STEP_NAMES.get(step_id, step_id)
        order = int(step_id.split('_')[1])
        
        with transaction.atomic():
            inquiry.status = 'RUNNING'
            inquiry.current_status_msg = f"Executing {display_name}..."
            inquiry.save(update_fields=['status', 'current_status_msg'])
            Planet.objects.filter(inquiry=inquiry, order=order).update(status='IN_PROGRESS')

        # Check if we should use serverless or local execution
        engine_url = getattr(django_settings, 'ELIF_ENGINE_URL', None)
        
        prior_outputs = {f"step_{p.order}": p.data for p in inquiry.planets.filter(status='COMPLETED').order_by('order')}

        if engine_url:
            logger.info(f"Step {step_id} starting (SERVERLESS) for Inquiry {inquiry_id}")
            serverless_payload = EngineService.get_serverless_payload(inquiry, step_id, prior_outputs)
            result = EngineService.call_serverless_engine(serverless_payload)
            
            if result.get("status") != "success":
                raise Exception(f"Engine returned failure: {result.get('error')}")
                
            payload = result.get("payload")
            usage = result.get("usage", {})
        else:
            logger.info(f"Step {step_id} starting (LOCAL) for Inquiry {inquiry_id}")
            runner, run_context, components, input_frame = EngineService.initialize_orchestration(inquiry)
            payload, usage = runner.execute_step(
                step_id=step_id,
                run_context=run_context,
                components=components,
                input_frame=input_frame,
                prior_outputs=prior_outputs
            )

        from discovery.models import SpendRecord
        with transaction.atomic():
            Planet.objects.filter(inquiry=inquiry, order=order).update(status='COMPLETED', data=payload)
            record = SpendRecord.objects.create(
                inquiry=inquiry, step_name=display_name, model_id=usage.get("model_id", "unknown"),
                input_tokens=usage.get("input_tokens", 0), output_tokens=usage.get("output_tokens", 0)
            )
            record.calculate_cost()
            record.save()
            
            step_num = int(step_id.split('_')[1])
            progress_base = (step_num / 11.0) * 50.0
            density_bonus = min(40.0, len([v for v in payload.values() if v]) * 5.0) if isinstance(payload, dict) else 0
            current_mark = int(max(10, min(95, progress_base + density_bonus)))
            inquiry.confidence_evolution.append(current_mark)
            
            # Map step number to investigation status
            if step_num <= 3:
                inquiry.investigation_status = "Emerging"
            elif step_num <= 7:
                inquiry.investigation_status = "In-Depth"
            elif step_num <= 10:
                inquiry.investigation_status = "Synthesizing"
            else:
                inquiry.investigation_status = "Validated"
                
            inquiry.save(update_fields=['confidence_evolution', 'investigation_status'])

            for room_state in inquiry.room_states.all():
                room_state.sync_from_planets()

            if step_id == "step_1" and payload.get("verdict") == "invalid":
                inquiry.status = 'REFUSED'
                inquiry.investigation_status = "Refused"
                inquiry.current_status_msg = "Frame Invalid. Halting."
                inquiry.is_visible_to_user = False
                inquiry.save(update_fields=['status', 'investigation_status', 'current_status_msg', 'is_visible_to_user'])
                
                # SCRUB DIVERSION: Remove this trajectory from parent if it was a branch
                _scrub_parent_diversion(inquiry)
                return "skipped"

            if step_id == "step_9" and payload.get("verdict") == "refuse":
                inquiry.status = 'REFUSED'
                inquiry.investigation_status = "Refused"
                inquiry.current_status_msg = "Governance Refusal. Halting."
                inquiry.is_visible_to_user = False
                inquiry.save(update_fields=['status', 'investigation_status', 'current_status_msg', 'is_visible_to_user'])
                
                # SCRUB DIVERSION: Remove this trajectory from parent if it was a branch
                _scrub_parent_diversion(inquiry)
                return "skipped"

        return "success"
    except Exception as e:
        logger.exception(f"Step {step_id} failed: {str(e)}")
        if self and self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=5)
        Inquiry.objects.filter(pk=inquiry_id).update(status='FAILED', current_status_msg=f"Failed at {step_id}: {str(e)}")
        return "error"

def _scrub_parent_diversion(inquiry):
    """If this was a branch, remove the matching trajectory from the parent's Decision Room."""
    if inquiry.parent_inquiry and inquiry.branch_name:
        parent = inquiry.parent_inquiry
        
        # 1. Scrub from persistent JSONField
        if parent.divergences:
            original_count = len(parent.divergences)
            parent.divergences = [
                d for d in parent.divergences 
                if (d.get('title') if isinstance(d, dict) else str(d)) != inquiry.branch_name
            ]
            if len(parent.divergences) != original_count:
                parent.save(update_fields=['divergences'])
                logger.info(f"Scrubbed diversion '{inquiry.branch_name}' from parent {parent.id} JSONField")

        # 2. Scrub from Step 7 Planet data to prevent fallback re-population
        step7 = parent.planets.filter(order=7).first()
        if step7 and step7.data and 'trajectories' in step7.data:
            original_count = len(step7.data['trajectories'])
            step7.data['trajectories'] = [
                t for t in step7.data['trajectories']
                if (t.get('tag', t.get('title', str(t))) if isinstance(t, dict) else str(t)) != inquiry.branch_name
            ]
            if len(step7.data['trajectories']) != original_count:
                step7.save(update_fields=['data'])
                logger.info(f"Scrubbed diversion '{inquiry.branch_name}' from parent {parent.id} Planet 7")

        # 3. Sync the parent's RoomState so the Decision Room updates immediately
        for rs in parent.room_states.all():
            rs.sync_from_planets()

@shared_task(name='discovery.finalize_engine_workflow_task')
def finalize_engine_workflow_task(prev_result, inquiry_id):
    """
    Consolidates planet data into Inquiry fields and closes the workflow.
    """
    logger.info(f"FINALIZING WORKFLOW FOR INQUIRY: {inquiry_id}")
    try:
        inquiry = Inquiry.objects.get(pk=inquiry_id)
        if inquiry.status in ['REFUSED', 'FAILED', 'DELETED']:
            return "halted"

        planets = {p.order: p.data for p in inquiry.planets.filter(status='COMPLETED')}
        
        with transaction.atomic():
            if 9 in planets: inquiry.final_verdict = planets[9].get("verdict", "N/A")
            if 1 in planets: inquiry.current_question_state = planets[1].get("reformulated_frame", inquiry.core_question)
            if 3 in planets: inquiry.assumptions = planets[3].get("assumptions", [])
            
            # UNRESOLVED SEMANTIC ZONES (Step 11 Core)
            # Prioritize Step 11 "entries" or Step 9 "unresolved_uncertainty_sources"
            if 11 in planets:
                inquiry.unresolved_zones = planets[11].get("unresolved_zones", []) or planets[11].get("entries", [])
            elif 9 in planets:
                # Step 9 is the primary source of uncertainty if Step 11 is not present
                inquiry.unresolved_zones = planets[9].get("unresolved_uncertainty_sources", [])
            
            if 7 in planets:
                raw_trajs = planets[7].get("trajectories", [])
                inquiry.divergences = [{
                    "title": t.get('tag') or t.get('title') or "Alternative Trajectory",
                    "description": t.get('reason') or t.get('description') or "No details.",
                    "confidence_impact": t.get('confidence_impact', "High")
                } if isinstance(t, dict) else {"title": "Trajectory", "description": str(t)} for t in raw_trajs]

            if 8 in planets:
                stages = planets[8].get("stages", []) if isinstance(planets[8], dict) else []
                inquiry.solution_families = [{
                    "name": s.get("title", f"Stage {s.get('stage_id')}") if isinstance(s, dict) else "Unknown",
                    "description": s.get("description", "") if isinstance(s, dict) else str(s),
                    "confidence": 85 
                } for s in stages]

            inquiry.status = 'COMPLETED'
            inquiry.current_status_msg = "Workflow Complete."
            inquiry.completion_date = datetime.now()
            inquiry.save()

            for room_state in inquiry.room_states.all():
                room_state.sync_from_planets()
                room_state.save()
        return "success"
    except Exception as e:
        logger.exception(f"Finalization failed: {e}")
        return "error"
