from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import Inquiry, SpendRecord, Tier, UserSubscription, FinancialTransaction, DailyFinancialSnapshot, PlatformCost
from decimal import Decimal

class FinancialAnalyticsService:
    @staticmethod
    def get_executive_summary():
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        start_of_current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_of_last_month = (start_of_current_month - timedelta(days=1)).replace(day=1)
        
        # 1. Total (Lifetime) metrics
        total_revenue = FinancialTransaction.objects.exclude(type='REFUND').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        active_subs = UserSubscription.objects.exclude(tier__price=0).count()
        total_ai_cost = SpendRecord.objects.aggregate(Sum('cost_usd'))['cost_usd__sum'] or 0.0
        
        # 2. MRR / ARPU logic
        mrr = UserSubscription.objects.exclude(tier__price=0).aggregate(Sum('tier__price'))['tier__price__sum'] or Decimal('0.00')
        paid_user_count = max(active_subs, 1)
        arpu = mrr / Decimal(paid_user_count)
        
        # 3. Monthly delta logic (Current vs Previous Month)
        current_month_rev = FinancialTransaction.objects.filter(
            timestamp__gte=start_of_current_month,
            timestamp__lt=now
        ).exclude(type='REFUND').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        
        last_month_rev = FinancialTransaction.objects.filter(
            timestamp__gte=start_of_last_month,
            timestamp__lt=start_of_current_month
        ).exclude(type='REFUND').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        
        revenue_delta_pct = 0
        if last_month_rev > 0:
            revenue_delta_pct = ((current_month_rev - last_month_rev) / last_month_rev) * 100

        # AI cost last 30 days
        monthly_ai_cost = SpendRecord.objects.filter(inquiry__created_at__gte=thirty_days_ago).aggregate(Sum('cost_usd'))['cost_usd__sum'] or 0.0
        
        # Infra monthly estimate
        monthly_infra = PlatformCost.objects.filter(date_applied__gte=thirty_days_ago.date()).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
        
        net_profit = float(total_revenue) - float(total_ai_cost) - float(monthly_infra)

        return {
            "total_revenue": total_revenue,
            "mrr": mrr,
            "arr": mrr * 12,
            "active_subscribers": active_subs,
            "total_ai_cost": total_ai_cost,
            "net_profit": net_profit,
            "arpu": arpu,
            "revenue_delta_pct": revenue_delta_pct,
            "current_month_rev": current_month_rev
        }

    @staticmethod
    def get_cost_analytics():
        """Aggregates AI costs across various dimensions."""
        model_costs = SpendRecord.objects.values('model_id').annotate(total=Sum('cost_usd')).order_by('-total')
        step_costs = SpendRecord.objects.values('step_name').annotate(total=Sum('cost_usd')).order_by('-total')
        
        most_expensive_inquiries = Inquiry.objects.all().annotate(
            cost=Sum('spend_records__cost_usd')
        ).order_by('-cost')[:10]
        
        return {
            "model_costs": model_costs,
            "step_costs": step_costs,
            "expensive_inquiries": most_expensive_inquiries
        }

    @staticmethod
    def generate_daily_snapshot():
        """Scheduled task to collapse daily metrics into single rows."""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        rev = FinancialTransaction.objects.filter(timestamp__date=yesterday).aggregate(Sum('amount'))['amount__sum'] or 0.0
        ai = SpendRecord.objects.filter(inquiry__created_at__date=yesterday).aggregate(Sum('cost_usd'))['cost_usd__sum'] or 0.0
        subs = UserSubscription.objects.exclude(tier__price=0).count()
        
        DailyFinancialSnapshot.objects.update_or_create(
            date=yesterday,
            defaults={
                'total_revenue': rev,
                'total_ai_cost': ai,
                'active_subscribers': subs
            }
        )
