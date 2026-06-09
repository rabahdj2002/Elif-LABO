from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.urls import reverse
from django import forms
from django.db.models import Sum, Count, Avg, Q
from .models import Inquiry, Planet, RoomState, EngineRun, SystemSettings, SpendRecord, Tier, UserSubscription, IssueReport, StripeWebhookLog, DailyFinancialSnapshot, FinancialTransaction, BusinessAlert, SystemTestRun, Notification
from .financial_service import FinancialAnalyticsService
from .system_tests import run_system_tests_async
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from engine_bridge.services import EngineService
from .tasks import run_engine_task
import logging
import stripe
from .utils_stripe import create_checkout_session, handle_webhook_event, get_stripe_client


logger = logging.getLogger(__name__)

from celery.result import AsyncResult
import io
import json
import re
import time
import threading
from contextlib import redirect_stdout
from django.db import connection
from .utils import run_threaded_task, collect_inquiry_report_data
from django.template.loader import render_to_string

def _check_auth(request, inquiry):
    """Refuse access if not superuser and not the owner."""
    if not request.user.is_superuser and inquiry.user != request.user:
        return False
    return True

def _is_engine_busy(request):
    """
    Helper to check if the session lock is valid.
    Self-heals if the inquiry in the session is actually finished, deleted, or stale.
    """
    active_pk = request.session.get('active_engine_pk')
    if not active_pk:
        return False
        
    try:
        active_inq = Inquiry.objects.get(pk=active_pk)
        
        # 1. Check for finished statuses
        if active_inq.status in ['COMPLETED', 'FAILED', 'REFUSED', 'DELETED']:
            # Stale lock - inquiry finished but session not updated
            del request.session['active_engine_pk']
            request.session.modified = True
            return False
            
        # 2. Check for staleness (e.g., if it's been running/pending for > 15 minutes)
        # Since we have timeouts on tasks (10m), 15m is a safe buffer.
        from django.utils import timezone
        from datetime import timedelta
        if active_inq.updated_at < timezone.now() - timedelta(minutes=15):
            # Force clear stale lock
            del request.session['active_engine_pk']
            request.session.modified = True
            return False
            
        return True # Still busy
    except Inquiry.DoesNotExist:
        # Record gone - clear lock
        del request.session['active_engine_pk']
        request.session.modified = True
        return False

@login_required
def clear_engine_lock(request):
    """Manually clear the active engine lock from the user's session."""
    if 'active_engine_pk' in request.session:
        del request.session['active_engine_pk']
        request.session.modified = True
        messages.success(request, "Reasoning lock cleared. You can now initiate a new inquiry.")
    else:
        messages.info(request, "No active engine lock found.")
    
    return redirect(request.META.get('HTTP_REFERER', 'discovery:system_map'))

def admin_access_required(permission=None):
    """
    Decorator for views that require either Superuser or 'Limited Admin' status.
    If a permission name is provided, 'Limited Admin' must have that permission in their JSON blob.
    """
    def decorator(view_func):
        from functools import wraps
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("discovery:landing")
            
            subscription = getattr(request.user, 'subscription', None)
            
            # Superuser always bypasses checks
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check Limited Admin
            if subscription and subscription.user_type == 'ADMIN':
                if permission:
                    # Check the permission in the JSON field
                    if subscription.admin_permissions.get(permission):
                        return view_func(request, *args, **kwargs)
                    else:
                        messages.error(request, f"Permission Denied: You do not have the '{permission}' authority.")
                        return redirect("discovery:admin_dashboard")
                return view_func(request, *args, **kwargs)
                
            messages.error(request, "Permission Denied: This area is restricted to system administrators.")
            return redirect("discovery:system_map")
        return _wrapped_view
    return decorator

@login_required
def profile_view(request):
    """User-facing profile/settings view."""
    if request.method == "POST":
        # Handle account update
        if "update_account" in request.POST:
            email = request.POST.get("email")
            specializations = request.POST.getlist("specializations[]")
            
            if email:
                request.user.email = email
                request.user.save()
            
            subscription = getattr(request.user, 'subscription', None)
            if subscription:
                # Clean up empty strings and ensure uniqueness
                specializations = list(set([s.strip() for s in specializations if s.strip()]))
                subscription.research_specializations = specializations
                subscription.save()
                
            messages.success(request, "Identity and specializations updated.")
            return redirect("discovery:profile")
        
        # Handle password change
        if "change_password" in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, "Your password was successfully updated!")
                return redirect("discovery:profile")
            else:
                messages.error(request, "Please correct the error below.")
                # We need to render the page with errors if the form is invalid
                subscription = getattr(request.user, 'subscription', None)
                password_form = form
                return render(request, "discovery/profile.html", {
                    "user": request.user,
                    "subscription": subscription,
                    "password_form": password_form,
                    "system_settings": SystemSettings.get_settings()
                })

        # Handle account deactivation
        if "deactivate_account" in request.POST:
            user = request.user
            user.is_active = False
            user.save()
            from django.contrib.auth import logout
            logout(request)
            messages.warning(request, "Your account has been deactivated. Contact an administrator to re-enable access.")
            return redirect("discovery:system_map")

    subscription = getattr(request.user, 'subscription', None)
    password_form = PasswordChangeForm(request.user)
    return render(request, "discovery/profile.html", {
        "user": request.user,
        "subscription": subscription,
        "password_form": password_form,
        "system_settings": SystemSettings.get_settings()
    })

@user_passes_test(lambda u: u.is_superuser)
def system_settings_view(request):
    """View to manage global engine and UI parameters. Restricted to Superusers."""
    settings = SystemSettings.get_settings()
    
    if request.method == "POST":
        settings.auto_refresh_ms = int(request.POST.get("auto_refresh_ms", 5000))
        settings.strict_governance = request.POST.get("strict_governance") == "on"
        settings.debug_mode = request.POST.get("debug_mode") == "on"
        settings.show_spending_overview = request.POST.get("show_spending_overview") == "on"
        settings.system_version = request.POST.get("system_version", "V1.0 ALPHA")
        settings.documentation_content = request.POST.get("documentation_content", settings.documentation_content)
        settings.save()
        messages.success(request, "System parameters updated successfully.")
        return redirect("discovery:settings")

    return render(request, "discovery/settings.html", {"settings": settings})

@user_passes_test(lambda u: u.is_superuser)
def admin_integrations_center(request):
    """Centralized management for AI models, Stripe, and other external APIs."""
    settings = SystemSettings.get_settings()
    from .models import StripeWebhookLog
    from .db_service import DatabaseService
    import stripe
    import time
    from django.http import HttpResponse # Added back for safety

    stripe_status = "Unknown"
    last_webhook = StripeWebhookLog.objects.order_by('-processed_at').first()
    
    if settings.stripe_secret_key:
        try:
            stripe.api_key = settings.stripe_secret_key
            stripe.Account.retrieve()
            stripe_status = "Connected"
        except Exception as e:
            stripe_status = f"Error: {str(e)}"
    else:
        stripe_status = "Not Configured"

    if request.method == "POST":
        # Check which section was submitted to avoid overwriting unrelated fields
        section_ai = "save_ai" in request.POST
        section_stripe = "save_stripe" in request.POST or "test_stripe" in request.POST
        section_db = "save_db" in request.POST or "test_db" in request.POST
        section_email = "save_email" in request.POST or "test_email" in request.POST

        if "test_email" in request.POST:
            from .email_service import EmailService
            # Update settings object with values from POST (for the test)
            settings.smtp_host = request.POST.get("smtp_host")
            settings.smtp_port = int(request.POST.get("smtp_port") or 587)
            settings.smtp_user = request.POST.get("smtp_user")
            # Only update password if provided
            new_pass = request.POST.get("smtp_pass")
            if new_pass:
                settings.smtp_pass = new_pass
            settings.smtp_use_tls = request.POST.get("smtp_use_tls") == "on"
            settings.email_from_address = request.POST.get("email_from_address")
            
            test_recipient = request.POST.get("test_recipient")
            if not test_recipient:
                messages.error(request, "Recipient email is required for testing.")
            else:
                success, msg = EmailService.send_mail(
                    subject="ELIF System: SMTP Channel Verification",
                    message="If you're reading this, your SMTP configuration is functional.",
                    recipient_list=[test_recipient],
                    html_content="<div style='font-family: sans-serif; padding: 20px; border: 1px solid #1d4ed8; border-radius: 8px;'><h2 style='color: #1d4ed8;'>SMTP Channel Verification</h2><p>Integrated successfully.</p></div>"
                )
                if success:
                    messages.success(request, f"Test email dispatched successfully to {test_recipient}. Check your inbox.")
                    settings.save() # If test passed, auto-save settings
                else:
                    messages.error(request, f"Email Dispatch Failed: {msg}")
            return redirect("discovery:integrations_center")

        if "test_stripe" in request.POST:
            # Update values in memory to test them
            settings.stripe_public_key = request.POST.get("stripe_public_key")
            settings.stripe_secret_key = request.POST.get("stripe_secret_key")
            settings.stripe_webhook_secret = request.POST.get("stripe_webhook_secret")
            settings.stripe_live_mode = request.POST.get("stripe_live_mode") == "on"
            
            if not settings.stripe_secret_key:
                messages.error(request, "Stripe Secret Key is required to test connectivity.")
            else:
                try:
                    stripe.api_key = settings.stripe_secret_key
                    stripe.Account.retrieve()
                    messages.success(request, "Stripe Connectivity Verified: Account retrieved successfully.")
                    settings.save() # Persist keys if test succeeded
                except Exception as e:
                    messages.error(request, f"Stripe Connection Failed: {str(e)}")
            return redirect("discovery:integrations_center")
            
        if "test_db" in request.POST:
            # Connection testing now uses internal credentials from settings.py
            success, msg = DatabaseService.test_connection(settings)
            if success:
                messages.success(request, f"Internal Database Connection Verified: {msg}")
            else:
                messages.error(request, f"Internal Database Connection Failed: {msg}")
            return redirect("discovery:integrations_center")

        # Handle UI Section Saves
        if section_ai:
            if "active_model" in request.POST:
                settings.active_model = request.POST.get("active_model")
            if "anthropic_api_key" in request.POST:
                settings.anthropic_api_key = request.POST.get("anthropic_api_key")
            if "deepseek_api_key" in request.POST:
                settings.deepseek_api_key = request.POST.get("deepseek_api_key")
            
            settings.offline_mode = request.POST.get("offline_mode") == "on"
            settings.enable_web_search = request.POST.get("enable_web_search") == "on"
            settings.save()
            messages.success(request, "Intelligence parameters updated.")
            return redirect("discovery:integrations_center")

        if section_email:
            settings.smtp_host = request.POST.get("smtp_host")
            settings.smtp_port = int(request.POST.get("smtp_port") or 587)
            settings.smtp_user = request.POST.get("smtp_user")
            
            new_pass = request.POST.get("smtp_pass")
            if new_pass:
                settings.smtp_pass = new_pass
                
            settings.smtp_use_tls = request.POST.get("smtp_use_tls") == "on"
            settings.email_from_address = request.POST.get("email_from_address")
            settings.save()
            messages.success(request, "Communication layer parameters updated.")
            return redirect("discovery:integrations_center")

        if section_db:
            settings.db_pg_host = request.POST.get("db_pg_host")
            settings.db_pg_port = request.POST.get("db_pg_port")
            settings.db_pg_name = request.POST.get("db_pg_name")
            settings.db_pg_user = request.POST.get("db_pg_user")
            settings.db_pg_password = request.POST.get("db_pg_password")
            settings.db_pg_ssl_mode = request.POST.get("db_pg_ssl_mode")
            settings.use_postgres = request.POST.get("use_postgres") == "on"
            
            settings.save()
            messages.success(request, "Database substrate parameters updated.")
            return redirect("discovery:integrations_center")

        if section_stripe:
            if "stripe_public_key" in request.POST:
                settings.stripe_public_key = request.POST.get("stripe_public_key")
            if "stripe_secret_key" in request.POST:
                settings.stripe_secret_key = request.POST.get("stripe_secret_key")
            if "stripe_webhook_secret" in request.POST:
                settings.stripe_webhook_secret = request.POST.get("stripe_webhook_secret")
            
            settings.stripe_live_mode = request.POST.get("stripe_live_mode") == "on"
            settings.save()
            messages.success(request, "Financial parameters updated.")
            return redirect("discovery:integrations_center")

    return render(request, "discovery/integrations_center.html", {
        "settings": settings,
        "stripe_status": stripe_status,
        "last_webhook": last_webhook,
        "webhook_count": StripeWebhookLog.objects.count()
    })

