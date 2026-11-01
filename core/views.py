from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .crop_health import DISEASE_GUIDES, screen_crop_symptoms
from .fertilizer_recommendations import get_fertilizer_reference
from .forms import CropActivityForm, CropHealthForm, FarmCropForm, FarmerProfileForm, FertilizerScheduleForm, SensorReadingForm
from .models import CropActivity, FarmCrop, FarmerProfile, FertilizerSchedule, SensorReading
from .soil_suggestions import suggest_soil_type
from .weather import WeatherServiceError, get_local_weather


def crop_care_guidance(crop, latest_reading, weather, soil_type=''):
    if weather and weather['today_rain'] is not None and weather['today_rain'] >= 5:
        watering = (
            f"About {weather['today_rain']:.1f} mm rain is forecast today. Do not irrigate by calendar alone; "
            "check soil near the roots and reassess after the rain."
        )
    elif latest_reading:
        moisture = latest_reading.soil_moisture
        if moisture < 30:
            watering = (
                f"The latest field entry is {moisture:.0f}% soil moisture. Check the sensor calibration and "
                "root-zone soil; irrigate if the crop needs water. This generic percentage is not a universal threshold."
            )
        elif moisture < 50:
            watering = (
                f"The latest field entry is {moisture:.0f}% soil moisture. Check the root zone and crop stage "
                "today; irrigate only if the soil and crop indicate need."
            )
        else:
            watering = (
                f"The latest field entry is {moisture:.0f}% soil moisture. Check for waterlogging before "
                "irrigating; sensor scale and suitable moisture vary by soil and crop."
            )
    else:
        watering = (
            "No sensor reading is saved. Check soil moisture near active roots and the crop stage before "
            "watering; avoid a fixed calendar or overwatering."
        )

    crop_watering = {
        'wheat': 'Check soil at crown-root initiation, heading and grain filling; irrigate only when the root zone needs it and rain/soil permit.',
        'rice': 'Use the locally recommended rice water regime; do not assume a continuous-flood or dry-field method without checking your system and extension advice.',
        'maize': 'Protect moisture around tasseling/silking and grain filling; avoid waterlogging and check root-zone moisture before irrigating.',
        'tomato': 'Keep root-zone moisture steady during flowering and fruiting; prefer drip/soil-level watering and avoid repeated wet-dry stress.',
        'potato': 'Maintain even root-zone moisture during tuber initiation and bulking; avoid waterlogging and follow local advice before stopping irrigation near harvest.',
        'chickpea': 'Avoid waterlogging; if irrigation is needed, check local advice especially around flowering and pod filling.',
        'cotton': 'Prioritize root-zone moisture around flowering and boll development; avoid waterlogging and use field checks rather than a fixed calendar.',
        'sugarcane': 'Check moisture during establishment and rapid growth; use local irrigation intervals for your soil and method, and avoid waterlogging.',
        'other': 'Check soil moisture near active roots and use crop-specific local irrigation guidance.',
    }
    watering = f"{crop_watering.get(crop.name, crop_watering['other'])} {watering}"

    crop_nutrients = {
        'wheat': {
            'sowing': 'At sowing, base phosphorus and potassium plus any basal nitrogen on the soil test and local wheat recommendation.',
            'seedling': 'At establishment, follow the local split-nitrogen schedule; do not place fertilizer against seed or young roots.',
            'vegetative': 'At tillering/jointing, check whether a locally recommended split of nitrogen is due; avoid excess nitrogen.',
            'flowering': 'At flowering, do not apply nitrogen automatically. Use only locally recommended nutrients based on soil/crop diagnosis.',
            'fruiting': 'During grain filling, avoid late nitrogen unless locally advised; check crop maturity and soil test.',
            'maturity': 'Near harvest, do not add fertilizer automatically.',
        },
        'rice': {
            'sowing': 'At planting/transplanting, follow the soil-test-based basal NPK plan for the rice system and local variety.',
            'seedling': 'After establishment, follow local split-nitrogen timing; keep drainage and water level appropriate to the rice system.',
            'vegetative': 'At active tillering, apply a nitrogen split only if it is due in your local rice schedule.',
            'flowering': 'At panicle initiation/flowering, use only the locally advised nutrient split; do not overapply nitrogen.',
            'fruiting': 'During grain filling, avoid unplanned late fertilizer and maintain the locally recommended water regime.',
            'maturity': 'Near harvest, do not add fertilizer automatically; follow local drainage and harvest guidance.',
        },
        'maize': {
            'sowing': 'At sowing, use a soil-test-based basal phosphorus/potassium plan and place starter fertilizer safely away from seed.',
            'seedling': 'At early growth, check the locally recommended first nitrogen split; avoid fertilizer touching stems or roots.',
            'vegetative': 'At knee-high/rapid growth, apply a nitrogen split only if locally due and rain is not imminent.',
            'flowering': 'At tasseling/silking, avoid excess nitrogen; correct a diagnosed deficiency only under local guidance.',
            'fruiting': 'During grain filling, do not add nutrients automatically; use local crop-stage advice.',
            'maturity': 'Near harvest, do not add fertilizer automatically.',
        },
        'tomato': {
            'sowing': 'At transplanting, incorporate mature compost and a soil-test-based balanced nutrient plan; keep fertilizer off roots.',
            'seedling': 'After transplant establishment, use only a locally advised light nutrient application if plants need it.',
            'vegetative': 'During canopy growth, avoid excess nitrogen; apply balanced nutrients only according to soil test and local schedule.',
            'flowering': 'At flowering, maintain balanced nutrition; avoid excess nitrogen and diagnose any deficiency before correction.',
            'fruiting': 'During fruit development, potassium may be important, but use a soil-test/local recommendation for product and timing.',
            'maturity': 'During final picking, avoid unplanned fertilizer and observe any product pre-harvest instructions.',
        },
        'potato': {
            'sowing': 'At planting, use a soil-test-based basal NPK plan; place fertilizer safely below/aside from seed tubers.',
            'seedling': 'After emergence, follow local earthing-up and split-nitrogen timing; do not apply blindly.',
            'vegetative': 'During canopy/tuber initiation, follow the local nitrogen and potassium schedule; avoid excess nitrogen.',
            'flowering': 'During tuber bulking, maintain even moisture and apply nutrients only if locally recommended.',
            'fruiting': 'During tuber bulking, potassium needs depend on soil and crop plan; confirm with local advice.',
            'maturity': 'Near haulm maturity/harvest, stop unplanned fertilizer and follow local harvest guidance.',
        },
        'chickpea': {
            'sowing': 'At sowing, use inoculated seed where locally recommended and soil-test-based phosphorus; avoid heavy nitrogen.',
            'seedling': 'Check stand and drainage; do not add nitrogen automatically to a legume.',
            'vegetative': 'Avoid waterlogging and excess nitrogen; apply nutrients only where soil test/local guidance indicates a need.',
            'flowering': 'At flowering, avoid water stress but do not over-irrigate; do not apply fertilizer without local advice.',
            'fruiting': 'At pod filling, protect root-zone moisture and use only diagnosed, locally recommended nutrients.',
            'maturity': 'Near harvest, do not add fertilizer automatically.',
        },
        'cotton': {
            'sowing': 'At sowing, use a soil-test-based basal phosphorus/potassium plan and safe fertilizer placement.',
            'seedling': 'After establishment, follow the local split-nutrient schedule; avoid fertilizer touching stems.',
            'vegetative': 'During square/branch growth, apply nitrogen or potassium splits only when locally due.',
            'flowering': 'At flowering/boll set, avoid excess nitrogen; correct deficiencies only after local diagnosis.',
            'fruiting': 'During boll development, follow local potassium/nitrogen schedule and protect soil moisture.',
            'maturity': 'Near final boll opening, avoid unplanned late fertilizer.',
        },
        'sugarcane': {
            'sowing': 'At planting, follow a soil-test-based basal phosphorus/potassium and organic-matter plan.',
            'seedling': 'At establishment, keep fertilizer away from setts/young roots and use local split timing.',
            'vegetative': 'During tillering/rapid growth, apply nitrogen/potassium splits only at locally recommended times.',
            'flowering': 'Follow local sugarcane nutrient schedule; do not apply a late nitrogen dose without advice.',
            'fruiting': 'During stalk growth/maturity, avoid unplanned fertilizer and follow local harvest timing.',
            'maturity': 'Near harvest, do not add fertilizer automatically; follow local crop guidance.',
        },
        'other': {},
    }
    nutrient_advice = crop_nutrients.get(crop.name, {}).get(crop.stage)
    if not nutrient_advice:
        nutrient_advice = (
            'Use the crop- and growth-stage-specific soil-test recommendation. Ask your local KVK/agriculture officer '
            'which nutrient/product is due; do not guess a dose.'
        )
    fertilizer = nutrient_advice
    if soil_type:
        fertilizer += f' Farm profile soil type: {soil_type}; confirm it with a soil test.'

    precautions = (
        "Avoid fertilizer application just before heavy rain, flooding, or strong wind. Use soil-test and "
        "local agriculture/KVK guidance for product and dose; wear protective equipment and follow the label."
    )
    return {'watering': watering, 'fertilizer': fertilizer, 'precautions': precautions}


