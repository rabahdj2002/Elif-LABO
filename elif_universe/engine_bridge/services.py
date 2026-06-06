import sys
import re
from pathlib import Path
from django.conf import settings

# Ensure engine is in path
if str(settings.ENGINE_SRC) not in sys.path:
    sys.path.append(str(settings.ENGINE_SRC))

from elif_v0_1.orchestration_runner import ProcedureRunner
from elif_v0_1.base import InputFrame
from discovery.models import SystemSettings
import uuid
import langdetect
from langdetect import detect, DetectorFactory

# Set seed for reproducible language detection
DetectorFactory.seed = 0

class EngineService:
    @staticmethod
    def _detect_language(text):
        """Robust language detection for ELIF engine using langdetect."""
        # 1. Arabic Script Detection (High Reliability for RTL script)
        if re.search(r'[\u0600-\u06FF]', text):
            return "Arabic"
        
        # 2. Advanced detection using langdetect for all supported languages
        try:
            # Map ISO codes to full names for the prompt
            iso_map = {
                'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali', 'ca': 'Catalan', 
                'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 
                'en': 'English', 'es': 'Spanish', 'et': 'Estonian', 'fa': 'Persian', 'fi': 'Finnish', 
                'fr': 'French', 'gu': 'Gujarati', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian', 
                'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'kn': 'Kannada', 
                'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'mk': 'Macedonian', 'ml': 'Malayalam', 
                'mr': 'Marathi', 'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'pa': 'Punjabi', 
                'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak', 
                'sl': 'Slovenian', 'so': 'Somali', 'sq': 'Albanian', 'sv': 'Swedish', 'sw': 'Swahili', 
                'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tl': 'Tagalog', 'tr': 'Turkish', 
                'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-cn': 'Chinese', 'zh-tw': 'Chinese'
            }
            detected_code = detect(text)
            return iso_map.get(detected_code, "English")
        except Exception:
            # Heuristic Fallback for very short strings or failed detection
            text_lower = text.lower()
            
            french_heuristics = [
                r'\b(est-ce|comment|pourquoi|pour|dans|quelle|est|la|cause|plus|probable|ma|voiture|ne|démarre|plus|le|moteur|se|lance|pas|problème|panne|aide|moi)\b',
                r'\b(l\'|d\'|qu\'|j\'|m\'|t\'|s\')',  # French apostrophes
                r'[éèêëàâîïôûùç]' # French accents
            ]
            
            spanish_heuristics = [
                r'\b(qué|cómo|cuál|donde|quién|por|con|para|más|esta|esta|coche|motor|arranca|problema)\b',
                r'[áéíóúñ¿¡]' # Spanish marks
            ]

            if any(re.search(h, text_lower) for h in french_heuristics):
                return "French"
            if any(re.search(h, text_lower) for h in spanish_heuristics):
                return "Spanish"
            
        return "English"

    @staticmethod
    def generate_case_id(question, topic=None):
        """
        Generates a case ID and topic purely locally to prevent blocking the UI.
        Determining the optimized topic can be handled later in the process.
        """
        import uuid
        import re
        from discovery.models import Inquiry
        
        # 1. Determine Topic (Default if not provided)
        final_topic = topic if topic and topic.strip() else "General"
        
        # 2. Generate a unique suffix
        suffix = uuid.uuid4().hex[:6]

        # 3. Assign or retrieve the Sequence Number for this topic
        existing_with_topic = Inquiry.objects.filter(topic__iexact=final_topic).first()
        
        if existing_with_topic:
            match = re.match(r"case_(\d+)_", existing_with_topic.case_id)
            seq_num = match.group(1) if match else "99"
        else:
            # New topic, find next available sequence
            all_inquiries = Inquiry.objects.all()
            max_seq = 0
            for inq in all_inquiries:
                match = re.match(r"case_(\d+)_", inq.case_id)
                if match:
                    try:
                        num = int(match.group(1))
                        if num > max_seq: max_seq = num
                    except: pass
            seq_num = f"{max_seq + 1:02d}"

        final_case_id = f"case_{seq_num}_{suffix}"
        return final_case_id, final_topic

    @staticmethod
    def spawn_branch(parent_inquiry, divergence_title, trajectory_description):
        """Creates a new Inquiry as a branch of a parent divergence."""
        from discovery.models import Inquiry, Planet
        import uuid
        
        # 1. Create the child inquiry with a COMPOUND core question
        # We explicitly state the goal of finding better results and increasing confidence.
        # Coupled with parent findings to avoid drift.
        parent_verdict = parent_inquiry.final_verdict or "NOT_YET_REACHED"
        parent_assumptions = ", ".join(parent_inquiry.assumptions[:3]) if parent_inquiry.assumptions else "None yet identified"
        
        compound_question = (
            f"DIVERGENCE BRANCH: {divergence_title}\n\n"
            f"[CONTEXT]: {trajectory_description}\n"
            f"[PARENT VERDICT]: {parent_verdict}\n"
            f"[KEY PARENT ASSUMPTIONS]: {parent_assumptions}\n\n"
            f"[PARENT INQUIRY]: {parent_inquiry.core_question}\n\n"
            f"[OBJECTIVE]: Evolve the reasoning on this specific branch to find higher-fidelity results "
            f"and increase total confidence levels beyond the current {parent_inquiry.confidence_evolution[-1] if parent_inquiry.confidence_evolution else '25'}%."
            f" Focus specifically on avoiding drift while exploring the {divergence_title} trajectory."
        )

        child = Inquiry.objects.create(
            parent_inquiry=parent_inquiry,
            topic=parent_inquiry.topic,
            user=parent_inquiry.user,
            case_id=f"{parent_inquiry.case_id}_branch_{uuid.uuid4().hex[:4]}",
            branch_name=divergence_title,
            core_question=compound_question,
            current_question_state=compound_question,
            history_log=[{
                "timestamp": str(parent_inquiry.updated_at),
                "event": "Branch Spawned",
                "trajectory": divergence_title,
                "parent_id": str(parent_inquiry.id),
                "objective": "Better Results / Increased Confidence",
                "coupling_status": "LOCKED_TO_PARENT"
            }]
        )

        # 2. Re-initialize planets for the child (clean slate for the branch)
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
        
        for name, icon, order in steps:
            Planet.objects.create(
                inquiry=child,
                name=name,
                icon_class=icon,
                order=order,
                status='NOT_STARTED'
            )
            
        return child

    @staticmethod
    def call_serverless_engine(payload):
        """
        Calls the decoupled ELIF engine via HTTP.
        """
        import requests
        url = getattr(settings, 'ELIF_ENGINE_URL', None)
        if not url:
            raise ValueError("ELIF_ENGINE_URL is not configured in settings.py")
            
        response = requests.post(url, json=payload, timeout=120)
        
        if response.status_code != 200:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {"error": response.text}
            raise Exception(f"Engine Serverless Error ({response.status_code}): {error_data.get('error', 'Unknown error')}")
            
        return response.json()

    @staticmethod
    def initialize_orchestration(inquiry_obj):
        """Initializes the runner and context for a step-by-step procedure execution."""
        from discovery.models import SystemSettings
        import os
        
        sys_settings = SystemSettings.get_settings()
        
        # Inject API keys into environment for the engine
        if sys_settings.anthropic_api_key:
            os.environ["ELIF_ANTHROPIC_API_KEY"] = sys_settings.anthropic_api_key
        if sys_settings.deepseek_api_key:
            os.environ["ELIF_DEEPSEEK_API_KEY"] = sys_settings.deepseek_api_key

        runner = ProcedureRunner()
        
        # Build initial frame
        detected = EngineService._detect_language(inquiry_obj.core_question)
        language_hint = ""
        if detected != "English":
            language_hint = f"CRITICAL: The operator is using {detected}. Respond ONLY in {detected}. ALL reasoning segments, descriptions, and labels MUST be in {detected}. Do not use English."

        input_frame = InputFrame(
            id=str(inquiry_obj.id),
            text=inquiry_obj.core_question,
            locked_at_iso=inquiry_obj.created_at.isoformat() if inquiry_obj.created_at else "2026-05-28T00:00:00Z",
            doctrinal_scope_tag="GENERAL",
            companion_case=inquiry_obj.case_id,
            language_instruction=language_hint
        )

        # 1. Prepare context and internal engine components
        results_dir = Path(settings.MEDIA_ROOT) / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        run_context, components = runner.get_context_and_components(
            case_id=inquiry_obj.case_id,
            condition='c', # Production default
            input_frame=input_frame,
            offline_mode=sys_settings.offline_mode,
            max_llm_calls=getattr(settings, 'MAX_LLM_CALLS', 15),
            model_id=sys_settings.active_model,
            results_dir=results_dir,
            language_instruction=language_hint
        )

        return runner, run_context, components, input_frame

    @staticmethod
    def get_serverless_payload(inquiry_obj, step_id, prior_outputs):
        """
        Generates a JSON-serializable payload to invoke a serverless engine function.
        """
        runner, run_context, components, input_frame = EngineService.initialize_orchestration(inquiry_obj)
        
        return {
            "step_id": step_id,
            "case_id": inquiry_obj.case_id,
            "condition": "c",
            "input_frame": {
                "id": input_frame.id,
                "text": input_frame.text,
                "locked_at_iso": input_frame.locked_at_iso,
                "doctrinal_scope_tag": input_frame.doctrinal_scope_tag,
                "companion_case": input_frame.companion_case,
                "language_instruction": input_frame.language_instruction
            },
            "prior_outputs": prior_outputs,
            "run_context_data": {
                "procedure_version": run_context.procedure_version,
                "max_llm_calls": run_context.max_llm_calls,
                "started_at_iso": run_context.started_at_iso,
                "run_id": run_context.run_id,
                "language_instruction": run_context.language_instruction
            },
            "model_id": run_context.model_id,
            "offline_mode": run_context.offline_mode
        }

    @staticmethod
    def run_full_procedure(inquiry_obj, request=None):
        """Triggers the distributed Celery workflow for the procedure."""
        from discovery.workflow_tasks import start_engine_workflow
        
        # Track the active job if request is provided
        if request:
            request.session['active_engine_pk'] = str(inquiry_obj.id)
            request.session.modified = True
            
        # Trigger async workflow start (returns < 1s)
        if getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False):
            # This service might be called from outside a request, so we need a logic to handle that
            # but usually it's used in views.
            from discovery.utils import run_threaded_task
            run_threaded_task(start_engine_workflow.delay, str(inquiry_obj.id))
        else:
            start_engine_workflow.delay(str(inquiry_obj.id))
        return True

    @staticmethod
    def refine_question(inquiry_obj, directive):
        """
        Synthesizes a new question based on the user's directive and current state.
        Updates the Inquiry object but DOES NOT trigger the run.
        """
        from elif_v0_1.llm_adapter import complete_structured
        sys_settings = SystemSettings.get_settings()
        
        # 1. Build context for the LLM
        summary = {
            "original_question": inquiry_obj.core_question,
            "current_findings": {
                "assumptions": inquiry_obj.assumptions[:5],
                "active_hypotheses": [h.get("description") for h in inquiry_obj.hypothesis_set.get("hypotheses", [])[:3]],
                "unresolved_uncertainty": inquiry_obj.unresolved_zones[:3]
            },
            "user_refinement_directive": directive
        }

        prompt = f"""
        You are the ELIF Synthesis Agent. Your task is to evolve a core inquiry question based on current reasoning results and a user directive.
        
        CURRENT STATE:
        {summary}
        
        GOAL:
        - Integrate the user's directive into a new, more precise, or expanded core question.
        - Ensure the new question remains compatible with ELIF doctrinal standards (separation, preserve over chase, anti-drift).
        
        Emit the new question clearly.
        """
        
        schema = {
            "type": "object",
            "properties": {
                "new_question": {"type": "string"},
                "rationale": {"type": "string"}
            },
            "required": ["new_question", "rationale"]
        }

        import os
        if sys_settings.anthropic_api_key:
            os.environ["ELIF_ANTHROPIC_API_KEY"] = sys_settings.anthropic_api_key

        result = complete_structured(
            prompt=prompt,
            output_schema=schema,
            offline_mode=sys_settings.offline_mode,
            max_calls=5
        )

        # Record spend for refinement
        from discovery.models import SpendRecord
        usage = getattr(complete_structured, 'last_usage', {})
        # Note: We record even if tokens are zero (offline) to ensure the ledger remains a complete interaction log.
        record = SpendRecord.objects.create(
            inquiry=inquiry_obj,
            step_name=f"Refinement: {directive[:50]}...",
            model_id=usage.get("model_id", sys_settings.active_model or "claude-3-5-sonnet-20240620"),
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0)
        )
        record.calculate_cost()
        record.save()

        new_q = result.get("new_question")
        
        # 2. Update Inquiry History
        inquiry_obj.history_log.append({
            "timestamp": str(inquiry_obj.updated_at),
            "event": "Question Refinement",
            "previous_question": inquiry_obj.core_question,
            "directive": directive,
            "new_question": new_q,
            "rationale": result.get("rationale")
        })
        
        inquiry_obj.core_question = new_q
        inquiry_obj.current_question_state = new_q
        inquiry_obj.save()
        return new_q

    @staticmethod
    def evolve_inquiry(inquiry_obj, directive):
        """
        Takes an existing Inquiry model and a directive.
        Simulates a targeted engine call or branch update.
        """
        pass