@user_passes_test(lambda u: u.is_superuser)
def db_backup_download(request):
    """Generates and downloads a JSON dump of the current database."""
    from .db_service import DatabaseService
    try:
        data = DatabaseService.dump_database_json()
        response = HttpResponse(data, content_type='application/json')
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        response['Content-Disposition'] = f'attachment; filename="elif_backup_{timestamp}.json"'
        return response
    except Exception as e:
        messages.error(request, f"Backup failed: {str(e)}")
        return redirect("discovery:integrations_center")

@user_passes_test(lambda u: u.is_superuser)
def db_restore_upload(request):
    """Restores database from an uploaded JSON file."""
    if request.method == "POST" and request.FILES.get('backup_file'):
        from .db_service import DatabaseService
        backup_file = request.FILES['backup_file']
        try:
            content = backup_file.read().decode('utf-8')
            success, msg = DatabaseService.load_database_json(content)
            if success:
                messages.success(request, msg)
            else:
                messages.error(request, f"Restore failed: {msg}")
        except Exception as e:
            messages.error(request, f"Restore error: {str(e)}")
    else:
        messages.error(request, "No backup file provided.")
    
    return redirect("discovery:integrations_center")

@user_passes_test(lambda u: u.is_superuser)
def db_restore_sqlite_migration(request):
    """Migrates data from the local db.sqlite3 to the active database (Postgres)."""
    from .db_service import DatabaseService
    success, msg = DatabaseService.migrate_from_sqlite()
    if success:
        messages.success(request, msg)
    else:
        messages.error(request, f"SQLite migration failed: {msg}")
    
    return redirect("discovery:integrations_center")

@login_required
def documentation_view(request):
    """Protocol Documentation and Tutorials."""
    settings = SystemSettings.get_settings()
    
    # Initialize with default content if empty
    if not settings.documentation_content:
        settings.documentation_content = """# ELIF Universe: Phase V1 Protocol

Welcome to the **ELIF Universe Protocol Documentation**. This guide outlines the architectural logic, operational procedures, and cognitive framework of the ELIF Laboratory.

---

## 01. The Cognitive Archive
The ELIF system organizes intelligence into **Cognitive Sectors** (Folders). Unlike linear chat systems, ELIF treats every inquiry as a structured case file.

*   **Case Indexing**: Every inquiry is assigned a unique `case_id` (e.g., `case_01`).
*   **Temporal Sorting**: The archive dynamically promotes active inquiries to the top of your workspace.
*   **Sector Isolation**: Knowledge is compartmentalized to maintain the integrity of specific logic streams.

## 02. The Logic Pipeline
When you initialize an inquiry, it passes through an immutable reasoning sequence:

1.  **Frame Validation**: Ensuring the inquiry falls within operative boundaries.
2.  **Object Decomposition**: Breaking complex objectives into atomic logical units.
3.  **Hypothesis Validation**: Testing branching paths for capacity accumulation.
4.  **Governance Kernel**: Applying strict constraints to the final output.

## 03. Room Architectures
Each inquiry is visualised across different "Rooms" designed for specific cognitive tasks:

### 🧭 Exploration Room
Visualize the branching roadmap of your inquiry. Each node represents a decision point or a breakthrough in the logic.

### ⚠️ Uncertainty Room
The audit chamber where biases, logical gaps, and failure conditions are exposed for adjudication.

### ⚖️ Governance Room
Where the final operative truth is separated from speculative noise, providing the definitive verdict.

## 04. System Management
Administrators can calibrate the system via the **System Control** panel:
*   **Intelligence Model**: Canonical selection (e.g., Claude 4.5 Sonnet).
*   **Reasoning Depth**: Fine-tuning the depth of the logic engine (3-15 levels).
*   **Budgeting**: Real-time spending overview and API quota management.

---

> *\"Logic is the architect; governance is the guardian.\"* - ELIF Core Doctrine
"""
        settings.save()
    
    if request.method == "POST" and request.user.is_superuser:
        settings.documentation_content = request.POST.get("documentation_content", "")
        settings.save()
        messages.success(request, "Documentation updated successfully.")
        return redirect("discovery:documentation")
        
    return render(request, "discovery/documentation.html", {
        "documentation_content": settings.documentation_content
    })