def get_user_profile(user):
    profile, _ = FarmerProfile.objects.get_or_create(
        user=user,
        defaults={
            'farm_name': f'{user.username.title()} Farm',
            'district': 'Not set',
            'crop_type': 'Wheat',
            'acreage': 0,
            'phone': '',
            'location': '',
        },
    )
    return profile


def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def dashboard(request):
    profile = get_user_profile(request.user)
    latest = SensorReading.objects.filter(user=request.user).order_by('-timestamp').first()
    readings = SensorReading.objects.filter(user=request.user).order_by('-timestamp')[:5]
    crops = FarmCrop.objects.filter(user=request.user)
    weather, weather_error = None, None
    weather_city = profile.city or (profile.district if profile.district != 'Not set' else '')
    if weather_city or profile.state:
        try:
            weather, weather_error = get_local_weather(weather_city, profile.state)
        except WeatherServiceError as exc:
            weather_error = str(exc)

    if latest:
        metrics = [
            {'label': 'Soil moisture', 'value': f'{latest.soil_moisture:.0f}%', 'note': 'Current moisture level'},
            {'label': 'Air temperature', 'value': f'{latest.temperature:.0f}°C', 'note': 'Daily thermal range'},
            {'label': 'Humidity', 'value': f'{latest.humidity:.0f}%', 'note': 'Ambient humidity level'},
            {'label': 'Irrigation need', 'value': latest.irrigation_status, 'note': 'Based on field reading'},
        ]
    else:
        metrics = [
            {'label': 'Soil moisture', 'value': '72%', 'note': 'No live sensor yet'},
            {'label': 'Air temperature', 'value': '28°C', 'note': 'No live sensor yet'},
            {'label': 'Humidity', 'value': '64%', 'note': 'No live sensor yet'},
            {'label': 'Irrigation need', 'value': 'Low', 'note': 'Add field data to update'},
        ]

    return render(request, 'dashboard.html', {
        'metrics': metrics,
        'crops': crops,
        'profile': profile,
        'readings': readings,
        'weather': weather,
        'weather_error': weather_error,
    })


