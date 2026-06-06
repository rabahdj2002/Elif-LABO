from django.db import models

class SystemSettings(models.Model):
    """
    Control layer for the ELIF Engine and UX parameters.
    """
    engine_model_choices = [
        ('sonnet', 'Claude 3.5 Sonnet (Canonical)'),
    ]

    # Engine Config
    active_model = models.CharField(max_length=50, choices=engine_model_choices, default='sonnet')
    anthropic_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="API Key for Claude models")
    # Gemini and OpenAI removed per operator directive 2026-06-03
    offline_mode = models.BooleanField(default=False, help_text="Simulate reasoning without API calls")
    reasoning_depth = models.IntegerField(default=7, help_text="Depth of Step 6 propagation")
    enable_web_search = models.BooleanField(default=True)
    strict_governance = models.BooleanField(default=True, help_text="Bypass Step 10 if Step 9 fails")
    
    # UX Config
    linear_ui_mode = models.BooleanField(default=True)
    show_spending_overview = models.BooleanField(default=True, help_text="Show or hide USD accumulation metrics for users.")
    auto_refresh_ms = models.IntegerField(default=5000)
    debug_mode = models.BooleanField(default=False, help_text="Expose engine telemetry during execution")
    system_version = models.CharField(max_length=20, default="V1.0 ALPHA", help_text="Version string displayed in sidebar")

    # Documentation
    documentation_content = models.TextField(
        default="# ELIF Protocol Documentation\n\nWelcome to the official ELIF documentation. This guide details the cognitive engine architecture, hypothesis validation layers, and operative truth separates protocols.",
        help_text="Markdown content for the Documentation page."
    )

    # Tester Protocol
    tester_free_inquiry_limit = models.IntegerField(default=10, help_text="Inquiries available for Testers before survey/cutoff.")
    tester_free_spend_limit = models.DecimalField(max_digits=10, decimal_places=2, default=50.00, help_text="USD spend available for Testers before cutoff.")
    tester_survey_schema = models.JSONField(default=list, help_text="List of questions for the tester survey.")
    
    # Commercial Config
    default_tier = models.ForeignKey('Tier', on_delete=models.SET_NULL, null=True, blank=True, help_text="Automatically assigned to new users.")
    
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    def __str__(self):
        return "Global System Settings"