def engine_events(request, pk):
    """
    Server-Sent Events (SSE) stream for engine progress.
    Provides real-time updates of Inquiry and Planet states.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)

    def event_stream():
        last_state = ""
        while True:
            # Re-fetch from DB to get latest state
            try:
                inquiry.refresh_from_db()
            except Exception:
                break # Model deleted or connection lost
                
            planets = inquiry.planets.all().order_by('order')
            
            # Construct a minimal representation of the whole pipeline state
            state_obj = {
                "inquiry_id": str(inquiry.id),
                "status": inquiry.status,
                "message": inquiry.current_status_msg,
                "steps": [
                    {
                        "order": p.order,
                        "name": p.name,
                        "status": p.status,
                    } for p in planets
                ]
            }
            
            current_state_json = json.dumps(state_obj)
            
            # Only send if state has changed (to save bandwidth)
            if current_state_json != last_state:
                yield f"data: {current_state_json}\n\n"
                last_state = current_state_json
            
            # Safety break if inquiry reached a terminal state
            if inquiry.status in ['COMPLETED', 'FAILED', 'REFUSED']:
                # Clear session tracker for this inquiry
                if request.session.get('active_engine_pk') == str(inquiry.pk):
                    del request.session['active_engine_pk']
                    request.session.modified = True
                
                # Send one last update then close
                yield f"data: {current_state_json}\n\n"
                break
                
            time.sleep(1) # Poll DB every 1s

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

@login_required
def engine_telemetry(request, pk):
    """Returns a full JSON status of the engine for polling fallback."""
    inquiry = get_object_or_404(Inquiry, pk=pk)

    if not _check_auth(request, inquiry):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    planets = inquiry.planets.all().order_by('order')
    
    # If terminal state or stale, clear from session
    if inquiry.status in ['COMPLETED', 'FAILED', 'REFUSED']:
        if request.session.get('active_engine_pk') == str(pk):
            del request.session['active_engine_pk']
            request.session.modified = True
            print(f"DEBUG: Cleared session lock for Inquiry {pk} (Terminal State)")

    data = {
        "inquiry_id": str(inquiry.id),
        "status": inquiry.status,
        "message": inquiry.current_status_msg,
        "steps": [
            {
                "order": p.order,
                "name": p.name,
                "status": p.status,
            } for p in planets
        ]
    }
    return JsonResponse(data)

def landing_page(request):
    """The public landing page / entry point."""
    if request.user.is_authenticated:
        return redirect("discovery:system_map")
    tiers = Tier.objects.all().order_by('price', 'id')
    return render(request, 'discovery/landing.html', {
        'system_settings': SystemSettings.get_settings(),
        'tiers': tiers,
        'hide_sidebar': True
    })


@login_required
def system_map(request):
    """The main view of all inquiries grouped by Topic."""
    # Admins should not see their own (non-existent) inquiries but their management view
    if request.user.is_superuser or (getattr(request.user, 'subscription', None) and request.user.subscription.user_type == 'ADMIN'):
        return redirect("discovery:admin_dashboard")

    # If superuser, they see everything in the admin dash, but maybe we want them to see their own here?
    # Usually users see their own inquiries.
    all_inquiries = Inquiry.objects.filter(user=request.user, is_visible_to_user=True).order_by("-updated_at")

    # Group inquiries by topic
    topics_dict = {}
    for inq in all_inquiries:
        topic_name = inq.topic or "Uncategorized"

        # Determine if this inquiry is "Active" (has incomplete steps)
        completed_planets = inq.planets.filter(status='COMPLETED').count()
        is_active = completed_planets < 11

        if topic_name not in topics_dict:
            # Get the shared prefix number for this topic folder
            match = re.match(r"case_(\d+)_", inq.case_id)
            prefix = f"CASE_{match.group(1)}" if match else "CASE_XX"
            topics_dict[topic_name] = {
                "name": topic_name,
                "prefix": prefix,
                "inquiries": [],
                "active_count": 0,
                "last_updated": inq.updated_at
            }

        topics_dict[topic_name]["inquiries"].append(inq)
        if is_active:
            topics_dict[topic_name]["active_count"] += 1

        # Update last_updated if this inquiry is more recent
        if inq.updated_at > topics_dict[topic_name]["last_updated"]:
            topics_dict[topic_name]["last_updated"] = inq.updated_at

    # Sort topics by last_updated (descending)
    sorted_topics = sorted(topics_dict.values(), key=lambda x: x["last_updated"], reverse=True)

    # User Performance Statistics (Formerly Metacognitive Statistics)
    # Filter by user to ensure stats are specific to the logged-in user
    # Only count planets from inquiries that are visible to the user
    user_planets = Planet.objects.filter(inquiry__user=request.user, inquiry__is_visible_to_user=True)
    planets_resolved = user_planets.filter(status='COMPLETED').count()
    
    # Usage calculation based on subscription limits
    from .models import UserSubscription
    sub = getattr(request.user, 'subscription', None)
    usage_pc = 0.0
    if sub and sub.tier.inquiry_limit > 0:
        usage_pc = (sub.inquiry_usage / sub.tier.inquiry_limit) * 100

    context = {
        "topics": sorted_topics,
        "total_inquiries": all_inquiries.count(),
        "planets_resolved": planets_resolved,
        "usage": f"{usage_pc:.1f}%",
        "system_settings": SystemSettings.get_settings()
    }
    return render(request, "discovery/index.html", context)

@login_required
def topic_detail(request, topic_name):
    """
    Shows a timeline view of all inquiries within a specific topic folder.
    """
    inquiries_list = Inquiry.objects.filter(topic=topic_name, user=request.user, is_visible_to_user=True).order_by("created_at")
    if not inquiries_list.exists():
        messages.error(request, f"Topic '{topic_name}' not found.")
        return redirect("discovery:system_map")
    
    # Annotate inquiries with their active status
    inquiries = []
    for inq in inquiries_list:
        completed = inq.planets.filter(status='COMPLETED').count()
        inq.is_active = completed < 11
        inquiries.append(inq)
    
    # Get the sequence prefix from the first inquiry
    match = re.match(r"case_(\d+)_", inquiries[0].case_id)
    topic_prefix = f"CASE_{match.group(1)}" if match else "CASE_XX"
    
    context = {
        "topic_name": topic_name,
        "topic_prefix": topic_prefix,
        "inquiries": inquiries, # Chronological order
    }
    return render(request, "discovery/topic_detail.html", context)

@login_required
def initialize_inquiry(request):
    """POST view to start a new inquiry."""
    # Restricted: Admins cannot initialize inquiries
    if request.user.is_superuser or (getattr(request.user, 'subscription', None) and request.user.subscription.user_type == 'ADMIN'):
        messages.error(request, "Permission Denied: Administrators and Superusers cannot initialize inquiries.")
        return redirect("discovery:admin_dashboard")

    # Emergency Lock Override: If user adds ?force=1, we clear the busy state
    if request.GET.get('force') == '1':
        if 'active_engine_pk' in request.session:
            del request.session['active_engine_pk']
            request.session.modified = True
            messages.info(request, "Engine lock manually cleared.")

    # Block concurrent engine runs for the same account
    if _is_engine_busy(request):
        messages.error(request, "Engine Busy: A cognitive process is already active. Please wait for completion or clear your lock in Profile settings.")
        return redirect("discovery:system_map")

    # Inquiry & Spend Limit Check
    # Ensure default tier exists or use the system setting
    settings = SystemSettings.get_settings()
    
    if settings.default_tier:
        target_tier = settings.default_tier
    else:
        target_tier, _ = Tier.objects.get_or_create(name="Free", defaults={"inquiry_limit": 5, "spend_limit": 10.00, "price": 0.00})
        
    subscription, _ = UserSubscription.objects.get_or_create(user=request.user, defaults={"tier": target_tier})
    
    if not request.user.is_superuser:
        # 1. Check Spend Safety Net FIRST (Financial Safeguard)
        if subscription.spend_usage >= subscription.tier.spend_limit:
            messages.error(request, f"Financial Safeguard Triggered: Your current spend (${subscription.spend_usage:.2f}) has exceeded your tier's safety limit (${subscription.tier.spend_limit:.2f}). Please upgrade to continue.")
            return redirect("discovery:subscription")
            
        # 2. Check Inquiry Cap SECOND (Operational Limit)
        if subscription.inquiry_usage >= subscription.tier.inquiry_limit:
            messages.error(request, f"Inquiry Limit Reached: Your current tier allows only {subscription.tier.inquiry_limit} inquiries. Please upgrade your subscription.")
            return redirect("discovery:subscription")

    if request.method == "POST":
        question = request.POST.get("question")
        topic_input = request.POST.get("topic")
        spec_input = request.POST.get("specialization")
        
        # Build a case for every single input from a template generated based on the existing cases
        from engine_bridge.services import EngineService
        case_id, topic = EngineService.generate_case_id(question, topic=topic_input)

        inquiry = Inquiry.objects.create(
            case_id=case_id,
            topic=topic,
            core_question=question,
            current_question_state=question,
            user=request.user,
            specialization=spec_input
        )

        # The worker will handle pre-populating planets (Step 1-11)
        try:
            from .workflow_tasks import start_engine_workflow
            
            # Use CELERY_TASK_ALWAYS_EAGER check to provide immediate fallback if broker is dead
            from django.conf import settings as django_settings
            
            # Dispatch task
            if getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False):
                # If we are in Eager mode (likely local dev without Redis),
                # we MUST use a thread to prevent the UI from freezing.
                run_threaded_task(start_engine_workflow.delay, str(inquiry.id))
            else:
                # Standard Celery dispatch (non-blocking if Redis is running)
                start_engine_workflow.delay(str(inquiry.id))
            
            # Persist the active task state in session for UI persistence
            request.session['active_engine_pk'] = str(inquiry.pk)
            request.session.modified = True
            
        except Exception as e:
            import traceback
            error_msg = f"Failed to dispatch workflow: {str(e)}"
            print(f"ERROR: {error_msg}")
            print(traceback.format_exc())
            messages.error(request, error_msg)
            
        return redirect("discovery:inquiry_detail", pk=inquiry.pk)
    
    return render(request, "discovery/initialize.html")

@login_required
def task_status_view(request, task_id):
    """Endpoint to check the status of a Celery task."""
    result = AsyncResult(task_id)
    response_data = {
        "task_id": task_id,
        "status": result.status,
        "ready": result.ready(),
    }
    if result.ready():
        response_data["result"] = result.result if not isinstance(result.result, Exception) else str(result.result)
    
    return JsonResponse(response_data)

@login_required
def inquiry_detail(request, pk):
    """
    LAYER 3: EXPERIENCE LAYER (REDIRECT TO ROOMS)
    The main dash is now replaced by the Discovery Room.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)
    
    # Check authorization
    if not _check_auth(request, inquiry):
        messages.error(request, "Sovereign Denial: You do not have authorization to access this reality.")
        return redirect("discovery:system_map")

    rooms_to_create = [r[0] for r in RoomState.ROOM_CHOICES]
    for r_type in rooms_to_create:
        RoomState.objects.get_or_create(inquiry=inquiry, room_type=r_type)

    return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

@login_required
def complete_walkthrough(request):
    """AJAX endpoint to mark the onboarding tour as completed."""
    if request.method == "POST":
        sub = getattr(request.user, 'subscription', None)
        if sub:
            sub.has_seen_walkthrough = True
            sub.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@login_required
