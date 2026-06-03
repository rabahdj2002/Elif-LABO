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

class EngineService:
    @staticmethod
    def generate_case_id(question, topic=None):
        """Generates a unique, topic-aware Case ID."""
        from discovery.models import Inquiry, SystemSettings
        from elif_v0_1.llm_adapter import complete_structured
        import os
        
        settings = SystemSettings.get_settings()
        
        if topic and topic.strip():
            # If user provided a topic, we just need a descriptive suffix via LLM
            prompt = f"""
            You are the ELIF Case Architect. A topic "{topic}" has already been assigned.
            Analyze the following question and generate a short, slug-like 'case_id' suffix.
            
            CASE_ID FORMAT: Just the descriptive suffix (e.g., "electroculture", "policy_drift").
            
            INPUT QUESTION: {question}
            """
            schema = {
                "type": "object",
                "properties": {
                    "suffix": {"type": "string"}
                },
                "required": ["suffix"]
            }
        else:
            # 1. Determine Topic and Case ID via LLM
            prompt = f"""
            You are the ELIF Case Architect. Analyze the following question and assign it to a high-level "topic" (category).
            Then generate a short, slug-like 'case_id' suffix.
            
            TOPIC RULES:
            - Must be a single word or short phrase (e.g., "Policy", "Technology", "Agriculture", "Governance").
            - If it fits an existing common topic, use it.
            
            CASE_ID FORMAT: Just the descriptive suffix (e.g., "electroculture", "policy_drift").
            
            INPUT QUESTION: {question}
            
            Return the topic name and the descriptive suffix.
            """
            
            schema = {
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "suffix": {"type": "string"}
                },
                "required": ["topic", "suffix"]
            }

        if settings.anthropic_api_key:
            os.environ["ELIF_ANTHROPIC_API_KEY"] = settings.anthropic_api_key

        try:
            res = complete_structured(prompt=prompt, output_schema=schema, offline_mode=settings.offline_mode)
            if not topic or not topic.strip():
                topic = res.get("topic", "General")
            suffix = res.get("suffix", uuid.uuid4().hex[:6])
        except Exception:
            if not topic or not topic.strip():
                topic = "General"
            suffix = uuid.uuid4().hex[:6]

        # 2. Assign or retrieve the Sequence Number for this topic
        # We look for the first occurrence of this topic to see what its sequence number was.
        # If it doesn't exist, we find the max sequence number across all topics and increment.
        
        existing_with_topic = Inquiry.objects.filter(topic__iexact=topic).first()
        
        if existing_with_topic:
            # Extract number from existing case_id: case_XX_...
            match = re.match(r"case_(\d+)_", existing_with_topic.case_id)
            if match:
                seq_num = match.group(1)
            else:
                seq_num = "99"
        else:
            # New topic, find next available sequence
            all_inquiries = Inquiry.objects.all()
            max_seq = 0
            for inq in all_inquiries:
                match = re.match(r"case_(\d+)_", inq.case_id)
                if match:
                    num = int(match.group(1))
                    if num > max_seq: max_seq = num
            seq_num = f"{max_seq + 1:02d}"

        final_case_id = f"case_{seq_num}_{suffix}"
        return final_case_id, topic

    @staticmethod
    def spawn_branch(parent_inquiry, divergence_title, trajectory_description):
        """Creates a new Inquiry as a branch of a parent divergence."""
        from discovery.models import Inquiry, Planet
        import uuid
        
        # 1. Create the child inquiry with a COMPOUND core question
        # We explicitly state the goal of finding better results and increasing confidence.
        compound_question = (
            f"DIVERGENCE BRANCH: {divergence_title}\n\n"
            f"[CONTEXT]: {trajectory_description}\n\n"
            f"[PARENT INQUIRY]: {parent_inquiry.core_question}\n\n"
            f"[OBJECTIVE]: Evolve the reasoning on this specific branch to find higher-fidelity results "
            f"and increase total confidence levels beyond the current {parent_inquiry.confidence_evolution[-1] if parent_inquiry.confidence_evolution else '25'}%."
        )

        child = Inquiry.objects.create(
            parent_inquiry=parent_inquiry,
            case_id=f"{parent_inquiry.case_id}_branch_{uuid.uuid4().hex[:4]}",
            branch_name=divergence_title,
            core_question=compound_question,
            current_question_state=compound_question,
            history_log=[{
                "timestamp": str(parent_inquiry.updated_at),
                "event": "Branch Spawned",
                "trajectory": divergence_title,
                "parent_id": str(parent_inquiry.id),
                "objective": "Better Results / Increased Confidence"
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
    def run_full_procedure(inquiry_obj):
        """Runs the standard 11-step procedure and updates the Inquiry/Planets."""
        settings = SystemSettings.get_settings()
        
        # Inject API keys into environment for the engine
        import os
        if settings.anthropic_api_key:
            os.environ["ELIF_ANTHROPIC_API_KEY"] = settings.anthropic_api_key

        # Governance Check: Validate Model Registry
        from elif_v0_1.model_registry import MODEL_REGISTRY
        if settings.active_model not in MODEL_REGISTRY and not settings.offline_mode:
             print(f"Warning: Model key '{settings.active_model}' not found in Registry. Proceeding with passthrough.")

        runner = ProcedureRunner()
        
        # Build initial frame
        input_frame = InputFrame(
            id=str(inquiry_obj.id),
            text=inquiry_obj.core_question,
            locked_at_iso=inquiry_obj.created_at.isoformat() if inquiry_obj.created_at else "2026-05-28T00:00:00Z",
            doctrinal_scope_tag="GENERAL",
            companion_case=inquiry_obj.case_id
        )

        def update_status(msg):
            inquiry_obj.current_status_msg = msg
            inquiry_obj.save(update_fields=['current_status_msg'])
        
        # Execute (This is a blocking call, typically would be async)
        try:
            report = runner.run(
                case_id=inquiry_obj.case_id,
                condition='c', 
                input_frame=input_frame,
                offline_mode=settings.offline_mode,
                model_id=settings.active_model,
                status_callback=update_status
            )
            
            # Map report steps to planets
            step_to_planet_map = {
                "step_1": "Step 1: Frame Validation",
                "step_2": "Step 2: Object Decomposition",
                "step_3": "Step 3: Normalization Layer",
                "step_4": "Step 4: Hypothesis Construction",
                "step_5": "Step 5: Falsification Design",
                "step_6": "Step 6: Multi-Scale Propagation",
                "step_7": "Step 7: Outside-Frame Generation",
                "step_8": "Step 8: Stage-Gated Roadmap",
                "step_9": "Step 9: Constraint Synthesis",
                "step_10": "Step 10: Verdict Engine",
                "step_11": "Step 11: Audit / Drift Layer",
            }
            
            inquiry_obj.current_status_msg = "Cognitive Run Initiated..."
            inquiry_obj.save(update_fields=['current_status_msg'])

            for step_env in report.step_outputs:
                step_id = step_env.step_id
                planet_name = step_to_planet_map.get(step_id)
                
                if planet_name:
                    planet = inquiry_obj.planets.filter(name=planet_name).first()
                    if planet:
                        # Capture the structured output if available, else content
                        data = step_env.structured_output_dict if step_env.structured_output_dict else {}
                        if not data and step_env.content:
                            data = {"content": str(step_env.content)}
                        
                        planet.data = data
                        planet.status = 'COMPLETED'
                        planet.save()

                        # --- SPEND TRACKING (Article II Financials) ---
                        from discovery.models import SpendRecord
                        usage = step_env.usage_metadata
                        if usage:
                            spend = SpendRecord(
                                inquiry=inquiry_obj,
                                step_name=planet_name,
                                model_id=usage.get("model_id", "unknown"),
                                input_tokens=usage.get("input_tokens", 0),
                                output_tokens=usage.get("output_tokens", 0)
                            )
                            spend.calculate_cost()
                            spend.save()

                        # Step 1: Sync Frame to Inquiry
                        if step_id == "step_1":
                            inquiry_obj.current_question_state = data.get("reformulated_frame", inquiry_obj.core_question)
                            inquiry_obj.save()

                        # Step 9: Sync Unresolved Zones & Governance Enforcement
                        if step_id == "step_9":
                            inquiry_obj.unresolved_zones = data.get("unresolved_uncertainty_sources", [])
                            inquiry_obj.save()
                            
                            # LEVEL 2 BLOCK: Enforce Governance Execution Halt
                            if data.get("verdict") == "REFUSE":
                                raise Exception("GOVERNANCE_BLOCK: Engine execution terminated per Article V.")

            # --- DIVERGENCE SYNTHESIS (Article IV Sovereignty) ---
            # Instead of a single "Next Step", we extract forks in reality.
            # We derive these from Step 2 (Decomposition), Step 4 (Hypotheses), and Step 7 (Outside-Frame).
            divergences = []
            
            # Map of step_id to data for fast lookup
            step_data_map = {s.step_id: (s.structured_output_dict if s.structured_output_dict else {}) for s in report.step_outputs}

            # 1. From Step 2: Families as primary trajectories (Decomposition Output as branches)
            s2_data = step_data_map.get("step_2", {})
            axes = s2_data.get("axes") or s2_data.get("Axes") or []
            for axis in axes:
                axis_name = axis.get("axis_name") or axis.get("name") or "Decomposition Axis"
                for fam in (axis.get("families") or axis.get("Families") or []):
                    divergences.append({
                        "title": f"Branch: {fam.get('family_id', 'Unknown')}",
                        "why_emerged": f"Decomposition: {axis_name}",
                        "assumption": axis.get("rationale", "Identified in foundational break-up."),
                        "impact_if_true": fam.get("description", "Expanding reasoning on this decomposition path."),
                        "confidence_impact": "High",
                        "source_step": 2,
                        "identifier": fam.get("family_id")
                    })

            # 2. From Step 4: Hypotheses
            s4_data = step_data_map.get("step_4", {})
            hyps = s4_data.get("hypotheses") or s4_data.get("Hypotheses") or []
            for hyp in hyps:
                divergences.append({
                    "title": f"Hypothesis: {hyp.get('hypothesis_id', 'New Path')}",
                    "why_emerged": "Identified as a core exploratory trajectory.",
                    "assumption": "Derived from the primary problem-object decomposition.",
                    "impact_if_true": hyp.get("statement", "Expanding reasoning on this hypothesis."),
                    "confidence_impact": "High (Primary)",
                    "source_step": 4
                })

            # 3. From Step 7: Outside-Original-Frame Trajectories (Reality Forks)
            s7_data = step_data_map.get("step_7", {})
            trajs = s7_data.get("trajectories") or s7_data.get("Trajectories") or []
            for traj in trajs:
                if isinstance(traj, dict):
                    divergences.append({
                        "title": f"Reality Fork: {traj.get('tag', 'New Trajectory')}",
                        "why_emerged": "Identified trajectory outside the initial frame of reference.",
                        "assumption": "The initial frame was too narrow to capture this emergent path.",
                        "impact_if_true": traj.get("reason", "No reason provided."),
                        "confidence_impact": "Medium (Exploratory)",
                        "source_step": 7
                    })

            inquiry_obj.divergences = divergences[:15] # Cap at 15 for cockpit richness
            inquiry_obj.save()
            print(f"DEBUG: Saved {len(inquiry_obj.divergences)} total divergences to inquiry {inquiry_obj.id}")

            # FINALLY: Update all 8 Room Projections from the newly saved planets
            from discovery.models import RoomState
            for r_type, _ in RoomState.ROOM_CHOICES:
                room, _ = RoomState.objects.get_or_create(inquiry=inquiry_obj, room_type=r_type)
                room.sync_from_planets()
                room.save()

            inquiry_obj.state_data = {"run_id": report.run_context.run_id, "status": "COMPLETED"}
            inquiry_obj.current_status_msg = "Propagation Complete."
            inquiry_obj.save()
            return report

        except Exception as e:
            print(f"Engine Failure: {e}")
            inquiry_obj.state_data = {"error": str(e)}
            inquiry_obj.save()
            raise e

    @staticmethod
    def refine_and_run(inquiry_obj, directive):
        """
        Synthesizes a new question based on the user's directive and current state,
        then triggers a full re-run representing a 'Branch' in the roadmap.
        """
        from elif_v0_1.llm_adapter import complete_structured
        settings = SystemSettings.get_settings()
        
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
        - If the user wants to 'dive deeper' into a finding, focus the question on that finding.
        
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

        # Call LLM
        # Ensure API key is set
        import os
        if settings.anthropic_api_key:
            os.environ["ELIF_ANTHROPIC_API_KEY"] = settings.anthropic_api_key

        result = complete_structured(
            prompt=prompt,
            output_schema=schema,
            offline_mode=settings.offline_mode,
            max_calls=5
        )

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
        
        # Update core question and reset planets for fresh run
        inquiry_obj.core_question = new_q
        inquiry_obj.current_question_state = new_q
        inquiry_obj.save()
        
        # Reset Layer 1
        inquiry_obj.planets.all().update(status="NOT_STARTED", data={})

        # 3. Trigger Full Run
        return EngineService.run_full_procedure(inquiry_obj)

    @staticmethod
    def evolve_inquiry(inquiry_obj, directive):
        """
        Takes an existing Inquiry model and a directive.
        Simulates a targeted engine call or branch update.
        """
        pass
