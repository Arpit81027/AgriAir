from django.contrib import admin

from .models import CropActivity, FarmCrop, FarmerProfile, FertilizerSchedule, SensorReading


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('farm_name', 'user', 'district', 'crop_type', 'acreage')
    search_fields = ('farm_name', 'district', 'crop_type', 'user__username')


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('user', 'soil_moisture', 'temperature', 'humidity', 'rainfall', 'timestamp')
    list_filter = ('irrigation_status',)
    search_fields = ('user__username', 'notes')


@admin.register(FarmCrop)
class FarmCropAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'stage', 'planted_on', 'area_acres')
    list_filter = ('name', 'stage')
    search_fields = ('user__username', 'variety', 'notes')


@admin.register(CropActivity)
class CropActivityAdmin(admin.ModelAdmin):
    list_display = ('crop', 'activity_type', 'completed', 'condition', 'quantity', 'unit', 'recorded_at')
    list_filter = ('activity_type', 'completed', 'condition')
    search_fields = ('crop__user__username', 'crop__variety', 'product_or_method', 'notes')


@admin.register(FertilizerSchedule)
class FertilizerScheduleAdmin(admin.ModelAdmin):
    list_display = ('fertilizer_name', 'crop', 'rate_per_acre', 'unit', 'interval_days', 'last_applied_on')
    list_filter = ('unit', 'interval_days')
    search_fields = ('fertilizer_name', 'crop__user__username', 'advisory_source')