def room_view(request, pk, room_type):
    """
    Universal Room Renderer for Layer 3.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)
    
    # Check authorization
    if not _check_auth(request, inquiry):
        messages.error(request, "Sovereign Denial: Access Restricted.")
        return redirect("discovery:system_map")

    room_state, _ = RoomState.objects.get_or_create(inquiry=inquiry, room_type=room_type.upper())
    
    # Auto-sync projection if out of date or running
    room_state.sync_from_planets()

    # Map types to templates
    template_map = {
        "DISCOVERY": "discovery/rooms/discovery.html",
        "EVIDENCE": "discovery/rooms/evidence.html",
        "EXPLORATION": "discovery/rooms/exploration.html",
        "SOLUTION": "discovery/rooms/solution.html",
        "PROJECTION": "discovery/rooms/projection.html",
        "GOVERNANCE": "discovery/rooms/governance.html",
        "UNCERTAINTY": "discovery/rooms/uncertainty.html",
        "DECISION": "discovery/rooms/decision.html",
    }
    
    context = {
        "inquiry": inquiry,
        "planets": inquiry.planets.all().order_by('order'),
        "room_type": room_type.upper(),
        "room_data": room_state.room_data,
        "nav_rooms": RoomState.ROOM_CHOICES
    }
    
    response = render(request, template_map.get(room_type.upper(), "discovery/rooms/discovery.html"), context)
    # Force no-cache for live rooms
    if inquiry.status in ['RUNNING', 'PENDING']:
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
    return response

def _process_inquiry_sync_results(inquiry, request, snapshot=None):
    """
    Consolidated metadata update logic for both manual syncs and branching.
    Calculates Confidence based on Epistemic Stability (Article IV Sovereignty).
    Supports Epistemic Contraction rewards (Article VII).
    """
    inquiry.refresh_from_db()
    
    inquiry.history_log.append({
        "timestamp": str(inquiry.updated_at),
        "event": "Full Engine Re-run",
        "trigger": request.POST.get("reason", "Manual Refresh")
    })
    
    # 1. BASE AI CONFIDENCE (Epistemic Input - Step 9 Kernel)
    step_9_planet = inquiry.planets.filter(name__icontains="Step 9").first()
    if not step_9_planet or not step_9_planet.data or not step_9_planet.data.get("confidence"):
        step_9_planet = inquiry.planets.filter(name__icontains="Step 10").first()

    base_ai_confidence = 50
    if step_9_planet and step_9_planet.data:
        raw_confidence = step_9_planet.data.get("confidence") or \
                         step_9_planet.data.get("confidence_rating") or \
                         step_9_planet.data.get("stability_score") or "0"
        c_lower = str(raw_confidence).lower()
        if "high" in c_lower and "medium" not in c_lower: base_ai_confidence = 88
        elif "medium" in c_lower and "low" not in c_lower: base_ai_confidence = 55
        elif "low" in c_lower: base_ai_confidence = 28
        else:
            match = re.search(r"(\d+)", str(raw_confidence))
            if match:
                val = int(match.group(1))
                base_ai_confidence = val * 10 if val <= 10 else val

    # 2. UNCERTAINTY DENSITY (Penalty for unresolved components)
    unresolved_count = len(inquiry.unresolved_zones or [])
    uncertainty_penalty = min(unresolved_count * 7, 45) # Max 45% penalty
    
    # 3. DIVERGENCE VOLATILITY (Reality Forks indicate ambiguity)
    divergence_count = len(inquiry.divergences or [])
    divergence_penalty = min(divergence_count * 6, 30) # Max 30% penalty

    # 4. FRAME DRIFT (Similarity between core and current question)
    q1 = str(inquiry.core_question).lower()
    q2 = str(inquiry.current_question_state).lower()
    drift_score = 100
    if q1 and q2 and q1 != q2:
        overlap = sum(1 for char in q1 if char in q2)
        drift_score = (overlap / max(len(q1), 1)) * 100

    # 5. EPISTEMIC CONTRACTION (Sovereign Recovery Signals)
    recovery_bonus = 0
    
    if snapshot:
        # A. Uncertainty Resolution
        prev_unresolved = snapshot.get('unresolved_count', 0)
        if unresolved_count < prev_unresolved:
            recovery_bonus += (prev_unresolved - unresolved_count) * 12
            
        # B. Divergence Collapse (Pruning reality forks)
        prev_divergences = snapshot.get('divergence_count', 0)
        if divergence_count < prev_divergences:
            recovery_bonus += (prev_divergences - divergence_count) * 10
            
    # C. Convergence Bonus (Stable frame across cycles)
    if drift_score >= 95:
        recovery_bonus += 15
    elif drift_score >= 85:
        recovery_bonus += 8

    # D. Step 10 Completion Bonus (Verdict reached)
    verdict_planet = inquiry.planets.filter(name__icontains="Step 10", status="COMPLETED").exists()
    if verdict_planet:
        recovery_bonus += 20 

    # 6. TEMPORAL STABILITY (Similarity to previous run)
    prev_confidence = 25
    if inquiry.confidence_evolution and len(inquiry.confidence_evolution) > 0:
        prev_confidence = inquiry.confidence_evolution[-1]
    
    # CALCULATE COMPOSITE STABILITY (The "Truth Separator" logic)
    stability_val = (drift_score * 0.4) + (base_ai_confidence * 0.6)
    stability_val -= uncertainty_penalty
    stability_val -= divergence_penalty
    stability_val += recovery_bonus
    
    # Final clamping and moving average smoothing
    final_confidence = (stability_val * 0.75) + (prev_confidence * 0.25)
    final_confidence = max(min(int(final_confidence), 98), 5)

    if not inquiry.confidence_evolution or abs(inquiry.confidence_evolution[-1] - final_confidence) >= 1:
        inquiry.confidence_evolution.append(final_confidence)
        if len(inquiry.confidence_evolution) > 20:
            inquiry.confidence_evolution = inquiry.confidence_evolution[-20:]
    
    inquiry.save()
    
    for room in RoomState.objects.filter(inquiry=inquiry):
        room.sync_from_planets()

@login_required
def spawn_branch_view(request, pk):
    """Handles the creation of a new inquiry branch from a divergence."""
    parent = get_object_or_404(Inquiry, pk=pk)

    if not _check_auth(request, parent):
        messages.error(request, "Sovereign Denial: Branching Unauthorized.")
        return redirect("discovery:system_map")
    
    # Tier & Limit Validation for Branching
    sub = getattr(request.user, 'subscription', None)
    if sub and not request.user.is_superuser:
        if sub.spend_usage >= sub.tier.spend_limit:
            messages.error(request, f"Financial Safeguard: Branching restricted. Spend limit reached.")
            if request.headers.get('HX-Request'):
                response = HttpResponse()
                response['HX-Redirect'] = reverse("discovery:subscription")
                return response
            return redirect("discovery:subscription")
            
        if sub.inquiry_usage >= sub.tier.inquiry_limit:
            messages.error(request, f"Inquiry Limit Reached: Your current tier allows only {sub.tier.inquiry_limit} inquiries. Please upgrade to branch into new trajectories.")
            if request.headers.get('HX-Request'):
                response = HttpResponse()
                response['HX-Redirect'] = reverse("discovery:subscription")
                return response
            return redirect("discovery:subscription")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        
        # 1. Spawn the child
        child = EngineService.spawn_branch(parent, title, description)
        
        # 2. Add specific history to the parent
        parent.history_log.append({
            "timestamp": str(parent.updated_at),
            "event": "Branching Initiated",
            "description": f"Diverged toward Trajectory: {title} (Coupled to avoid drift)",
            "child_id": str(child.id)
        })
        parent.save()
        
        # 3. Trigger immediate run for the child
        try:
            from .workflow_tasks import start_engine_workflow
            from django.conf import settings as django_settings
            
            if getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False):
                run_threaded_task(start_engine_workflow.delay, str(child.id))
            else:
                start_engine_workflow.delay(str(child.id))
            
            # Persist tracking
            request.session['active_engine_pk'] = str(child.pk)
            request.session.modified = True
        except Exception as e:
            logger.error(f"Failed to trigger branch workflow: {e}")
            messages.error(request, f"Engine failed to start for branch: {e}")

        if request.headers.get('HX-Request'):
            response = HttpResponse()
            response['HX-Redirect'] = reverse("discovery:room_view", kwargs={"pk": child.id, "room_type": "DISCOVERY"})
            return response
        else:
            return redirect("discovery:room_view", pk=child.id, room_type="DISCOVERY")
    
    return redirect("discovery:room_view", pk=pk, room_type="DECISION")

@login_required
def sync_engine_pulse(request, pk):
    """
    Invokes Layer 1, Updates Layer 2, Refreshes Layer 3.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)

    if not _check_auth(request, inquiry):
        messages.error(request, "Sovereign Denial: Intervention Restricted.")
        return redirect("discovery:system_map")

    # Block concurrent engine runs for the same account
    
    # Trigger the engine run asynchronously via Distributed Workflow
    try:
        from .workflow_tasks import start_engine_workflow
        from django.conf import settings as django_settings
        
        if getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False):
            run_threaded_task(start_engine_workflow.delay, str(inquiry.id))
        else:
            start_engine_workflow.delay(str(inquiry.id))
        
        # Persist the active task state in session for UI persistence
        request.session['active_engine_pk'] = str(inquiry.pk)
        request.session.modified = True

    except Exception as e:
        messages.error(request, f"Failed to dispatch workflow: {str(e)}")
    
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Redirect'] = reverse("discovery:room_view", kwargs={"pk": inquiry.id, "room_type": "DISCOVERY"})
        return response

    return redirect("discovery:room_view", pk=inquiry.id, room_type="DISCOVERY")

@login_required
def refine_inquiry(request, pk):
    """
    Takes user feedback, evolves the question using LLM, and re-runs the engine.
    """
    inquiry = get_object_or_404(Inquiry, pk=pk)
    
    if not _check_auth(request, inquiry):
        messages.error(request, "Sovereign Denial: Refinement Unauthorized.")
        return redirect("discovery:system_map")

    # Block concurrent engine runs for the same account
    directive = request.POST.get("directive", "")
    
    if request.method != "POST" or not directive:
        if not directive:
            messages.warning(request, "Please provide a refinement directive.")
        return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

    try:
        from engine_bridge.services import EngineService
        from .workflow_tasks import start_engine_workflow
        
        # 1. Update the question model
        EngineService.refine_question(inquiry, directive)
        
        # 2. Trigger asynchronous workflow
        from django.conf import settings as django_settings
        if getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False):
            run_threaded_task(start_engine_workflow.delay, str(inquiry.id))
        else:
            start_engine_workflow.delay(str(inquiry.id))
        
        request.session['active_engine_pk'] = str(inquiry.pk)
        request.session.modified = True
        
    except Exception as e:
        messages.error(request, f"Refinement Failed: {str(e)}")
        
    if request.htmx:
        from django_htmx.http import HttpResponseClientRefresh
        return HttpResponseClientRefresh()
        
    return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

