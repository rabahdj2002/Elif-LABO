import sys
from pathlib import Path
from django.conf import settings

# Ensure engine is in path
if str(settings.ENGINE_SRC) not in sys.path:
    sys.path.append(str(settings.ENGINE_SRC))

from elif_v0_1.orchestration_runner import ProcedureRunner
from elif_v0_1.base import InputFrame
from discovery.models import SystemSettings

class EngineService:
    @staticmethod
    def run_full_procedure(inquiry_obj):
        """Runs the standard 11-step procedure and updates the Inquiry/Planets."""
        settings = SystemSettings.get_settings()
        
        # Inject API keys into environment for the engine
        import os
        if settings.anthropic_api_key:
            os.environ["ELIF_ANTHROPIC_API_KEY"] = settings.anthropic_api_key
        if settings.openai_api_key:
            os.environ["OPENAI_API_KEY"] = settings.openai_api_key

        runner = ProcedureRunner()
        
        # Build initial frame
        input_frame = InputFrame(
            id=str(inquiry_obj.id),
            text=inquiry_obj.core_question,
            locked_at_iso=inquiry_obj.created_at.isoformat() if inquiry_obj.created_at else "2026-05-28T00:00:00Z",
            doctrinal_scope_tag="GENERAL",
            companion_case=inquiry_obj.case_id
        )
        
        # Execute (This is a blocking call, typically would be async)
        try:
            report = runner.run(
                case_id=inquiry_obj.case_id,
                condition='c', 
                input_frame=input_frame,
                offline_mode=settings.offline_mode,
                model_id=settings.active_model
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

            # FINALLY: Update all 8 Room Projections from the newly saved planets
            from discovery.models import RoomState
            for r_type, _ in RoomState.ROOM_CHOICES:
                room, _ = RoomState.objects.get_or_create(inquiry=inquiry_obj, room_type=r_type)
                room.sync_from_planets()
                room.save()

            inquiry_obj.state_data = {"run_id": report.run_context.run_id, "status": "COMPLETED"}
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
