import logging
from celery import shared_task
from .models import Inquiry, Planet
from engine_bridge.services import EngineService
import re
from .workflow_tasks import *

logger = logging.getLogger(__name__)

@shared_task(bind=True, name='discovery.run_engine_task')
def run_engine_task(self, inquiry_id):
    """
    Refactored Celery task using a State Machine design for high scalability.
    Executes the 11-step ELIF procedure incrementally, emitting progress.
    """
    from django.utils import timezone
    from discovery.models import Inquiry, Planet
    from engine_bridge.services import EngineService
    import logging

    logger = logging.getLogger(__name__)
    inquiry = None
    
    try:
        inquiry = Inquiry.objects.get(pk=inquiry_id)
        inquiry.status = 'RUNNING'
        inquiry.save(update_fields=['status'])
        
        logger.info(f"[JOB {self.request.id}] Starting State Machine for Inquiry {inquiry_id}")

        # 1. Initialize Engine Components
        inquiry.current_status_msg = "Booting Engine & Initializing Components..."
        inquiry.save(update_fields=['current_status_msg'])
        
        runner, run_context, components, input_frame = EngineService.initialize_orchestration(inquiry)
        
        prior_outputs = {}
        step_ids = ["step_1", "step_2", "step_3", "step_4", "step_5", "step_6", "step_7", "step_8", "step_9", "step_10", "step_11"]
        
        step_names = {
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

        # 2. Sequential Step Execution (State Machine Loop)
        for idx, step_id in enumerate(step_ids, 1):
            # Update Inquiry Status
            display_name = step_names.get(step_id, step_id)
            inquiry.current_status_msg = f"Executing {display_name} ({idx}/11)..."
            inquiry.save(update_fields=['current_status_msg'])
            
            # Update Planet UI Status
            planet = Planet.objects.filter(inquiry=inquiry, order=idx).first()
            if planet:
                planet.status = 'IN_PROGRESS'
                planet.save(update_fields=['status'])

            logger.info(f"[JOB {self.request.id}] [{step_id}] Starting {display_name}")

            # ACTUAL ENGINE EXECUTION
            try:
                payload = runner.execute_step(
                    step_id=step_id,
                    run_context=run_context,
                    components=components,
                    input_frame=input_frame,
                    prior_outputs=prior_outputs
                )
                
                # Commit results
                prior_outputs[step_id] = payload
                
                # Update Planet with result data
                if planet:
                    planet.status = 'COMPLETED'
                    planet.data = payload
                    planet.save(update_fields=['status', 'data'])
                
                logger.info(f"[JOB {self.request.id}] [{step_id}] Completed successfully.")
                
                # Early exit condition (Article II Refusal in Step 1)
                if step_id == "step_1" and payload.get("verdict") == "invalid":
                    inquiry.current_status_msg = "Frame Invalid. Halting according to Article II."
                    inquiry.status = 'REFUSED'
                    inquiry.save(update_fields=['current_status_msg', 'status'])
                    logger.warning(f"[JOB {self.request.id}] Step 1 Refusal. Halting.")
                    break

            except Exception as step_exc:
                logger.error(f"[JOB {self.request.id}] [{step_id}] FAILED: {str(step_exc)}")
                if planet:
                    planet.status = 'FAILED'
                    planet.save(update_fields=['status'])
                raise step_exc

        # 3. Finalize Inquiry
        if inquiry.status != 'REFUSED':
            inquiry.status = 'COMPLETED'
            inquiry.current_status_msg = "Procedure completed. Verdict finalized."
            
            # Extract final metrics from step_11 summary if available
            final_summary = prior_outputs.get("step_11", {})
            if final_summary:
                inquiry.final_verdict = final_summary.get("final_verdict", "N/A")
            
            inquiry.save(update_fields=['status', 'current_status_msg', 'final_verdict', 'updated_at'])
        
        # Post-process (Confidence/Evolution)
        _process_inquiry_async_results(inquiry)
        
        logger.info(f"[JOB {self.request.id}] Engine procedure finished for Inquiry {inquiry_id}")
        return {"status": "success", "inquiry_id": str(inquiry_id)}
        
    except Inquiry.DoesNotExist:
        logger.error(f"Inquiry {inquiry_id} not found.")
        return {"status": "error", "message": "Inquiry not found"}
    except Exception as e:
        logger.exception(f"[JOB {self.request.id}] Engine task failed for Inquiry {inquiry_id}: {str(e)}")
        if inquiry:
            inquiry.current_status_msg = f"Engine Error: {str(e)}"
            inquiry.status = 'FAILED'
            inquiry.save(update_fields=['current_status_msg', 'status'])
        raise self.retry(exc=e, countdown=30, max_retries=2)

def _process_inquiry_async_results(inquiry):
    """
    High-fidelity confidence calculation for background tasks.
    """
    inquiry.refresh_from_db()
    
    # 1. AI Signal Axis (Step 9 Kernel)
    p9 = inquiry.planets.filter(order=9).first()
    base_confidence = 70.0
    
    if p9 and p9.data:
        ai_signal = p9.data.get("confidence", "").lower()
        if "high" in ai_signal: base_confidence = 92.0
        elif "medium" in ai_signal: base_confidence = 72.0
        elif "low" in ai_signal: base_confidence = 35.0
        
    if inquiry.final_verdict == "refuse":
        base_confidence = max(base_confidence, 85.0)

    # 2. Darkness Axis (Uncertainty Density)
    unresolved = p9.data.get("unresolved_uncertainty_sources", []) if p9 and p9.data else []
    darkness_penalty = len(unresolved) * 4.5
    
    # 3. Assumption Axis
    assumption_penalty = len(inquiry.assumptions or []) * 2.5
    
    # Final Score Calculation
    final_score = max(5, min(99, base_confidence - darkness_penalty - assumption_penalty))
    
    # Update evolution
    if not isinstance(inquiry.confidence_evolution, list):
        inquiry.confidence_evolution = []
    inquiry.confidence_evolution.append(int(final_score))
    
    inquiry.history_log.append({
        "timestamp": str(inquiry.updated_at),
        "event": "Finalized Confidence (HF Audit)",
        "score": f"{final_score}%"
    })
    
    inquiry.save()

@shared_task(name='discovery.reset_monthly_usage')
def reset_monthly_usage():
    """
    Background worker to check and reset all active subscriptions.
    Usually runs nightly via Celery Beat.
    """
    from discovery.models import UserSubscription
    subs = UserSubscription.objects.all()
    reset_count = 0
    for sub in subs:
        if sub.check_cycle_reset():
            reset_count += 1
    return f"Processed {subs.count()} subscriptions. Reset_count: {reset_count}"
