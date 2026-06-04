from django.urls import path
from . import views

app_name = 'discovery'

urlpatterns = [
    path('', views.system_map, name='system_map'),
    path('initialize/', views.initialize_inquiry, name='initialize'),
    path('inquiry/<pk>/', views.inquiry_detail, name='inquiry_detail'),
    path('inquiry/<pk>/room/<str:room_type>/', views.room_view, name='room_view'),
    path('inquiry/<pk>/sync/', views.sync_engine_pulse, name='sync_engine'),
    path('inquiry/<pk>/branch/', views.spawn_branch_view, name='spawn_branch'),
    path('inquiry/<pk>/refine/', views.refine_inquiry, name='refine_inquiry'),
    path('inquiry/<pk>/reset/', views.reset_inquiry, name='reset'),
    path('inquiry/<pk>/delete/', views.delete_inquiry, name='delete'),
    path('inquiry/<pk>/telemetry/', views.engine_telemetry, name='telemetry'),
    path('inquiry/<pk>/events/', views.engine_events, name='engine_events'),
    path('settings/', views.system_settings_view, name='settings'),
    path('settings/clear-lock/', views.clear_engine_lock, name='clear_lock'),
    path('spend/', views.spend_history, name='spend_history'),
    path('documentation/', views.documentation_view, name='documentation'),
    path('topic/<str:topic_name>/', views.topic_detail, name='topic_detail'),
    path('task/<str:task_id>/status/', views.task_status_view, name='task_status'),
]
