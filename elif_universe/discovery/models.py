from django.db import models
from django.contrib.auth.models import User
import uuid
import re

from .settings_models import SystemSettings
from .financial_models import DailyFinancialSnapshot, FinancialTransaction, PlatformCost, BusinessAlert

class Inquiry(models.Model):
    """
    LAYER 2: PERSISTENT INQUIRY OBJECT
    The core architectural substrate of ELIF. This is not a 'report' but a living,
    corrigible record of reasoning. It manages the evolution of clinical understanding
    while maintaining non-sovereign boundaries.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case_id = models.CharField(max_length=100, default=uuid.uuid4)
    topic = models.CharField(max_length=255, default="General", help_text="The thematic folder/category for this inquiry.")
    core_question = models.TextField(help_text="The original input frame.")
    current_question_state = models.TextField(blank=True, help_text="The evolved inquiry state.")
    
    # Structured State (Corrigibility Substrate)
    parent_inquiry = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    branch_name = models.CharField(max_length=255, blank=True, help_text="The name of the trajectory this branch represents.")
    divergences = models.JSONField(default=list, help_text="First-class inquiry forks / competing futures.")
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries', null=True, blank=True)
    assumptions = models.JSONField(default=list, help_text="Load-bearing assumptions surfaced by Step 3.")
    evidence_map = models.JSONField(default=dict)
    hypothesis_set = models.JSONField(default=dict, help_text="Active and falsified possibilities.")
    solution_families = models.JSONField(default=list, help_text="Competing solution architectures (Pluralism).")
    unresolved_zones = models.JSONField(default=list, help_text="Residual Darkness / Regulatory uncertainty (The One).")
    constraints = models.JSONField(default=list)
    history_log = models.JSONField(default=list, help_text="Traceable audit of all cognitive mutations.")
    investigation_status = models.CharField(max_length=50, default="Emerging", help_text="The qualitative status of the inquiry (e.g., Emerging, Validated).")
    confidence_evolution = models.JSONField(default=list)
    stability_evolution = models.JSONField(default=list)
    current_status_msg = models.CharField(max_length=255, default="Initializing Engine...", blank=True)
    is_visible_to_user = models.BooleanField(default=True, help_text="Set to False when a user 'deletes' the inquiry to persist it for admin audit.")
    status = models.CharField(max_length=20, default="PENDING", choices=[
        ("PENDING", "Pending"),
        ("RUNNING", "Running"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("REFUSED", "Refused"),
        ("DELETED", "Deleted"),
    ])
    final_verdict = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True, help_text="User's expertise specialization for this inquiry.")
    
    # Legacy compatibility fields (deprecated in UI)
    current_frame = models.JSONField(default=dict)
    state_data = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        # If this is a new inquiry and has a user, increment their usage metrics
        if is_new and self.user and hasattr(self.user, 'subscription'):
            sub = self.user.subscription
            sub.total_inquiries_consumed += 1
            sub.monthly_inquiries_consumed += 1
            sub.save(update_fields=['total_inquiries_consumed', 'monthly_inquiries_consumed'])

    @property
    def current_confidence(self):
        """Latest entry in confidence_evolution or default 25."""
        if self.confidence_evolution:
            return self.confidence_evolution[-1]
        return 25

    @property
    def total_spend(self):
        """Aggregate USD cost from all associated SpendRecords."""
        return sum(f.cost_usd for f in self.spend_records.all())

    @property
    def refusal_reason(self):
        """Extract reasoning from Step 1 or Step 9 if the inquiry was refused."""
        if self.status == 'REFUSED':
            # Check Step 1 (Frame)
            step1 = self.planets.filter(order=1).first()
            if step1 and step1.data and step1.data.get('verdict') == 'invalid':
                return step1.data.get('reasoning') or "Article II: Frame failed structural scrutiny."
            
            # Check Step 9 (Governance)
            step9 = self.planets.filter(order=9).first()
            if step9 and step9.data and step9.data.get('verdict') == 'refuse':
                return step9.data.get('verdict_detail') or "Article V: Governance refused to authorize the roadmap."
        return None

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
        ('FAILED', 'Failed'),
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

            # Ensure we don't show "None" for reformulation if the engine returns null or "none"
            reformulation = None
            if step1:
                reformulation = step1.data.get("reformulated_frame")
                if isinstance(reformulation, str) and reformulation.lower().strip() in ["none", ""]:
                    reformulation = None
            
            self.room_data = {
                "verdict": step1.data.get("verdict", "PENDING") if step1 else "PENDING",
                "reformulation": reformulation if reformulation else self.inquiry.core_question,
                "objects": families
            }
            
        elif self.room_type == 'EVIDENCE':
            # Map Step 3 (Assumptions) + Step 4 (Hypotheses)
            step3 = find_planet("Step 3")
            step4 = find_planet("Step 4")
            step5 = find_planet("Step 5")
            
            # Map contradictions from failure conditions or unresolved zones
            contradictions = []
            if step5:
                for fc in step5.data.get("failure_conditions", []):
                    if fc.get("is_contradiction"):
                        contradictions.append(fc.get("fails_if", "Unknown conflict"))
            
            if not contradictions:
                contradictions = self.inquiry.unresolved_zones

            self.room_data = {
                "assumptions": step3.data.get("assumptions", []) if step3 else self.inquiry.assumptions,
                "hypotheses": step4.data.get("hypotheses", []) if step4 else [],
                "contradictions": contradictions
            }
            
        elif self.room_type == 'EXPLORATION':
            # Map Step 6 (Scales) + Step 7 (Outside-Original-Frame Trajectories)
            step4 = find_planet("Step 4")
            step6 = find_planet("Step 6")
            step7 = find_planet("Step 7")
            
            # Normalize trajectories to ensure consistent keys
            raw_trajectories = step7.data.get("trajectories", []) if step7 else []
            normalized_trajs = []
            for t in raw_trajectories:
                if isinstance(t, dict):
                    t_norm = t.copy()
                    t_norm['description'] = t.get('reason') or t.get('description') or t.get('impact_if_true') or "No details."
                    normalized_trajs.append(t_norm)
                else:
                    normalized_trajs.append({"reason": str(t), "description": str(t), "tag": "unknown"})

            self.room_data = {
                "hypotheses": step4.data.get("hypotheses", []) if step4 else [],
                "scales": step6.data.get("scales", []) if step6 else [],
                "relations": step6.data.get("cross_scale_relations", []) if step6 else [],
                "trajectories": normalized_trajs
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
                "summary": step6.data.get("synthesis", "Multi-scale propagation complete.") if step6 else "Awaiting Step 6 Scenario Synthesis."
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
            step9 = find_planet("Step 9")
            step11 = find_planet("Step 11")
            
            biases = []
            if step5:
                for fc in step5.data.get("failure_conditions", []):
                    biases.append({
                        "name": f"Hypothesis {fc.get('hypothesis_id', 'Unknown')}",
                        "impact": fc.get("fails_if", "Unknown failure condition")
                    })

            # UNRESOLVED SEMANTIC ZONES:
            # Step 11 data is structured with 'kind' and 'description'.
            # If Step 11 exists, we use its entries.
            # If not, we fall back to self.inquiry.unresolved_zones (which now holds Step 9 data).
            ambiguities = []
            if step11 and step11.data.get("entries"):
                ambiguities = step11.data.get("entries")
            elif self.inquiry.unresolved_zones:
                # Map simple strings from Step 9 to the ambiguity dict format
                for zone in self.inquiry.unresolved_zones:
                    if isinstance(zone, dict):
                        ambiguities.append(zone)
                    else:
                        ambiguities.append({"kind": "unresolved_uncertainty", "description": str(zone)})

            self.room_data = {
                "biases": biases,
                "ambiguities": ambiguities,
                "gap_density": 45 
            }

        elif self.room_type == 'DECISION':
            # Map Step 10 (Operative vs Theoretical) + Inquiry Divergences
            step10 = find_planet("Step 10")
            step7 = find_planet("Step 7")
            
            # Use persistent divergences if available, else pull from Step 7 live
            divergences = self.inquiry.divergences
            if not divergences and step7 and step7.data:
                divergences = step7.data.get("trajectories", [])

            # NORMALIZE: Ensure every divergence has a title, description, and confidence
            # This prevents template lookup errors
            normalized_divergences = []
            for d in (divergences or []):
                norm = d.copy() if isinstance(d, dict) else {"reason": str(d)}
                # Map various engine outputs to consistent keys
                norm['title'] = norm.get('title') or norm.get('tag') or "Alternative Trajectory"
                norm['description'] = norm.get('reason') or norm.get('impact_if_true') or norm.get('description') or "No details available."
                norm['confidence_impact'] = norm.get('confidence_impact') or "Step 7 Evolution"
                normalized_divergences.append(norm)
                
            self.room_data = {
                "decision": step10.data.get("operative", ["N/A"])[0] if step10 and step10.data.get("operative") else "DIVERGENCE UNRESOLVED",
                "summary": step10.data.get("absence_log", "") if step10 else "",
                "requirements": step10.data.get("operative", []) if step10 else [],
                "divergences": normalized_divergences
            }

        self.save()

class Tier(models.Model):
    """
    BUSINESS LAYER: SUBSCRIPTION TIERS
    Defines limits and pricing for different user levels.
    """
    name = models.CharField(max_length=100)
    inquiry_limit = models.IntegerField(default=5, help_text="Maximum number of inquiries allowed.")
    spend_limit = models.DecimalField(max_digits=10, decimal_places=2, default=50.00, help_text="Maximum USD spend allowed.")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Monthly price for this tier.")
    price_yearly = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Total yearly price for this tier.")
    is_contact_only = models.BooleanField(default=False, help_text="If True, price is hidden and replaced with 'Contact Us'.")
    is_recommended = models.BooleanField(default=False, help_text="Mark this tier as 'Recommended' on the landing page.")
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    """
    BUSINESS LAYER: USER QUOTAS
    Tracks individual user usage against their tier limits.
    """
    USER_TYPE_CHOICES = [
        ('NORMAL', 'Normal User'),
        ('ADMIN', 'Limited Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    tier = models.ForeignKey(Tier, on_delete=models.PROTECT, default=1)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='NORMAL')
    total_inquiries_consumed = models.IntegerField(default=0, help_text="Lifetime inquiries started, non-decrementing.")
    monthly_inquiries_consumed = models.IntegerField(default=0, help_text="Inquiries consumed in current billing cycle.")
    monthly_spend_consumed = models.DecimalField(max_digits=10, decimal_places=6, default=0.0, help_text="Spend consumed in current billing cycle.")
    billing_start_date = models.DateTimeField(auto_now_add=True)
    has_seen_walkthrough = models.BooleanField(default=False)
    research_specializations = models.JSONField(default=list, blank=True, help_text="User-defined areas of expertise.")
    
    # Email Verification
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    token_expires_at = models.DateTimeField(blank=True, null=True)
    
    # Custom permissions for 'Limited Admin' stored as JSON blob of allowed route names or categories
    admin_permissions = models.JSONField(default=dict, blank=True, help_text="Configured by Superuser for 'Limited Admin' type.")
    
    # Stripe Substrate
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_status = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. active, past_due, canceled")
    current_period_end = models.DateTimeField(blank=True, null=True)
    cancel_at_period_end = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old_tier = None
        if not is_new:
            try:
                old_instance = UserSubscription.objects.get(pk=self.pk)
                old_tier = old_instance.tier
            except UserSubscription.DoesNotExist:
                pass

        super().save(*args, **kwargs)
        
        # Tier change notification
        if old_tier and old_tier != self.tier:
            Notification.objects.create(
                user=self.user,
                title="Tier Evolution",
                message=f"Your cognitive capacity has been updated to [{self.tier.name}]. Higher processing limits now active.",
                category='TIER_CHANGE',
                link='/discovery/subscription/'
            )

    @property
    def inquiry_usage(self):
        """Current usage based on monthly consumption, resetting automatically."""
        # We perform a JIT reset check here
        self.check_cycle_reset()
        return self.monthly_inquiries_consumed

    def check_cycle_reset(self):
        """Checks if a month has passed and resets counters if so."""
        from django.utils import timezone
        from dateutil.relativedelta import relativedelta
        
        now = timezone.now()
        # Calculate how many months have passed since billing_start_date
        diff = relativedelta(now, self.billing_start_date)
        months_passed = diff.months + (diff.years * 12)
        
        if months_passed > 0:
            # Advance billing_start_date by the number of months passed
            self.billing_start_date = self.billing_start_date + relativedelta(months=months_passed)
            self.monthly_inquiries_consumed = 0
            self.monthly_spend_consumed = 0.0
            self.save()

            Notification.objects.create(
                user=self.user,
                title="Cycle Refresh",
                message="A new monthly operational cycle has started. Your inquiry capacity has been refreshed.",
                category='USAGE_RESET'
            )
            return True
        return False

    @property
    def next_reset_date(self):
        """Calculates the date when the next reset will occur."""
        from dateutil.relativedelta import relativedelta
        return self.billing_start_date + relativedelta(months=1)

    @property
    def spend_usage(self):
        """Current monthly spend, resetting automatically."""
        self.check_cycle_reset()
        return float(self.monthly_spend_consumed)

    @property
    def total_spend_usage(self):
        """Aggregate lifetime spend from all records for admin auditing."""
        return sum(record.cost_usd for record in self.user.spend_records.all())

    def __str__(self):
        return f"{self.user.username} - {self.tier.name} ({self.user_type})"

class Notification(models.Model):
    """
    REAL-TIME NOTIFICATION SYSTEM
    Tracks updates for users (tier changes, resets) and admins (mission reports).
    """
    CATEGORY_CHOICES = [
        ('MISSION_REJECTED', 'Refill Requested'),
        ('MISSION_COMPLETED', 'Mission Submitted'),
        ('TIER_CHANGE', 'Tier Update'),
        ('USAGE_RESET', 'Usage Reset'),
        ('SYSTEM', 'System Alert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='SYSTEM')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"

class EmailLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    template_name = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='pending')
    error_log = models.TextField(blank=True)
    context_data = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    message_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.recipient} | {self.subject} | {self.status}"

class SpendRecord(models.Model):
    """
    METRIC: REAL-TIME COST ACCUMULATION
    Tracks every LLM call's financial footprint.
    Prices (Canonical Sonnet 20241022):
    Input: $3.00 / MTok
    Output: $15.00 / MTok
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spend_records', null=True, blank=True)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.SET_NULL, null=True, blank=True, related_name='spend_records')
    case_id_snapshot = models.CharField(max_length=100, blank=True, help_text="Snapshot of case_id for persistence after inquiry deletion.")
    step_name = models.CharField(max_length=100, help_text="The ELIF reasoning step (e.g. Frame Validator)")
    model_id = models.CharField(max_length=100)
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    cost_usd = models.DecimalField(max_digits=10, decimal_places=6, default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if self.inquiry:
            if not self.user:
                self.user = self.inquiry.user
            if not self.case_id_snapshot:
                self.case_id_snapshot = self.inquiry.case_id
        
        # Calculate cost before saving if it hasn't been set
        if not self.cost_usd:
            self.calculate_cost()
            
        super().save(*args, **kwargs)
        
        # If this is a new spend record being created, increment the user's monthly budget
        if is_new and self.user and hasattr(self.user, 'subscription'):
            sub = self.user.subscription
            sub.monthly_spend_consumed = float(sub.monthly_spend_consumed) + float(self.cost_usd)
            sub.save(update_fields=['monthly_spend_consumed'])

    def calculate_cost(self):
        # Pricing Table (USD per 1M tokens)
        PRICES = {
            "claude-3-5-sonnet": {"in": 3.0, "out": 15.0}, "deepseek-reasoner": {"in": 0.55, "out": 2.19}, "deepseek-chat": {"in": 0.14, "out": 0.28},
            "claude-3-5-haiku": {"in": 0.25, "out": 1.25},
            "gpt-4o": {"in": 5.0, "out": 15.0},
            "default": {"in": 3.0, "out": 15.0}
        }
        
        rate_key = "default"
        for key in PRICES:
            if key in self.model_id.lower():
                rate_key = key
                break
        
        input_rate = PRICES[rate_key]["in"] / 1_000_000
        output_rate = PRICES[rate_key]["out"] / 1_000_000
        
        self.cost_usd = (self.input_tokens * input_rate) + (self.output_tokens * output_rate)
        return self.cost_usd

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {self.step_name} | ${self.cost_usd:.4f}"

class IssueReport(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('WORKING', 'Working On'),
        ('FIXED', 'Fixed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issues')
    description = models.TextField()
    screenshot = models.TextField(blank=True, help_text="Base64 encoded screenshot data")
    url = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Issue by {self.user.username} - {self.status}"

class StripeWebhookLog(models.Model):
    """
    AUDIT TRAIL: STRIPE WEBHOOKS
    Prevents duplicate processing and provides security logs.
    """
    event_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=255)
    payload = models.JSONField()
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} ({self.event_id})"

class SystemTestRun(models.Model):
    CATEGORY_CHOICES = [
        ('CORE', 'Core System'),
        ('ENGINE', 'Reasoning Engine'),
        ('AI', 'AI Provider'),
        ('DATABASE', 'Database Integrity'),
        ('PAYMENT', 'Payment System'),
        ('SECURITY', 'Security & Access'),
        ('INFRA', 'Infrastructure'),
        ('API', 'External APIs'),
        ('UX', 'Frontend & UX'),
        ('FINANCE', 'Financial Reliability'),
        ('CHAOS', 'Chaos Mode'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    test_type = models.CharField(max_length=50, default='STANDARD') # STANDARD, DEEP, STRESS, CHAOS
    status = models.CharField(max_length=20, default='PENDING')
    health_score = models.IntegerField(default=0)
    results = models.JSONField(default=dict)
    logs = models.TextField(blank=True)
    execution_time = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category} [{self.test_type}] - {self.status} ({self.health_score}%)"