@login_required
def branch_out_planet(request, pk):
    """HTMX endpoint to RE-RUN engine based on AI-provided options from Step 2."""
    planet = get_object_or_404(Planet, pk=pk)
    inquiry = planet.inquiry
    
    family_id = request.POST.get("family_id")
    family_desc = request.POST.get("family_desc")
    
    if not family_id:
        return render(request, "discovery/partials/telemetry_entry.html", {
            "log": "DIVERGENCE ERROR: Invalid path selection.",
            "planet": planet, "inquiry": inquiry
        })

    new_perspective = (
        f"DECISION MADE: User selected option [{family_id}]. \n"
        f"DESCRIPTION: {family_desc}\n\n"
        "ACTION: Evolve all downstream steps assuming this is TRUE. Bypass decomposition check."
    )
    
    from .models import ExplorationBranch
    ExplorationBranch.objects.create(
        inquiry=inquiry,
        parent_planet=planet,
        choice_made=f"Resolved via {family_id}",
        branch_data={"perspective_shift": new_perspective, "family_id": family_id}
    )
    
    planet.data["branch_active"] = True
    planet.data["divergence_point"] = f"Resolved via: {family_id}"
    planet.status = "COMPLETED"
    
    # We clear the resolution override during the re-run setup
    # so the engine can provide NEW decomposition axes if the new path 
    # encounters a different deadlock.
    keys_to_fix = ["verdict", "final_verdict", "validation", "analysis"]
    for k in keys_to_fix:
        if k in planet.data and "DECOMPOSITION" in str(planet.data[k]).upper():
            planet.data[k] = f"DIVERGENCE INITIATED: Path {family_id} selected."

    planet.save()
    
    # Mark downstream planets as needing refresh
    inquiry.planets.filter(order__gt=planet.order).update(status="IN_PROGRESS", data={})
    
    # Epistemic Snapshot
    snapshot = {
        "unresolved_count": len(inquiry.unresolved_zones or []),
        "divergence_count": len(inquiry.divergences or []),
    }
    
    try:
        from engine_bridge.services import EngineService
        from .workflow_tasks import start_engine_workflow
        
        original_q = inquiry.core_question
        inquiry.core_question = f"USER CHOICE: {family_desc}\n\n[ORIGINAL QUESTION]: {original_q}"
        inquiry.save()

        # Update planet state
        planet.data["branch_active"] = True 
        planet.data["divergence_point"] = f"Current Thread: {family_id}"
        planet.save()

        # Trigger Workflow
        from django.conf import settings as django_settings
        if getattr(django_settings, 'CELERY_TASK_ALWAYS_EAGER', False):
            run_threaded_task(start_engine_workflow.delay, str(inquiry.id))
        else:
            start_engine_workflow.delay(str(inquiry.id))
        
        request.session['active_engine_pk'] = str(inquiry.pk)
        request.session.modified = True

        return render(request, "discovery/partials/telemetry_entry.html", {
            "log": f"DIVERGENCE TRIGGERED: Path [{family_id}] resolved. Engine restarted in background.",
            "planet": planet, 
            "inquiry": inquiry, 
            "oob_swap": True
        })
    except Exception as e:
        return render(request, "discovery/partials/telemetry_entry.html", {
            "log": f"DIVERGENCE FAILURE: {str(e)}",
            "planet": planet, "inquiry": inquiry
        })

@login_required
def reset_inquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)

    if not _check_auth(request, inquiry):
        messages.error(request, "Sovereign Denial: Memory Reset Restricted.")
        return redirect("discovery:system_map")

    # Layer 1: Reset Planets (Reasoning Engine Artifacts)
    inquiry.planets.all().update(status="NOT_STARTED", data={})
    
    # Layer 1 Audit: Clear Engine Runs history
    inquiry.engine_runs.all().delete()
    
    # Layer 2: Clear Explorations (Divergence Tree)
    inquiry.explorations.all().delete()
    
    # Layer 3: Reset Room Projections
    inquiry.room_states.all().update(room_data={})
    
    # Reset Inquiry Core State (Layer 2)
    inquiry.current_question_state = inquiry.core_question
    inquiry.assumptions = []
    inquiry.evidence_map = {}
    inquiry.hypothesis_set = {}
    inquiry.solution_families = []
    inquiry.unresolved_zones = []
    inquiry.constraints = []
    inquiry.confidence_evolution = []
    inquiry.state_data = {}
    
    inquiry.history_log = [{
        "timestamp": str(inquiry.updated_at),
        "event": "System Reset",
        "trigger": "Manual Override"
    }]
    
    inquiry.save()
    
    messages.success(request, f"Inquiry '{inquiry.case_id}' has been reset to base state.")
    
    return redirect("discovery:room_view", pk=pk, room_type="DISCOVERY")

@login_required
def delete_inquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)

    if not _check_auth(request, inquiry):
        messages.error(request, "Sovereign Denial: Purge Restricted.")
        return redirect("discovery:system_map")

    case_id = inquiry.case_id
    
    # Clear session lock if this was the active engine
    if request.session.get('active_engine_pk') == str(pk):
        del request.session['active_engine_pk']
        request.session.modified = True

    # Soft delete: Persistent record for admin audit, hidden from user.
    inquiry.is_visible_to_user = False
    
    # Scrub from parent if this was a branch
    try:
        from .workflow_tasks import _scrub_parent_diversion
        _scrub_parent_diversion(inquiry)
    except:
        pass

    inquiry.status = 'DELETED'
    inquiry.investigation_status = "Deleted"
    inquiry.current_status_msg = "Purged by user."
    inquiry.save()

    if request.headers.get('HX-Request'):
        # For HTMX requests (like the autodelete button), we redirect via header
        response = HttpResponse()
        response['HX-Redirect'] = reverse("discovery:system_map")
        return response
        
    messages.success(request, f"Inquiry '{case_id}' has been purged from current display.")
    return redirect("discovery:system_map")

from django.core.paginator import Paginator

@admin_access_required('can_view_spend')
def spend_history(request):
    """Real-time financial tracking for all reasoning runs. Restricted to Admins."""
    records_list = SpendRecord.objects.all().order_by("-timestamp")
    
    # Pagination: 20 logs per page
    paginator = Paginator(records_list, 20)
    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)

    total_cost = records_list.aggregate(Sum('cost_usd'))['cost_usd__sum'] or 0.0
    total_tokens = records_list.aggregate(Sum('input_tokens'), Sum('output_tokens'))
    
    context = {
        "records": records,
        "total_cost": total_cost,
        "total_input_tokens": total_tokens['input_tokens__sum'] or 0,
        "total_output_tokens": total_tokens['output_tokens__sum'] or 0,
    }
    return render(request, "discovery/spend_history.html", context)


@login_required
def analytics_dashboard(request):
    is_admin = request.user.is_superuser
    if is_admin:
        base_inquiries = Inquiry.objects.filter(is_visible_to_user=True)
        base_spend = SpendRecord.objects.all()
    else:
        base_inquiries = Inquiry.objects.filter(user=request.user, is_visible_to_user=True)
        base_spend = SpendRecord.objects.filter(user=request.user)
    
    total_inquiries = base_inquiries.count()
    completed_inquiries = base_inquiries.filter(status="COMPLETED").count()
    
    # Behavior Metrics
    total_branches = base_inquiries.filter(parent_inquiry__isnull=False).count()
    from django.db.models import Count
    # Average depth = average number of completed planets per inquiry
    depth_stats = base_inquiries.annotate(num_planets=Count('planets', filter=Q(planets__status='COMPLETED'))).aggregate(Avg('num_planets'))
    avg_depth = depth_stats['num_planets__avg'] or 0.0
    
    # Peak complexity (max history log depth)
    peak_complexity = 0
    for inq in base_inquiries:
        if inq.history_log and len(inq.history_log) > peak_complexity:
            peak_complexity = len(inq.history_log)

    from django.utils import timezone
    from datetime import timedelta
    thirty_days_ago = timezone.now() - timedelta(days=30)
    usage_over_time = base_inquiries.filter(created_at__gte=thirty_days_ago).extra(select={"day": "date(created_at)"}).values("day").annotate(count=Count("id")).order_by("day")
    status_distribution = base_inquiries.values("status").annotate(count=Count("id"))
    
    usage_labels = []
    usage_data = []
    for u in usage_over_time:
        label = u["day"].strftime("%d %b") if hasattr(u["day"], "strftime") else str(u["day"])
        usage_labels.append(label)
        usage_data.append(u["count"])
        
    context = {
        "is_admin": is_admin, 
        "total_inquiries": total_inquiries, 
        "completed_inquiries": completed_inquiries,
        "total_branches": total_branches,
        "avg_depth": avg_depth,
        "peak_complexity": peak_complexity,
        "usage_labels": usage_labels, 
        "usage_data": usage_data, 
        "status_distribution": list(status_distribution),
        "topic_distribution": list(base_inquiries.values("topic").annotate(count=Count("id")).order_by("-count")[:5])
    }
    
    # Spend Data (Admin Only)
    if is_admin:
        total_spend = base_spend.aggregate(Sum("cost_usd"))["cost_usd__sum"] or 0.0
        avg_cost = base_spend.aggregate(Avg("cost_usd"))["cost_usd__avg"] or 0.0
        model_spend = base_spend.values("model_id").annotate(total=Sum("cost_usd")).order_by("-total")
        efficiency = base_spend.values("model_id").annotate(avg_tokens=Avg("input_tokens") + Avg("output_tokens")).order_by("-avg_tokens")
        
        context.update({
            "total_spend": total_spend, 
            "avg_cost": avg_cost, 
            "model_spend": list(model_spend),
            "efficiency": list(efficiency),
        })
        
    return render(request, "discovery/cognitive_analytics.html", context)

