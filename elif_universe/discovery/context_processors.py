from .models import SystemSettings

def system_settings(request):
    """
    Available in all templates as 'system_settings'.
    """
    return {
        'system_settings': SystemSettings.get_settings()
    }
