import stripe
from django.conf import settings
from .settings_models import SystemSettings
from .models import Tier, UserSubscription, StripeWebhookLog
from django.urls import reverse
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def get_stripe_client():
    sys_settings = SystemSettings.get_settings()
    if not sys_settings.stripe_secret_key:
        return None
    stripe.api_key = sys_settings.stripe_secret_key
    return stripe

def create_checkout_session(user, tier_id, success_url, cancel_url):
    stripe_client = get_stripe_client()
    if not stripe_client:
        raise Exception("Stripe not configured.")

    tier = Tier.objects.get(id=tier_id)
    if not tier.stripe_price_id:
        raise Exception(f"Tier {tier.name} has no Stripe Price ID configured.")

    subscription = user.subscription
    
    checkout_session = stripe_client.checkout.Session.create(
        customer=subscription.stripe_customer_id if subscription.stripe_customer_id else None,
        customer_email=user.email if not subscription.stripe_customer_id else None,
        payment_method_types=['card'],
        line_items=[
            {
                'price': tier.stripe_price_id,
                'quantity': 1,
            },
        ],
        mode='subscription',
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
        metadata={
            'user_id': user.id,
            'tier_id': tier.id
        },
        subscription_data={
            'metadata': {
                'user_id': user.id,
                'tier_id': tier.id
            }
        }
    )
    return checkout_session

def handle_webhook_event(payload, sig_header):
    sys_settings = SystemSettings.get_settings()
    endpoint_secret = sys_settings.stripe_webhook_secret
    stripe_client = get_stripe_client()

    if not stripe_client:
        return False, "Stripe not configured"

    try:
        event = stripe_client.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return False, "Invalid payload"
    except stripe.error.SignatureVerificationError as e:
        return False, "Invalid signature"

    # Log event to prevent duplicates
    if StripeWebhookLog.objects.filter(event_id=event.id).exists():
        return True, "Event already processed"

    webhook_log = StripeWebhookLog.objects.create(
        event_id=event.id,
        event_type=event.type,
        payload=event.to_dict()
    )

    try:
        if event.type == 'checkout.session.completed':
            _handle_checkout_completed(event.data.object)
        elif event.type == 'customer.subscription.created':
            _handle_subscription_updated(event.data.object)
        elif event.type == 'customer.subscription.updated':
            _handle_subscription_updated(event.data.object)
        elif event.type == 'customer.subscription.deleted':
            _handle_subscription_deleted(event.data.object)
        elif event.type == 'invoice.paid':
            _handle_invoice_paid(event.data.object)
        elif event.type == 'invoice.payment_failed':
            _handle_invoice_payment_failed(event.data.object)
        
        return True, "Processed"
    except Exception as e:
        logger.error(f"Webhook Error [{event.type}]: {str(e)}")
        return False, str(e)

def _handle_checkout_completed(session):
    from django.contrib.auth.models import User
    user_id = session.metadata.get('user_id')
    tier_id = session.metadata.get('tier_id')
    customer_id = session.customer
    subscription_id = session.subscription

    if user_id:
        user = User.objects.get(id=user_id)
        sub = user.subscription
        sub.stripe_customer_id = customer_id
        sub.stripe_subscription_id = subscription_id
        
        tier = None
        if tier_id:
            tier = Tier.objects.get(id=tier_id)
            sub.tier = tier
        sub.save()

        # RECORD TRANSACTION
        from .financial_models import FinancialTransaction
        FinancialTransaction.objects.create(
            user=user,
            stripe_event_id=session.id,
            type='SUBSCRIPTION',
            amount=session.amount_total / 100, # Stripe uses cents
            tier=tier
        )

def _handle_subscription_updated(stripe_sub):
    sub = UserSubscription.objects.filter(stripe_subscription_id=stripe_sub.id).first()
    
    # Fallback to metadata if ID lookup fails (common in initial 'created' event)
    if not sub:
        user_id = stripe_sub.metadata.get('user_id')
        if user_id:
            from django.contrib.auth.models import User
            user = User.objects.filter(id=user_id).first()
            if user:
                sub = user.subscription
                sub.stripe_subscription_id = stripe_sub.id

    if sub:
        sub.stripe_status = stripe_sub.status
        sub.current_period_end = timezone.datetime.fromtimestamp(stripe_sub.current_period_end, tz=timezone.utc)
        sub.cancel_at_period_end = stripe_sub.cancel_at_period_end
        
        # Sync tier if price changed
        if stripe_sub.get('plan'):
            price_id = stripe_sub.plan.id
            new_tier = Tier.objects.filter(stripe_price_id=price_id).first()
            if new_tier:
                sub.tier = new_tier
        
        sub.save()

def _handle_subscription_deleted(stripe_sub):
    sub = UserSubscription.objects.filter(stripe_subscription_id=stripe_sub.id).first()
    if sub:
        sub.stripe_status = 'canceled'
        # Optional: Downgrade to free tier
        free_tier = Tier.objects.filter(price=0).first()
        if free_tier:
            sub.tier = free_tier
        sub.save()

def _handle_invoice_paid(invoice):
    # This ensures that even if checkout.session.completed hasn't arrived, the sub is active
    sub_id = invoice.subscription
    if sub_id:
        sub = UserSubscription.objects.filter(stripe_subscription_id=sub_id).first()
        if sub:
            sub.stripe_status = 'active'
            sub.save()

def _handle_invoice_payment_failed(invoice):
    sub_id = invoice.subscription
    if sub_id:
        sub = UserSubscription.objects.filter(stripe_subscription_id=sub_id).first()
        if sub:
            sub.stripe_status = 'past_due'
            sub.save()
