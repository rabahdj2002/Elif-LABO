from django.db import models
import uuid
import re

from .settings_models import SystemSettings

class Inquiry(models.Model):
    """
    LAYER 2: PERSISTENT INQUIRY OBJECT
    The core architectural substrate of ELIF. This is not a 'report' but a living,
    corrigible record of reasoning. It manages the evolution of clinical understanding
    while maintaining non-sovereign boundaries.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    core_question = models.TextField(help_text="The original input frame.")
    current_question_state = models.TextField(blank=True, help_text="The evolved inquiry state.")
    
    # Structured State (Corrigibility Substrate)
    assumptions = models.JSONField(default=list, help_text="Load-bearing assumptions surfaced by Step 3.")
    evidence_map = models.JSONField(default=dict)
    hypothesis_set = models.JSONField(default=dict, help_text="Active and falsified possibilities.")
    solution_families = models.JSONField(default=list, help_text="Competing solution architectures (Pluralism).")
    unresolved_zones = models.JSONField(default=list, help_text="Residual Darkness / Regulatory uncertainty (The One).")
    constraints = models.JSONField(default=list)
    history_log = models.JSONField(default=list, help_text="Traceable audit of all cognitive mutations.")
    confidence_evolution = models.JSONField(default=list)
    
    # Legacy compatibility fields (deprecated in UI)
    current_frame = models.JSONField(default=dict)
    state_data = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.case_id}: {self.core_question[:50]}..."

class Planet(models.Model):
    """
    LAYER 1: REASONING ENGINE ARTIFACTS
    These represent internal 'Step' executions. In V1, they are HIDDEN from UI.
    """
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ERROR', 'Error'),
    ]
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='planets')
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, default='fa-globe')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    order = models.IntegerField(default=0)
    data = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.name} ({self.inquiry.case_id})"

class ExplorationBranch(models.Model):
    """
    LAYER 2: DIVERGENCE TREE
    Tracks branching paths of reasoning.
    """
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='explorations')
    parent_planet = models.ForeignKey(Planet, on_delete=models.CASCADE, related_name='offshoots', null=True, blank=True)
    choice_made = models.CharField(max_length=255)
    branch_data = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Branch {self.choice_made} ({self.inquiry.case_id})"

class EngineRun(models.Model):
    """
    LAYER 1 Audit Trail: Every heartbeat of the engine pipeline.
    """
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='engine_runs')
    run_timestamp = models.DateTimeField(auto_now_add=True)
    trigger = models.CharField(max_length=255)
    result_snapshot = models.JSONField()

class RoomState(models.Model):
    """
    LAYER 3: ROOM PROJECTIONS
    Stores interaction history or localized state for specific Rooms.
    """
    ROOM_CHOICES = [
        ('DISCOVERY', 'Discovery Room'),
        ('EVIDENCE', 'Evidence Room'),
        ('EXPLORATION', 'Exploration Room'),
        ('SOLUTION', 'Solution Room'),
        ('PROJECTION', 'Projection Room'),
        ('GOVERNANCE', 'Governance Room'),
        ('UNCERTAINTY', 'Uncertainty Room'),
        ('DECISION', 'Decision Room'),
    ]
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='room_states')
    room_type = models.CharField(max_length=20, choices=ROOM_CHOICES)
    room_data = models.JSONField(default=dict)
    last_interaction = models.DateTimeField(auto_now=True)

    def sync_from_planets(self):
        """
        LAYER 3 PROJECTION: Update room data based on Layer 1/2 state.
        Ensures confidence and signals are high-fidelity, not arbitrary.
        """
        planets = self.inquiry.planets.all()
        
        def find_planet(search_str):
            # Normalize to Step N
            n_match = re.search(r'\d+', search_str)
            if n_match:
                s_id = n_match.group()
                p = planets.filter(models.Q(name__icontains=search_str) | models.Q(order=s_id)).first()
                if p: return p
            return planets.filter(name__icontains=search_str).first()

        if self.room_type == 'DISCOVERY':
            # Map Step 1 (Frame) + Step 2 (Object Decomposition)
            step1 = find_planet("Step 1")
            step2 = find_planet("Step 2")
            
            # Extract families from Step 2 axes
            families = []
            if step2 and "axes" in step2.data:
                for axis in step2.data["axes"]:
                    families.extend([{
                        "name": fam.get("family_id", "Unknown"),
                        "objects": [fam.get("description", "")]
                    } for fam in axis.get("families", [])])

            self.room_data = {
                "verdict": step1.data.get("verdict", "PENDING") if step1 else "PENDING",
                "reformulation": step1.data.get("reformulated_frame", self.inquiry.core_question) if step1 else self.inquiry.core_question,
                "objects": families
            }
            
        elif self.room_type == 'EVIDENCE':
            # Map Step 3 (Assumptions) + Step 4 (Hypotheses)
            step3 = find_planet("Step 3")
            step4 = find_planet("Step 4")
            
            self.room_data = {
                "assumptions": step3.data.get("assumptions", []) if step3 else [],
                "hypotheses": step4.data.get("hypotheses", []) if step4 else []
            }
            
        elif self.room_type == 'EXPLORATION':
            # Map Step 6 (Scales) + Step 7 (Outside-Original-Frame Trajectories)
            step4 = find_planet("Step 4")
            step6 = find_planet("Step 6")
            step7 = find_planet("Step 7")
            
            self.room_data = {
                "hypotheses": step4.data.get("hypotheses", []) if step4 else [],
                "scales": step6.data.get("scales", []) if step6 else [],
                "relations": step6.data.get("cross_scale_relations", []) if step6 else [],
                "trajectories": step7.data.get("trajectories", []) if step7 else []
            }
            
        elif self.room_type == 'SOLUTION':
            # Map Step 8 (Branching Roadmap)
            step8 = find_planet("Step 8")
            stages = []
            if step8 and "stages" in step8.data:
                for s in step8.data["stages"]:
                    # Ensure continuation_gates is always a list for the template
                    gate = s.get("continuation_gate", "")
                    stages.append({
                        "stage_id": s.get("stage_id"),
                        "title": s.get("title", f"Stage {s.get('stage_id')}"),
                        "description": s.get("description"),
                        "continuation_gates": [gate] if gate else []
                    })

            self.room_data = {
                "roadmap_stages": stages
            }
            
        elif self.room_type == 'PROJECTION':
            # Map cross-scale relations as hypothetical scenarios
            step6 = find_planet("Step 6")
            projections = []
            if step6:
                for rel in step6.data.get("cross_scale_relations", []):
                    projections.append({"description": rel})

            self.room_data = {
                "projections": projections,
                "summary": "Multi-scale propagation complete." if step6 else "Awaiting Step 6 Scenario Synthesis."
            }
            
        elif self.room_type == 'GOVERNANCE':
            # Map Step 9 (Governance Kernel)
            step9 = find_planet("Step 9")
            if step9:
                self.room_data = {
                    "verdict": step9.data.get("verdict", "TBD"),
                    "rationale": step9.data.get("verdict_detail", ""),
                    "confidence": step9.data.get("confidence", "0%"),
                    "audit_trail": step9.data.get("unresolved_uncertainty_sources", [])
                }
            else:
                self.room_data = {"verdict": "PENDING", "rationale": "Awaiting Step 9 adjudication."}

        elif self.room_type == 'UNCERTAINTY':
            # Map Step 5 (Failure Conditions) + Step 11 (Audit)
            step5 = find_planet("Step 5")
            step11 = find_planet("Step 11")
            
            biases = []
            if step5:
                for fc in step5.data.get("failure_conditions", []):
                    biases.append({
                        "name": f"Hypothesis {fc.get('hypothesis_id', 'Unknown')}",
                        "impact": fc.get("fails_if", "Unknown failure condition")
                    })

            self.room_data = {
                "biases": biases,
                "ambiguities": step11.data.get("entries", []) if step11 else [{"kind": "unresolved_zone", "description": zone} for zone in self.inquiry.unresolved_zones],
                "gap_density": 45 
            }

        elif self.room_type == 'DECISION':
            # Map Step 10 (Operative vs Theoretical)
            step10 = find_planet("Step 10")
            
            self.room_data = {
                "decision": step10.data.get("operative", ["N/A"])[0] if step10 and step10.data.get("operative") else "DIVERGENCE UNRESOLVED",
                "summary": step10.data.get("absence_log", "") if step10 else "",
                "requirements": step10.data.get("operative", []) if step10 else []
            }

        self.save()


