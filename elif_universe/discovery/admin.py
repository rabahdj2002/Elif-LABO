from django.contrib import admin
from .models import Inquiry, Planet, RoomState, SpendRecord, Tier, UserSubscription, TesterSurveyResponse
from .settings_models import SystemSettings

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'active_model', 'show_spending_overview', 'updated_at')
    fieldsets = (
        ('Engine configuration', {
            'fields': ('active_model', 'anthropic_api_key', 'offline_mode', 'reasoning_depth', 'enable_web_search', 'strict_governance')
        }),
        ('User Experience', {
            'fields': ('linear_ui_mode', 'show_spending_overview', 'auto_refresh_ms', 'debug_mode', 'system_version')
        }),
        ('Documentation', {
            'fields': ('documentation_content',)
        }),
        ('Tester Protocol', {
            'fields': ('tester_free_inquiry_limit', 'tester_survey_schema')
        }),
        ('Commercial', {
            'fields': ('default_tier',)
        }),
    )

@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'inquiry_limit', 'spend_limit', 'price', 'is_recommended')
    list_editable = ('is_recommended',)
    search_fields = ('name',)
    fields = ('name', 'inquiry_limit', 'spend_limit', 'price', 'is_recommended')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'tier', 'inquiry_usage', 'spend_usage', 'billing_start_date')
    list_filter = ('user_type', 'tier', 'has_completed_survey')
    search_fields = ('user__username',)
    fields = ('user', 'user_type', 'tier', 'monthly_inquiries_consumed', 'total_inquiries_consumed', 'billing_start_date', 'has_completed_survey', 'admin_permissions')
    readonly_fields = ('billing_start_date',)

@admin.register(TesterSurveyResponse)
class TesterSurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_at')
    readonly_fields = ('user', 'answers', 'submitted_at')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('case_id', 'user', 'topic', 'status', 'created_at')
    list_filter = ('status', 'topic')
    search_fields = ('case_id', 'core_question', 'user__username')

@admin.register(SpendRecord)
class SpendRecordAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'inquiry', 'step_name', 'model_id', 'cost_usd')
    list_filter = ('model_id', 'step_name')

admin.site.register(Planet)
admin.site.register(RoomState)