@login_required
def subscription_view(request):
    """View to show user tier and limits."""
    # Ensure a local profile exists
    subscription = getattr(request.user, 'subscription', None)
    if not subscription:
        # Fallback to default tier if missing
        settings = SystemSettings.get_settings()
        subscription = UserSubscription.objects.create(
            user=request.user,
            tier=settings.default_tier
        )

    if request.method == "POST":
        tier_id = request.POST.get('tier_id')
        if tier_id:
            new_tier = get_object_or_404(Tier, pk=tier_id)
            if new_tier.price == 0:
                # If they are on a paid plan, we should ideally cancel it in Stripe
                # For now, let's just update the local tier
                subscription.tier = new_tier
                subscription.save()
                messages.success(request, f"Operational capacity transitioned to {new_tier.name}.")
                return redirect('discovery:subscription')

    # Get available tiers for upgrade/downgrade (exclude internal tiers)
    available_tiers = Tier.objects.exclude(name="Staff").order_by('price')
    
    context = {
        "subscription": subscription,
        "tier": subscription.tier,
        "available_tiers": available_tiers,
        "system_settings": SystemSettings.get_settings(),
        "usage_percentage": min(int((subscription.monthly_inquiries_consumed / subscription.tier.inquiry_limit) * 100), 100) if subscription.tier.inquiry_limit > 0 else 0
    }
    return render(request, "discovery/subscription.html", context)

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import gettext_lazy as _

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text=_("Required for account recovery and notifications."))

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Initialize default subscription using system settings if available
            settings = SystemSettings.get_settings()
            
            if settings.default_tier:
                target_tier = settings.default_tier
            else:
                target_tier, _ = Tier.objects.get_or_create(name="Free", defaults={
                    "inquiry_limit": 5,
                    "spend_limit": 10.00,
                    "price": 0.00
                })
            
            UserSubscription.objects.get_or_create(user=user, tier=target_tier)
            
            # Send verification email asynchronously
            from .email_service import EmailService
            try:
                EmailService.send_verification_email(user)
                messages.info(request, "A verification email has been sent. Please check your inbox.")
            except Exception as e:
                import logging
                logging.error(f"Failed to send verification email: {e}")
                messages.warning(request, "Unable to send verification email at this time.")

            login(request, user)
            return redirect('discovery:system_map')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.is_verified = True
        user.verification_token = ""
        user.save()
        messages.success(request, "Account verified! You now have full access.")
        if request.user.is_authenticated:
            return redirect('discovery:system_map')
        return redirect('login')
    except User.DoesNotExist:
        messages.error(request, "Invalid or expired verification link.")
        return redirect('discovery:system_map')

@login_required
def resend_verification(request):
    if request.user.is_verified:
        messages.info(request, "Your account is already verified.")
        return redirect('discovery:system_map')
    
    from .email_service import EmailService
    try:
        EmailService.send_verification_email(request.user)
        messages.success(request, "A new verification email has been sent.")
    except Exception as e:
        messages.error(request, "Failed to send email. Please check integration settings.")
    
    return redirect('discovery:system_map')

@login_required
def financial_intelligence_view(request):
    """
    SaaS-style Financial Intelligence Dashboard.
    Primary source for Profit, MRR, and AI Spend analytics.
    """
    if not request.user.is_superuser and request.user.subscription.user_type != 'ADMIN':
        messages.error(request, "Sovereign Denial: Unauthorized to view Financial Intelligence.")
        return redirect("discovery:system_map")

    summary = FinancialAnalyticsService.get_executive_summary()
    costs = FinancialAnalyticsService.get_cost_analytics()
    
    # Get last 30 snapshots for charts
    snapshots = DailyFinancialSnapshot.objects.order_by('-date')[:30]
    
    context = {
        "summary": summary,
        "costs": costs,
        "snapshots": list(reversed(snapshots)),
        "recent_transactions": FinancialTransaction.objects.all()[:15],
        "active_alerts": BusinessAlert.objects.filter(is_resolved=False)
    }
    
    return render(request, "discovery/financial_dashboard.html", context)

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    """Dashboard view for superusers to see all system inquiries."""
    settings = SystemSettings.get_settings()
    
    if request.method == "POST" and "toggle_spending" in request.POST:
        settings.show_spending_overview = request.POST.get("show_spending_overview") == "on"
        settings.save()
        messages.success(request, f"Spending overview is now {'visible' if settings.show_spending_overview else 'hidden'} for users.")
        return_to = request.POST.get("return_to")
        if return_to == "users_list":
            return redirect("discovery:users_list")
        return redirect("discovery:admin_dashboard")

    all_inquiries = Inquiry.objects.all().order_by("-updated_at")
    
    # Simple summary stats
    stats = {
        'total_inquiries': all_inquiries.count(),
        'completed': all_inquiries.filter(status='COMPLETED').count(),
        'failed': all_inquiries.filter(status='FAILED').count(),
        'refused': all_inquiries.filter(status='REFUSED').count(),
        'deleted': all_inquiries.filter(status='DELETED').count(),
        'running': all_inquiries.filter(status='RUNNING').count(),
        'total_spend': SpendRecord.objects.aggregate(Sum('cost_usd'))['cost_usd__sum'] or 0
    }
    
    return render(request, 'discovery/admin_dashboard.html', {
        'inquiries': all_inquiries,
        'stats': stats,
        'tiers': Tier.objects.all(),
        'system_settings': settings
    })

@admin_access_required()
def admin_heal_engine(request):
    """
    Emergency admin action to clear stuck engine processes.
    Marks inquiries in transitionary states that haven't been updated for 10m as FAILED.
    """
    from django.utils import timezone
    from datetime import timedelta
    
    threshold = timezone.now() - timedelta(minutes=10)
    stuck_inqs = Inquiry.objects.filter(
        status__in=['RUNNING', 'PENDING'],
        updated_at__lt=threshold
    )
    
    count = stuck_inqs.count()
    if count > 0:
        for inq in stuck_inqs:
            inq.status = 'FAILED'
            inq.current_status_msg = "Force terminated by administrative override."
            inq.save()
        
        messages.success(request, f"Engine Recovery Complete: {count} stuck process(es) terminated.")
    else:
        messages.info(request, "No stuck processes identified (Threshold: 10 minutes).")
        
    return redirect("discovery:admin_dashboard")

