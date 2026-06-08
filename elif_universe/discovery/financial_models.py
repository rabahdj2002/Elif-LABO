from django.db import models
from django.contrib.auth.models import User
import uuid

class DailyFinancialSnapshot(models.Model):
    """
    Aggregated daily metrics for performance-optimized dashboard rendering.
    """
    date = models.DateField(unique=True)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    total_ai_cost = models.DecimalField(max_digits=12, decimal_places=6, default=0.0)
    total_infra_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    active_subscribers = models.IntegerField(default=0)
    new_subscriptions = models.IntegerField(default=0)
    churned_subscriptions = models.IntegerField(default=0)
    failed_payments = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

class FinancialTransaction(models.Model):
    """
    Granular record of every revenue-generating event.
    """
    TRANSACTION_TYPES = [
        ('SUBSCRIPTION', 'Subscription Payment'),
        ('RENEWAL', 'Renewal'),
        ('UPGRADE', 'Upgrade'),
        ('REFUND', 'Refund'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='financial_transactions')
    stripe_event_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    stripe_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tier = models.ForeignKey('discovery.Tier', on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class PlatformCost(models.Model):
    """
    Non-AI infrastructure costs (Hosting, DB, etc.) logged periodically.
    """
    COST_CATEGORIES = [
        ('HOSTING', 'Vercel / GCP Cloud Run'),
        ('DATABASE', 'Aiven PostgreSQL'),
        ('STORAGE', 'Cloud Storage'),
        ('SEARCH', 'Search API'),
        ('MISC', 'Miscellaneous'),
    ]
    
    category = models.CharField(max_length=20, choices=COST_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date_applied = models.DateField()
    
    def __str__(self):
        return f"{self.category}: ${self.amount} on {self.date_applied}"

class BusinessAlert(models.Model):
    """
    Automated system alerts based on financial thresholds.
    """
    SEVERITY_CHOICES = [
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('CRITICAL', 'Critical'),
    ]
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='INFO')
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