@login_required(login_url='login')
def crop_management(request):
    if request.method == 'POST':
        form = FarmCropForm(request.POST, request.FILES)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.user = request.user
            crop.save()
            messages.success(request, f'{crop.get_name_display()} added to your crop plan.')
            return redirect('crops')
    else:
        form = FarmCropForm()

    profile = get_user_profile(request.user)
    latest = SensorReading.objects.filter(user=request.user).first()
    crops = FarmCrop.objects.filter(user=request.user).select_related('user')
    weather, weather_error = None, None
    weather_city = profile.city or (profile.district if profile.district != 'Not set' else '')
    if weather_city or profile.state:
        try:
            weather, weather_error = get_local_weather(weather_city, profile.state)
        except WeatherServiceError as exc:
            weather_error = str(exc)

    suggested_soil = suggest_soil_type(profile.city or profile.district, profile.state)
    effective_soil = profile.get_soil_type_display() if profile.soil_type else (
        suggested_soil['soil_label'] if suggested_soil else ''
    )
    crop_guidance = []
    for crop in crops:
        activity_form = CropActivityForm(prefix=f'activity-{crop.pk}')
        schedule_form = FertilizerScheduleForm(prefix=f'fertilizer-{crop.pk}')
        crop_guidance.append({
            'crop': crop,
            'guidance': crop_care_guidance(crop, latest, weather, effective_soil),
            'activity_form': activity_form,
            'activities': crop.activities.all()[:8],
            'schedule_form': schedule_form,
            'fertilizer_schedules': crop.fertilizer_schedules.all(),
            'fertilizer_reference': get_fertilizer_reference(crop, crop.area_acres, profile.state),
        })
    return render(request, 'crops.html', {
        'form': form,
        'crops': crops,
        'profile': profile,
        'crop_guidance': crop_guidance,
        'weather': weather,
        'weather_error': weather_error,
        'suggested_soil': suggested_soil,
        'soil_is_estimate': not bool(profile.soil_type),
        'today': timezone.localdate(),
    })


