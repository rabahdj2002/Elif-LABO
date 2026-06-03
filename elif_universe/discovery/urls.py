from django.urls import path
from . import views

app_name = 'discovery'

urlpatterns = [
    path('', views.system_map, name='system_map'),
    path('initialize/', views.initialize_inquiry, name='initialize'),
    path('inquiry/<pk>/', views.inquiry_detail, name='inquiry_detail'),
    path('inquiry/<pk>/room/<str:room_type>/', views.room_view, name='room_view'),
    path('inquiry/<pk>/sync/', views.sync_engine_pulse, name='sync_engine'),
    path('inquiry/<pk>/refine/', views.refine_inquiry, name='refine_inquiry'),
    path('inquiry/<pk>/reset/', views.reset_inquiry, name='reset'),
    path('inquiry/<pk>/delete/', views.delete_inquiry, name='delete'),
    path('settings/', views.system_settings_view, name='settings'),
]