@admin_access_required('can_manage_inquiries')
def update_inquiry_status(request, pk):
    """Update inquiry status. Supports HTMX or redirect."""
    inquiry = get_object_or_404(Inquiry, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        valid_statuses = [c[0] for c in Inquiry.status.field.choices]
        
        if new_status in valid_statuses:
            inquiry.status = new_status
            inquiry.save()
            messages.success(request, f"Inquiry {inquiry.case_id} status updated to {new_status}.")
        else:
            messages.error(request, f"Invalid status: {new_status}")
            
    return redirect("discovery:admin_dashboard")

@user_passes_test(lambda u: u.is_superuser)
def admin_limits_config(request):
    """View to manage global system limits and governance settings. Restricted to Superusers."""
    settings = SystemSettings.get_settings()
    
    if request.method == "POST":
        settings.reasoning_depth = request.POST.get("reasoning_depth", 7)
        settings.strict_governance = request.POST.get("strict_governance") == "on"
        settings.show_spending_overview = request.POST.get("show_spending_overview") == "on"
        settings.save()

        messages.success(request, "Global limits and governance protocols updated.")
        return redirect('discovery:admin_limits_config')
        
    return render(request, 'discovery/admin_limits_config.html', {
        'settings': settings
    })

@user_passes_test(lambda u: u.is_superuser)
def admin_system_reset(request):
    """
    Destructive admin action to clear specific or all database entries.
    ONLY accessible to Superusers. Protects all Admin level accounts.
    """
    if request.method != "POST":
        return redirect("discovery:admin_limits_config")
        
    reset_users = request.POST.get("reset_users") == "on"
    reset_inquiries = request.POST.get("reset_inquiries") == "on"
    reset_spend = request.POST.get("reset_spend") == "on"
    reset_everything = request.POST.get("reset_everything") == "on"
    
    deleted_counts = {}
    
    try:
        if reset_everything:
            # Most destructive - everything but admin accounts and settings
            from .models import Inquiry, Planet, ExplorationBranch, EngineRun, RoomState, SpendRecord, IssueReport, UserSubscription, Notification
            from django.contrib.auth.models import User
            from django.db.models import Q
            
            deleted_counts['Inquiries'] = Inquiry.objects.all().delete()[0]
            deleted_counts['Planets'] = Planet.objects.all().delete()[0]
            deleted_counts['Explorations'] = ExplorationBranch.objects.all().delete()[0]
            deleted_counts['Engine Runs'] = EngineRun.objects.all().delete()[0]
            deleted_counts['Room States'] = RoomState.objects.all().delete()[0]
            deleted_counts['Spend Records'] = SpendRecord.objects.all().delete()[0]
            deleted_counts['Issue Reports'] = IssueReport.objects.all().delete()[0]
            deleted_counts['Notifications'] = Notification.objects.all().delete()[0]
            
            # Reset subscription usage for remaining users
            UserSubscription.objects.update(
                total_inquiries_consumed=0,
                monthly_inquiries_consumed=0,
                monthly_spend_consumed=0.0
            )
            
            # Delete non-admin users (Protect superusers and Limited Admins)
            users_to_del = User.objects.filter(
                is_superuser=False, 
                is_staff=False
            ).exclude(subscription__user_type='ADMIN')
            
            deleted_counts['Users'] = users_to_del.count()
            users_to_del.delete()
            
            messages.warning(request, f"Full System Reset Complete. Data cleared: {deleted_counts}")
            
        else:
            if reset_inquiries:
                from .models import Inquiry
                count = Inquiry.objects.all().delete()[0]
                deleted_counts['Inquiries'] = count
                
            if reset_spend:
                from .models import SpendRecord, UserSubscription
                count = SpendRecord.objects.all().delete()[0]
                deleted_counts['Spend Records'] = count
                UserSubscription.objects.update(monthly_spend_consumed=0.0)
                
            if reset_users:
                from django.contrib.auth.models import User
                # Delete non-admin users (Protect superusers and Limited Admins)
                users_to_del = User.objects.filter(
                    is_superuser=False, 
                    is_staff=False
                ).exclude(subscription__user_type='ADMIN')
                
                count = users_to_del.count()
                users_to_del.delete()
                deleted_counts['Users'] = count
                
            if deleted_counts:
                messages.warning(request, f"Selective Reset Complete. Data cleared: {deleted_counts}")
            else:
                messages.info(request, "No reset options were selected.")
                
    except Exception as e:
        messages.error(request, f"System Reset Failed: {str(e)}")
        
    return redirect(request.META.get('HTTP_REFERER', 'discovery:admin_limits_config'))


def tier_list(request):
    """View to list all available membership tiers."""
    tiers = Tier.objects.all().order_by('price')
    settings = SystemSettings.get_settings()

    if request.method == "POST":
        default_tier_id = request.POST.get("default_tier_id")
        if default_tier_id:
            settings.default_tier = Tier.objects.get(pk=default_tier_id)
            settings.save()
            messages.success(request, f"Default tier updated to {settings.default_tier.name}.")
            return redirect('discovery:tier_list')

    return render(request, 'discovery/tier_list.html', {
        'tiers': tiers,
        'default_tier': settings.default_tier
    })

@admin_access_required('can_manage_users')
def users_list(request):
    """View to list all users, their current tier usage, and spendage. Now handles user creation."""
    from django.contrib.auth.models import User
    from django.db.models import Q
    
    query = request.GET.get('q', '')
    users = User.objects.filter(is_superuser=False).prefetch_related('subscription', 'subscription__tier')
    
    # Initialize form
    signup_form = SignupForm()
    
    if request.method == 'POST' and 'create_user' in request.POST:
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            # Initialize default subscription using system settings
            settings = SystemSettings.get_settings()
            
            if settings.default_tier:
                target_tier = settings.default_tier
            else:
                target_tier, _ = Tier.objects.get_or_create(name="Free", defaults={
                    "inquiry_limit": 5,
                    "spend_limit": 10.00,
                    "price": 0.00
                })
            
            UserSubscription.objects.get_or_create(user=user, tier=target_tier)
            messages.success(request, f"Sovereign user '{user.username}' successfully registered in the archive.")
            return redirect('discovery:users_list')
        else:
            # Re-open modal script trigger could go here, but messages are usually enough
            for field, errors in signup_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    # Simple summary stats for the user list header
    user_data = []
    active_count = 0
    for user in users:
        if user.is_active:
            active_count += 1
        sub = getattr(user, 'subscription', None)
        user_data.append({
            'user': user,
            'subscription': sub,
            'is_active': user.is_active,
            'last_login': user.last_login,
            'date_joined': user.date_joined,
        })

    return render(request, 'discovery/users_list.html', {
        'users_data': user_data,
        'active_count': active_count,
        'total_count': users.count(),
        'search_query': query,
        'signup_form': signup_form
    })

@admin_access_required('can_manage_users')
def toggle_user_status(request, user_id):
    """Toggle the is_active status of a user."""
    from django.contrib.auth.models import User
    target_user = get_object_or_404(User, pk=user_id)
    if target_user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
    else:
        target_user.is_active = not target_user.is_active
        target_user.save()
        status = "activated" if target_user.is_active else "deactivated"
        messages.success(request, f"User {target_user.username} has been {status}.")
    return redirect('discovery:users_list')

@admin_access_required('can_manage_users')
def delete_user(request, user_id):
    """Permanently delete a user and their associated data."""
    from django.contrib.auth.models import User
    target_user = get_object_or_404(User, pk=user_id)
    
    if target_user == request.user:
        messages.error(request, "Sovereign Alert: You cannot terminate your own administrative identity.")
    else:
        username = target_user.username
        target_user.delete()
        messages.success(request, f"Identity Purge: User '{username}' and all associated cognitive records have been removed.")
    
    return redirect('discovery:users_list')

@admin_access_required('can_manage_users')
def manual_reset_usage(request, user_id):
    """Manually reset the monthly usage and billing cycle for a user."""
    from django.contrib.auth.models import User
    from django.utils import timezone
    target_user = get_object_or_404(User, pk=user_id)
    sub = getattr(target_user, 'subscription', None)
    if sub:
        sub.monthly_inquiries_consumed = 0
        sub.monthly_spend_consumed = 0.0
        sub.billing_start_date = timezone.now()
        sub.save()

        from .models import Notification
        Notification.objects.create(
            user=target_user,
            title="Manual Usage Reset",
            message="An administrator has manually reset your usage limits. Your monthly cycle starts fresh today.",
            category='USAGE_RESET'
        )
        messages.success(request, f"Usage limits reset for {target_user.username}. A new billing cycle starts today.")
    else:
        messages.error(request, f"User {target_user.username} has no active subscription profile.")
    return redirect('discovery:users_list')

@admin_access_required('can_manage_users')
def user_detail(request, user_id):
    """View to see detailed charts and activity for a specific user."""
    from django.contrib.auth.models import User
    target_user = get_object_or_404(User, pk=user_id)
    subscription = getattr(target_user, 'subscription', None)
    
    # Calculate more detailed stats
    inquiries = Inquiry.objects.filter(user=target_user).order_by('-created_at')
    spend_records = SpendRecord.objects.filter(inquiry__user=target_user).order_by('-timestamp')
    tiers = Tier.objects.all()
    
    # Calculate 30-day activity
    from datetime import timedelta
    from django.utils import timezone
    today = timezone.now().date()
    daily_activity = []
    
    # Get counts grouped by day for the last 30 days
    thirty_days_ago = today - timedelta(days=29)
    activity_qs = Inquiry.objects.filter(
        user=target_user, 
        created_at__date__gte=thirty_days_ago
    ).values('created_at__date').annotate(count=Count('id')).order_by('created_at__date')
    
    activity_map = {item['created_at__date']: item['count'] for item in activity_qs}
    
    for i in range(30):
        day = thirty_days_ago + timedelta(days=i)
        count = activity_map.get(day, 0)
        daily_activity.append({
            'label': day.strftime("%b %d"),
            'count': count,
        })
        
    max_count = max([d['count'] for d in daily_activity]) if daily_activity else 0
    for day in daily_activity:
        # Use a minimum height of 2 for visibility on the chart
        day['height'] = max(2, (day['count'] / max_count * 100)) if max_count > 0 else 2

    if request.method == "POST":
        # Handle admin permissions toggle
        if "update_admin_permissions" in request.POST and request.user.is_superuser:
            perm_key = request.POST.get("perm_key")
            is_enabled = request.POST.get("is_enabled") == "on"
            
            if subscription:
                perms = subscription.admin_permissions.copy()
                perms[perm_key] = is_enabled
                subscription.admin_permissions = perms
                subscription.save()
                messages.success(request, f"Permission '{perm_key}' updated for {target_user.username}.")
            return redirect('discovery:user_detail', user_id=user_id)

        # Handle account status updates
        if "update_account" in request.POST:
            email = request.POST.get("email")
            is_active = request.POST.get("is_active") == "on"
            target_user.email = email
            target_user.is_active = is_active
            target_user.save()
            messages.success(request, f"Account for {target_user.username} updated.")
            return redirect('discovery:user_detail', user_id=user_id)
        
        # Handle access/role updates
        if "update_access" in request.POST:
            user_type = request.POST.get("user_type")
            tier_id = request.POST.get("tier_id")
            if subscription:
                subscription.user_type = user_type
                
                # Role-Specific Tier Handling
                if user_type == "NORMAL":
                    if tier_id:
                        try:
                            subscription.tier = Tier.objects.get(pk=tier_id)
                        except Tier.DoesNotExist:
                            pass
                elif user_type == "ADMIN":
                    admin_tier, _ = Tier.objects.get_or_create(
                        name="Staff",
                        defaults={"inquiry_limit": 0, "spend_limit": 0.00, "price": 0.00}
                    )
                    subscription.tier = admin_tier

                # Update permissions JSON if role is ADMIN
                if user_type == "ADMIN":
                    new_perms = {
                        "can_view_stats": request.POST.get("perm_can_view_stats") == "on",
                        "can_manage_inquiries": request.POST.get("perm_can_manage_inquiries") == "on",
                        "can_manage_users": request.POST.get("perm_can_manage_users") == "on",
                        "can_view_spend": request.POST.get("perm_can_view_spend") == "on",
                        "can_manage_issues": request.POST.get("perm_can_manage_issues") == "on",
                        "can_edit_settings": request.POST.get("perm_can_manage_settings") == "on",
                        "can_manage_tiers": request.POST.get("perm_can_manage_tiers") == "on",
                        "can_view_analytics": request.POST.get("perm_can_view_analytics") == "on",
                    }
                    subscription.admin_permissions = new_perms
                else:
                    subscription.admin_permissions = {} # Clear if not admin
                
                subscription.save()
                messages.success(request, f"Access protocols for {target_user.username} recalibrated.")
            return redirect('discovery:user_detail', user_id=user_id)

    return render(request, 'discovery/user_detail.html', {
        'target_user': target_user,
        'subscription': subscription,
        'inquiries': inquiries,
        'spend_records': spend_records,
        'tiers': tiers,
        'daily_activity': daily_activity
    })

@admin_access_required('can_manage_tiers')
def tier_upsert(request, pk=None):
    """View to create or update a tier."""
    tier = get_object_or_404(Tier, pk=pk) if pk else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        inquiry_limit = request.POST.get('inquiry_limit')
        spend_limit = request.POST.get('spend_limit')
        price = request.POST.get('price')
        is_recommended = request.POST.get('is_recommended') == 'on'
        stripe_product_id = request.POST.get('stripe_product_id')
        stripe_price_id = request.POST.get('stripe_price_id')
        
        if tier:
            tier.name = name
            tier.inquiry_limit = inquiry_limit
            tier.spend_limit = spend_limit
            tier.price = price
            tier.is_recommended = is_recommended
            tier.stripe_product_id = stripe_product_id
            tier.stripe_price_id = stripe_price_id
            tier.save()
            messages.success(request, f"Tier '{name}' updated successfully.")
        else:
            Tier.objects.create(
                name=name,
                inquiry_limit=inquiry_limit,
                spend_limit=spend_limit,
                price=price,
                is_recommended=is_recommended,
                stripe_product_id=stripe_product_id,
                stripe_price_id=stripe_price_id
            )
            messages.success(request, f"Tier '{name}' created successfully.")
        return redirect('discovery:tier_list')
        
    return render(request, 'discovery/tier_form.html', {'tier': tier})

@admin_access_required('can_manage_tiers')
def tier_delete(request, pk):
    """View to delete a tier."""
    tier = get_object_or_404(Tier, pk=pk)
    # Check if any user is using this tier
    if UserSubscription.objects.filter(tier=tier).exists():
        messages.error(request, f"Cannot delete '{tier.name}': It is currently active for some users.")
    else:
        name = tier.name
        tier.delete()
        messages.success(request, f"Tier '{name}' has been deleted.")
    return redirect('discovery:tier_list')

@login_required
def report_issue(request):
    """Handle floating button issue reports."""
    if request.method == "POST":
        description = request.POST.get("description")
        screenshot = request.POST.get("screenshot")
        url = request.POST.get("url")
        
        if description:
            IssueReport.objects.create(
                user=request.user,
                description=description,
                screenshot=screenshot or "",
                url=url or ""
            )
            return JsonResponse({"status": "success", "message": "Issue reported successfully."})
        return JsonResponse({"status": "error", "message": "Description is required."}, status=400)
    return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)