@login_required(login_url='login')
def add_fertilizer_schedule(request, crop_id):
    crop = get_object_or_404(FarmCrop, pk=crop_id, user=request.user)
    if request.method != 'POST':
        return redirect('crops')

    form = FertilizerScheduleForm(request.POST, prefix=f'fertilizer-{crop.pk}')
    if form.is_valid():
        schedule = form.save(commit=False)
        schedule.crop = crop
        schedule.save()
        messages.success(request, f'Fertilizer schedule saved for {crop.get_name_display()}.')
        return redirect('crops')

    errors = '; '.join(
        error
        for field_errors in form.errors.values()
        for error in field_errors
    )
    messages.error(request, f'Fertilizer schedule could not be saved: {errors}')
    return redirect('crops')


@login_required(login_url='login')
def mark_fertilizer_applied(request, schedule_id):
    if request.method != 'POST':
        return redirect('crops')
    schedule = get_object_or_404(
        FertilizerSchedule.objects.select_related('crop'),
        pk=schedule_id,
        crop__user=request.user,
    )
    applied_on = timezone.localdate()
    schedule.last_applied_on = applied_on
    schedule.save(update_fields=['last_applied_on'])

    total_amount = schedule.total_amount
    CropActivity.objects.create(
        crop=schedule.crop,
        activity_type='fertilizer',
        completed=True,
        product_or_method=schedule.fertilizer_name,
        quantity=total_amount,
        unit=schedule.unit,
        condition='unknown',
        notes=f'Applied on {applied_on:%Y-%m-%d}. Crop condition not checked. Advised rate: {schedule.rate_per_acre} {schedule.unit}/acre.',
        recorded_at=timezone.now(),
    )
    messages.success(
        request,
        f'{schedule.fertilizer_name} marked applied. Next reminder: {schedule.next_due_on:%b %d, %Y}.',
    )
    return redirect('crops')


@login_required(login_url='login')
def delete_fertilizer_schedule(request, schedule_id):
    if request.method != 'POST':
        return redirect('crops')
    schedule = get_object_or_404(
        FertilizerSchedule.objects.select_related('crop'),
        pk=schedule_id,
        crop__user=request.user,
    )
    crop_name = schedule.crop.get_name_display()
    fertilizer_name = schedule.fertilizer_name
    schedule.delete()
    messages.success(request, f'{fertilizer_name} schedule removed from {crop_name}.')
    return redirect('crops')


