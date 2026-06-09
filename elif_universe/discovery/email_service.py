import logging
from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .settings_models import SystemSettings
from .models import EmailLog

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_mail(subject, message, recipient_list, html_content=None, from_email=None):
        """
        Dynamically sends email using SMTP settings stored in the database.
        Uses Django's email backend connection for production-grade reliability.
        """
        sys_settings = SystemSettings.objects.first()
        if not sys_settings:
            logger.error("SystemSettings not found. Cannot send email.")
            return False, "SystemSettings missing."
            
        # Fallback logic for credentials
        host = sys_settings.smtp_host or getattr(settings, 'EMAIL_HOST', 'localhost')
        port = sys_settings.smtp_port or getattr(settings, 'EMAIL_PORT', 587)
        user = sys_settings.smtp_user or getattr(settings, 'EMAIL_HOST_USER', '')
        password = sys_settings.smtp_pass
        use_tls = sys_settings.smtp_use_tls
        use_ssl = sys_settings.smtp_use_ssl
        from_email_addr = from_email or sys_settings.email_from_address or getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@elif.ai')
        from_name = sys_settings.email_from_name or "ELIF Engine"

        full_from = f"{from_name} <{from_email_addr}>"

        try:
            # Create a dynamic connection
            connection = get_connection(
                host=host,
                port=port,
                username=user,
                password=password,
                use_tls=use_tls,
                use_ssl=use_ssl,
                timeout=10
            )

            text_content = strip_tags(html_content) if html_content else message

            msg = EmailMultiAlternatives(
                subject, 
                text_content, 
                full_from, 
                recipient_list,
                connection=connection
            )
            
            if html_content:
                msg.attach_alternative(html_content, "text/html")

            msg.send()

            # Log success
            for recipient in recipient_list:
                EmailLog.objects.create(
                    recipient=recipient,
                    subject=subject,
                    status='SENT'
                )
            
            return True, "Email sent successfully."

        except Exception as e:
            logger.error(f"SMTP Delivery Failure: {str(e)}")
            # Log failure
            for recipient in recipient_list:
                EmailLog.objects.create(
                    recipient=recipient,
                    subject=subject,
                    status='FAILED',
                    error_log=str(e)
                )
            return False, str(e)

    @staticmethod
    def dispatch_alert(subject, message, alert_type="ANOMALY"):
        """
        High-priority system alert dispatcher.
        """
        sys_settings = SystemSettings.get_settings()
        if not sys_settings or not sys_settings.admin_alert_email:
            logger.warning("No admin alert email configured. Skipping alert.")
            return

        full_subject = f"[{alert_type}] {subject}"
        
        try:
            html_content = render_to_string('discovery/emails/system_alert.html', {
                'subject': subject,
                'message': message,
                'alert_type': alert_type,
                'project_name': 'ELIF Platform'
            })
        except Exception as e:
            logger.error(f"Template rendering failed for alert: {e}")
            html_content = None

        return EmailService.send_mail(
            subject=full_subject,
            message=message,
            recipient_list=[sys_settings.admin_alert_email],
            html_content=html_content
        )

    @staticmethod
    def send_verification_email(user):
        """Dispatches a signed verification link to a new user."""
        import uuid
        sub = user.subscription
        if not sub.verification_token:
            sub.verification_token = str(uuid.uuid4())
            sub.token_expires_at = timezone.now() + timezone.timedelta(hours=24)
            sub.save()

        verify_url = f"/discovery/verify-email/{sub.verification_token}/"
        subject = "ELIF Protocol: Verification Required"
        message = f"Please verify your account by clicking the link: {verify_url}"
        
        # HTML Content for verification
        html_content = f"""
        <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #1e293b; border-radius: 12px; background-color: #0f172a; color: #f8fafc;">
            <h2 style="color: #3b82f6; text-transform: uppercase; letter-spacing: 0.1em;">Verification Required</h2>
            <p style="font-size: 14px; line-height: 1.6; color: #94a3b8;">
                Your account on the ELIF Substrate has been created. To proceed with inquiry initialization and cognitive mapping, you must verify your communication channel.
            </p>
            <div style="margin: 30px 0; text-align: center;">
                <a href="{verify_url}" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; text-transform: uppercase; font-size: 12px; letter-spacing: 0.1em;">
                    Authorize Substrate Access
                </a>
            </div>
            <p style="font-size: 11px; color: #64748b; font-style: italic;">
                "Veritas per Verificationem." — This link expires in 24 hours.
            </p>
        </div>
        """
        
        return EmailService.send_mail(
            subject=subject, 
            message=message, 
            recipient_list=[user.email], 
            html_content=html_content
        )