@admin_access_required('can_manage_issues')
def admin_issue_center(request):
    """Admin view to manage all reported issues and platform verification."""
    issues = IssueReport.objects.all().order_by("-created_at")
    active_count = issues.exclude(status='FIXED').count()
    
    # Platform Verification Tests
    test_runs = SystemTestRun.objects.all().order_by("-created_at")[:20]
    
    # Calculate Global Health Score (avg of last 5 unique category runs)
    from django.db.models import Avg
    recent_health = SystemTestRun.objects.filter(status='COMPLETED').values('category').annotate(avg_score=Avg('health_score')).order_by('-created_at')[:5]
    global_score = sum(item['avg_score'] for item in recent_health) / len(recent_health) if recent_health else 0
    
    # Calculate SVG offset for health ring (dasharray 440)
    # 440 - (440 * score / 100)
    health_offset = 440 - (440 * (global_score / 100))

    context = {
        "issues": issues,
        "active_count": active_count,
        "test_runs": test_runs,
        "global_score": int(global_score),
        "health_offset": int(health_offset),
        "categories": SystemTestRun.CATEGORY_CHOICES
    }

    if request.headers.get('HX-Request') and request.GET.get('partial') == 'status':
        return render(request, "discovery/partials/admin_validation_status.html", context)

    if request.headers.get('HX-Request') and request.GET.get('partial') == 'logs':
        return render(request, "discovery/partials/admin_verification_logs.html", context)

    return render(request, "discovery/admin_issues.html", context)

@admin_access_required('can_manage_issues')
def trigger_system_test(request):
    """Trigger a new platform verification cycle."""
    if request.method == "POST":
        category = request.POST.get("category", "CORE")
        test_type = request.POST.get("test_type", "STANDARD")
        
        run = SystemTestRun.objects.create(
            category=category,
            test_type=test_type,
            status="RUNNING"
        )
        
        run_system_tests_async(run.id)
        
        if request.headers.get('HX-Request'):
            # Return nothing or a small signal, the polling will handle the UI update
            return HttpResponse(status=204)
            
        messages.success(request, f"Verification Cycle [{category}] initialized in background.")
        return redirect("discovery:admin_issue_center")
    return redirect("discovery:admin_issue_center")

@admin_access_required('can_manage_issues')
def get_test_report(request, run_id):
    """Return JSON details for a specific test run."""
    run = get_object_or_404(SystemTestRun, pk=run_id)
    return JsonResponse({
        "id": run.id,
        "status": run.status,
        "health_score": run.health_score,
        "results": run.results,
        "logs": run.logs,
        "execution_time": f"{run.execution_time:.2f}s",
        "created_at": run.created_at.strftime("%Y-%m-%d %H:%M:%S")
    })

@login_required
def user_issues(request):
    """User view to see their own issues."""
    issues = IssueReport.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "discovery/user_issues.html", {"issues": issues})

@admin_access_required('can_manage_issues')
def update_issue_status(request, issue_id):
    """Update status or admin note for an issue."""
    issue = get_object_or_404(IssueReport, pk=issue_id)
    if request.method == "POST":
        status = request.POST.get("status")
        admin_note = request.POST.get("admin_note")
        if status:
            issue.status = status
        if admin_note is not None:
            issue.admin_note = admin_note
        issue.save()
        
        # Support HTMX partial updates for row interactivity
        if request.headers.get("HX-Request"):
            return render(request, "discovery/partials/issue_row.html", {"issue": issue})
            
        messages.success(request, f"Issue #{issue.id} updated.")
    return redirect("discovery:admin_issue_center")

@login_required
def get_notifications(request):
    """Retrieve recent notifications for the user, with unread count."""
    from .models import Notification
    # Show last 10 notifications total
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:10]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    return render(request, 'discovery/partials/notifications_dropdown.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def mark_notification_read(request, pk):
    """Mark a specific notification as read and redirect or return success."""
    from .models import Notification
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('HX-Request'):
        return get_notifications(request)
        
    if notification.link:
        return redirect(notification.link)
    return redirect('discovery:system_map')

@login_required
def clear_all_notifications(request):
    """Mark all notifications for the user as read."""
    from .models import Notification
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    if request.headers.get('HX-Request'):
        return get_notifications(request)
    return redirect('discovery:system_map')

@login_required
def export_inquiry(request, pk, format):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    
    # Check authorization
    if not _check_auth(request, inquiry):
        messages.error(request, 'Sovereign Denial: Unauthorized export attempt.')
        return redirect('discovery:system_map')

    if format != 'pdf':
        messages.error(request, 'Sovereign Constraint: Only PDF export is authorized at this stage.')
        return redirect('discovery:room_view', pk=pk, room_type='DISCOVERY')

    data = collect_inquiry_report_data(inquiry)
    # Providing a Print-Ready HTML page as a fallback that behaves like a professional report.
    return render(request, 'discovery/reports/inquiry_report_pdf.html', data)

@login_required
@require_POST
def create_stripe_checkout(request, tier_id):
    """Initialize a Stripe Checkout session for a tier."""
    success_url = request.build_absolute_uri(reverse('discovery:stripe_success'))
    cancel_url = request.build_absolute_uri(reverse('discovery:stripe_cancel'))
    
    try:
        session = create_checkout_session(request.user, tier_id, success_url, cancel_url)
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f'Checkout Error: {str(e)}')
        return redirect('discovery:subscription')

@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Process incoming Stripe webhooks."""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    success, message = handle_webhook_event(payload, sig_header)
    
    if success:
        return HttpResponse(status=200)
    else:
        logger.error(f'Webhook handling failed: {message}')
        return HttpResponse(content=message, status=400)

@login_required
def stripe_success(request):
    """Return page after successful checkout."""
    session_id = request.GET.get('session_id')
    if session_id:
        messages.success(request, 'Payment successful! Your subscription is being activated.')
    return redirect('discovery:subscription')

@login_required
def stripe_cancel(request):
    """Return page after cancelled checkout."""
    messages.info(request, 'Checkout cancelled. No charges were made.')
    return redirect('discovery:subscription')

@login_required
def stripe_customer_portal(request):
    """Redirect to Stripe Customer Portal for subscription management."""
    stripe_client = get_stripe_client()
    if not stripe_client:
        messages.error(request, 'Stripe is not configured.')
        return redirect('discovery:subscription')
        
    subscription = getattr(request.user, 'subscription', None)
    if not subscription or not subscription.stripe_customer_id:
        messages.error(request, 'You do not have an active billing profile.')
        return redirect('discovery:subscription')
        
    try:
        import stripe
        settings = SystemSettings.get_settings()
        stripe.api_key = settings.stripe_secret_key
        return_url = request.build_absolute_uri(reverse('discovery:subscription'))
        session = stripe_client.billing_portal.Session.create(
            customer=subscription.stripe_customer_id,
            return_url=return_url,
        )
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f'Portal Error: {str(e)}')
        return redirect('discovery:subscription')