@login_required(login_url='login')
def log_crop_activity(request, crop_id):
    crop = get_object_or_404(FarmCrop, pk=crop_id, user=request.user)
    if request.method != 'POST':
        return redirect('crops')

    form = CropActivityForm(request.POST, prefix=f'activity-{crop.pk}')
    if form.is_valid():
        activity = form.save(commit=False)
        activity.crop = crop
        activity.save()
        if activity.completed:
            messages.success(request, f'{activity.get_activity_type_display()} recorded for {crop.get_name_display()}.')
        else:
            messages.success(request, f'Pending {activity.get_activity_type_display().lower()} reminder saved for {crop.get_name_display()}.')
        return redirect('crops')
    errors = '; '.join(
        error
        for field_errors in form.errors.values()
        for error in field_errors
    )
    messages.error(request, f'Activity could not be saved: {errors}')
    return redirect('crops')


@login_required(login_url='login')
def profile_settings(request):
    profile = get_user_profile(request.user)
    if request.method == 'POST':
        form = FarmerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farm profile updated successfully.')
            return redirect('profile')
    else:
        form = FarmerProfileForm(instance=profile)
    soil_city = profile.city or (profile.district if profile.district != 'Not set' else '')
    suggested_soil = suggest_soil_type(soil_city, profile.state)
    return render(request, 'profile.html', {
        'form': form,
        'profile': profile,
        'suggested_soil': suggested_soil,
    })


@login_required(login_url='login')
def sensor_entry(request):
    if request.method == 'POST':
        form = SensorReadingForm(request.POST)
        if form.is_valid():
            reading = form.save(commit=False)
            reading.user = request.user
            reading.save()
            messages.success(request, 'Sensor data saved successfully.')
            return redirect('dashboard')
    else:
        form = SensorReadingForm()
    return render(request, 'sensor_entry.html', {'form': form})


@login_required(login_url='login')
def crop_health(request):
    symptom_labels = dict(CropHealthForm.base_fields['symptoms'].choices)
    crop_symptom_map = {
        crop: sorted({
            symptom
            for disease in diseases
            for symptom in disease['symptoms']
        })
        for crop, diseases in DISEASE_GUIDES.items()
    }
    if request.method == 'POST':
        form = CropHealthForm(request.POST)
        if form.is_valid():
            candidates = screen_crop_symptoms(
                form.cleaned_data['crop'],
                form.cleaned_data['symptoms'],
            )
            crop_label = form.fields['crop'].choices
            crop_name = dict(crop_label)[form.cleaned_data['crop']]
            selected_symptoms = [
                symptom_labels[symptom] for symptom in form.cleaned_data['symptoms']
            ]
            candidates = [
                {
                    **candidate,
                    'matched_labels': [
                        symptom_labels[symptom]
                        for symptom in candidate['matched_symptoms']
                    ],
                }
                for candidate in candidates
            ]
            return render(request, 'crop_health.html', {
                'form': form,
                'candidates': candidates,
                'crop_name': crop_name,
                'selected_symptoms': selected_symptoms,
                'crop_symptom_map': crop_symptom_map,
                'show_results': True,
            })
    else:
        form = CropHealthForm()

    return render(request, 'crop_health.html', {
        'form': form,
        'crop_symptom_map': crop_symptom_map,
    })


def recommendations(request):
    recommendations = [
        {
            'crop': 'Wheat',
            'fit': 'High fit',
            'reason': 'Moisture balance and moderate temperature support a strong yield window.',
            'action': 'Apply 12% nitrogen boost in the next irrigation cycle.',
        },
        {
            'crop': 'Chickpea',
            'fit': 'Medium fit',
            'reason': 'The current soil profile is suitable with limited water stress.',
            'action': 'Add row spacing mulch to reduce evaporation.',
        },
        {
            'crop': 'Capsicum',
            'fit': 'Strong fit',
            'reason': 'Warm conditions and moderate humidity are ideal for fruit setting.',
            'action': 'Increase drip irrigation by 10% during early afternoon.',
        },
    ]
    return render(request, 'recommendations.html', {'recommendations': recommendations})


def contact(request):
    return render(request, 'contact.html')
