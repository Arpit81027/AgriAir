from datetime import timedelta
from pathlib import PurePath
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone


SOIL_TYPE_CHOICES = [
    ('alluvial', 'Alluvial'),
    ('black', 'Black (Regur)'),
    ('red_yellow', 'Red and yellow'),
    ('laterite', 'Laterite'),
    ('arid', 'Arid / desert'),
    ('mountain', 'Mountain / forest'),
    ('saline', 'Saline / alkaline'),
    ('peaty', 'Peaty / marshy'),
    ('other', 'Other / not sure'),
]


def crop_image_upload_to(instance, filename):
    extension = PurePath(filename).suffix.lower()
    return f'crop_photos/{instance.user_id}/{uuid4().hex}{extension}'


class FarmerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_name = models.CharField(max_length=150)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPE_CHOICES, blank=True)
    crop_type = models.CharField(max_length=100, default='Wheat')
    acreage = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.farm_name


class SensorReading(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sensor_readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    soil_moisture = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    rainfall = models.FloatField(default=0.0)
    irrigation_status = models.CharField(max_length=50, default='Low')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username} - {self.timestamp:%Y-%m-%d %H:%M}'


class FarmCrop(models.Model):
    CROP_CHOICES = [
        ('wheat', 'Wheat'),
        ('rice', 'Rice'),
        ('maize', 'Maize'),
        ('tomato', 'Tomato'),
        ('potato', 'Potato'),
        ('chickpea', 'Chickpea'),
        ('cotton', 'Cotton'),
        ('sugarcane', 'Sugarcane'),
        ('other', 'Other'),
    ]
    STAGE_CHOICES = [
        ('sowing', 'Sowing / planting'),
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative growth'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting / grain filling'),
        ('maturity', 'Maturity / harvest'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farm_crops')
    name = models.CharField(max_length=30, choices=CROP_CHOICES)
    image = models.ImageField(upload_to=crop_image_upload_to, blank=True)
    variety = models.CharField(max_length=100, blank=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='vegetative')
    planted_on = models.DateField(null=True, blank=True)
    area_acres = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_name_display()} - {self.user.username}'


class CropActivity(models.Model):
    ACTIVITY_CHOICES = [
        ('watering', 'Watering'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide / treatment'),
        ('observation', 'Field observation'),
    ]
    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('watch', 'Needs watching'),
        ('stressed', 'Stressed / unwell'),
        ('unknown', 'Not checked'),
    ]

    crop = models.ForeignKey(FarmCrop, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    completed = models.BooleanField(default=True)
    product_or_method = models.CharField(max_length=120, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=30, blank=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='unknown')
    notes = models.CharField(max_length=250, blank=True)
    recorded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f'{self.get_activity_type_display()} - {self.crop}'


class FertilizerSchedule(models.Model):
    UNIT_CHOICES = [
        ('kg', 'kg'),
        ('g', 'g'),
        ('L', 'L'),
        ('mL', 'mL'),
        ('bags', 'bags'),
    ]

    crop = models.ForeignKey(FarmCrop, on_delete=models.CASCADE, related_name='fertilizer_schedules')
    fertilizer_name = models.CharField(max_length=120)
    rate_per_acre = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    interval_days = models.PositiveSmallIntegerField()
    last_applied_on = models.DateField()
    advisory_source = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_applied_on', 'fertilizer_name']

    @property
    def next_due_on(self):
        return self.last_applied_on + timedelta(days=self.interval_days)

    @property
    def total_amount(self):
        if self.crop.area_acres is None:
            return None
        return self.rate_per_acre * self.crop.area_acres

    def __str__(self):
        return f'{self.fertilizer_name} for {self.crop}'
