from django.db import models

class SystemSettings(models.Model):
    """
    Control layer for the ELIF Engine and UX parameters.
    """
    engine_model_choices = [
        ('deepseek-chat', 'DeepSeek Chat (Standard)'),
        ('deepseek-reasoner', 'DeepSeek Reasoner (R1)'),
        ('sonnet', 'Claude 4.5 Sonnet (Canonical)'),
    ]

    # Engine Config
    active_model = models.CharField(max_length=50, choices=engine_model_choices, default='deepseek-chat')
    anthropic_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="API Key for Claude models")
    deepseek_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="API Key for DeepSeek models")
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

    # Integrations (API Keys)
    stripe_public_key = models.CharField(max_length=255, blank=True, null=True)
    stripe_secret_key = models.CharField(max_length=255, blank=True, null=True)
    stripe_webhook_secret = models.CharField(max_length=255, blank=True, null=True)
    stripe_live_mode = models.BooleanField(default=False, help_text="If True, uses Stripe Production. If False, uses Test Mode.")
    
    # SMTP Substrate (Communication Layer)
    smtp_host = models.CharField(max_length=255, blank=True, null=True)
    smtp_port = models.IntegerField(default=587)
    smtp_user = models.CharField(max_length=255, blank=True, null=True)
    smtp_password = models.TextField(blank=True, null=True, help_text="Encrypted SMTP Password")
    smtp_use_tls = models.BooleanField(default=True)
    smtp_use_ssl = models.BooleanField(default=False)
    email_from_address = models.EmailField(default='noreply@elif.ai')
    email_from_name = models.CharField(max_length=255, default='ELIF Engine')
    admin_alert_email = models.EmailField(blank=True, null=True, help_text="Where to send high-priority system alerts.")
    
    # Database Migration Settings (PostgreSQL)
    db_pg_host = models.CharField(max_length=255, blank=True, null=True)
    db_pg_port = models.CharField(max_length=10, blank=True, null=True)
    db_pg_name = models.CharField(max_length=255, blank=True, null=True, help_text="Database Name")
    db_pg_user = models.CharField(max_length=255, blank=True, null=True)
    db_pg_password = models.CharField(max_length=255, blank=True, null=True)
    db_pg_ssl_mode = models.CharField(
        max_length=20, 
        default="prefer", 
        choices=[('disable','disable'), ('allow','allow'), ('prefer','prefer'), ('require','require'), ('verify-ca','verify-ca'), ('verify-full','verify-full')]
    )
    use_postgres = models.BooleanField(default=True, help_text="Enable Postgres backend (requires server configuration)")
    
    # Database Health Metadata
    db_last_status = models.CharField(max_length=50, default="Unknown")
    db_last_check = models.DateTimeField(null=True, blank=True)
    db_version = models.CharField(max_length=512, blank=True, null=True)
    db_error_log = models.TextField(blank=True, null=True)

    # Documentation
    documentation_content = models.TextField(
        default="# ELIF Protocol Documentation\n\nWelcome to the official ELIF documentation. This guide details the cognitive engine architecture, hypothesis validation layers, and operative truth separates protocols.",
        help_text="Markdown content for the Documentation page."
    )

    # Commercial Config
    default_tier = models.ForeignKey('Tier', on_delete=models.SET_NULL, null=True, blank=True, help_text="Automatically assigned to new users.")
    yearly_discount_percent = models.IntegerField(default=40, help_text="Discount percentage shown for yearly plans (e.g. 40)")
    
    # Landing Page Statistics
    stat_avg_rating = models.CharField(max_length=20, default="4.9/5", help_text="Average Rating displayed on landing")
    stat_active_users = models.CharField(max_length=20, default="50K+", help_text="Active Users count displayed on landing")
    stat_automations_run = models.CharField(max_length=20, default="200M+", help_text="Automations Run count displayed on landing")
    stat_uptime = models.CharField(max_length=20, default="99.9%", help_text="Uptime percentage displayed on landing")

    # Branding
    favicon_url = models.URLField(max_length=1024, blank=True, null=True, help_text="External URL for favicon")
    logo_url = models.URLField(max_length=1024, blank=True, null=True, help_text="External URL for sidebar/landing logo")

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def smtp_pass(self):
        """Decrypts the SMTP password on the fly using Fernet and Django Secret Key."""
        if not self.smtp_password:
            return ""
        from cryptography.fernet import Fernet
        import base64
        from django.conf import settings
        
        # Derive a 32-byte key from Django's SECRET_KEY
        # Fernet requires exactly 32 bytes (base64 encoded)
        key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].encode().ljust(32, b'0'))
        f = Fernet(key)
        try:
            return f.decrypt(self.smtp_password.encode()).decode()
        except Exception:
            return ""

    @smtp_pass.setter
    def smtp_pass(self, value):
        """Encrypts the SMTP password using Fernet before storage."""
        if not value:
            self.smtp_password = None
            return
        from cryptography.fernet import Fernet
        import base64
        from django.conf import settings
        
        key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].encode().ljust(32, b'0'))
        f = Fernet(key)
        self.smtp_password = f.encrypt(value.encode()).decode()

    def save(self, *args, **kwargs):
        # Enforce single-row singleton pattern
        self.id = 1
        super().save(*args, **kwargs)
        
        # Mirror change to local config file to survive DB migrations/resets
        try:
            from .db_service import DatabaseService
            DatabaseService.persist_runtime_config(self)
        except Exception:
            # Avoid circular imports or other failures blocking DB saves
            pass

    def delete(self, *args, **kwargs):
        # Prevent deletion of global system settings
        pass

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(id=1)
        
        # Check if we need to bootstrap from local config
        # This is critical when switching between DB types (SQLite <-> Postgres)
        # where the database table might be new or empty.
        has_empty_db_fields = not obj.db_pg_host or not obj.db_pg_name
        
        if created or has_empty_db_fields:
            from .db_service import DatabaseService
            config = DatabaseService.load_runtime_config()
            if config:
                # Only update if the current field is empty or if we just created the object
                if created or not obj.anthropic_api_key:
                    obj.anthropic_api_key = config.get('anthropic_api_key', obj.anthropic_api_key)
                if created or not obj.deepseek_api_key:
                    obj.deepseek_api_key = config.get('deepseek_api_key', obj.deepseek_api_key)
                
                # Bootstrap database fields from mirror
                obj.db_pg_host = config.get('db_pg_host', obj.db_pg_host)
                obj.db_pg_port = config.get('db_pg_port', obj.db_pg_port)
                obj.db_pg_name = config.get('db_pg_name', obj.db_pg_name)
                obj.db_pg_user = config.get('db_pg_user', obj.db_pg_user)
                obj.db_pg_password = config.get('db_pg_password', obj.db_pg_password)
                obj.db_pg_ssl_mode = config.get('db_pg_ssl_mode', obj.db_pg_ssl_mode)
                obj.use_postgres = config.get('use_postgres', obj.use_postgres)
                
                obj.save()
        return obj

    def __str__(self):
        return "Global System Settings"
