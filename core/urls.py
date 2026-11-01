from django.urls import path

from .views import add_fertilizer_schedule, contact, crop_health, crop_management, dashboard, delete_fertilizer_schedule, home, log_crop_activity, mark_fertilizer_applied, profile_settings, recommendations, sensor_entry

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('crops/', crop_management, name='crops'),
    path('crops/<int:crop_id>/activities/', log_crop_activity, name='log-crop-activity'),
    path('crops/<int:crop_id>/fertilizer-schedules/', add_fertilizer_schedule, name='add-fertilizer-schedule'),
    path('fertilizer-schedules/<int:schedule_id>/applied/', mark_fertilizer_applied, name='mark-fertilizer-applied'),
    path('fertilizer-schedules/<int:schedule_id>/delete/', delete_fertilizer_schedule, name='delete-fertilizer-schedule'),
    path('profile/', profile_settings, name='profile'),
    path('sensor-entry/', sensor_entry, name='sensor-entry'),
    path('crop-health/', crop_health, name='crop-health'),
    path('recommendations/', recommendations, name='recommendations'),
    path('contact/', contact, name='contact'),
]
