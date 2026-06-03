from django.db import models

class SystemSettings(models.Model):
    """
    Control layer for the ELIF Engine and UX parameters.
    """
    engine_model_choices = [
        ('gpt-4o', 'GPT-4o (High Accuracy)'),
        ('claude-sonnet-4-6', 'Claude Sonnet (High Reasoning)'),
        ('gpt-4-turbo', 'GPT-4 Turbo'),
    ]

    # Engine Config
    active_model = models.CharField(max_length=50, choices=engine_model_choices, default='claude-sonnet-4-6')
    anthropic_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="API Key for Claude models")
    openai_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="API Key for GPT models")
    offline_mode = models.BooleanField(default=False, help_text="Simulate reasoning without API calls")
    reasoning_depth = models.IntegerField(default=7, help_text="Depth of Step 6 propagation")
    enable_web_search = models.BooleanField(default=True)
    strict_governance = models.BooleanField(default=True, help_text="Bypass Step 10 if Step 9 fails")
    
    # UX Config
    linear_ui_mode = models.BooleanField(default=True)
    auto_refresh_ms = models.IntegerField(default=5000)
    
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    def __str__(self):
        return "Global System Settings"
