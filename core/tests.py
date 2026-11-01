from datetime import timedelta
from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from .crop_health import DISEASE_GUIDES, screen_crop_symptoms
from .forms import CROP_CHOICES
from .fertilizer_recommendations import get_fertilizer_reference
from .models import CropActivity, FarmCrop, FarmerProfile, FertilizerSchedule
from .soil_suggestions import suggest_soil_type
from .weather import WeatherServiceError, get_local_weather


class CropCareTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='crop-test-farmer',
            password='TestPassword123!',
        )
        FarmerProfile.objects.create(
            user=self.user,
            farm_name='Test Farm',
            district='Pune',
            city='Pune',
            state='Maharashtra',
        )
        self.client.force_login(self.user)

    def tearDown(self):
        for crop in FarmCrop.objects.filter(user=self.user):
            if crop.image:
                crop.image.delete(save=False)
        super().tearDown()

    @staticmethod
    def make_image_upload(name='crop.png', image_format='PNG'):
        image_bytes = BytesIO()
        Image.new('RGB', (8, 8), color='green').save(image_bytes, format=image_format)
        return SimpleUploadedFile(
            name,
            image_bytes.getvalue(),
            content_type=f'image/{image_format.lower()}',
        )

    def test_navigation_replaces_contact_with_profile_icon_and_profile_is_editable(self):
        home_response = self.client.get(reverse('home'))

        self.assertContains(home_response, 'aria-label="Edit farm profile"')
        self.assertContains(home_response, 'href="/profile/"')
        self.assertNotContains(home_response, 'href="/contact/"')
        self.assertNotContains(home_response, f'Hi, {self.user.username}')

        profile_response = self.client.get(reverse('profile'))
        self.assertEqual(profile_response.status_code, 200)

        profile_response = self.client.post(reverse('profile'), {
            'farm_name': 'Updated Test Farm',
            'district': 'Nashik',
            'state': 'Maharashtra',
            'city': 'Nashik',
            'soil_type': 'black',
            'crop_type': 'Wheat',
            'acreage': '12.50',
            'phone': '',
            'location': '',
        })

        self.assertRedirects(profile_response, reverse('profile'))
        self.user.farmer_profile.refresh_from_db()
        self.assertEqual(self.user.farmer_profile.farm_name, 'Updated Test Farm')
        self.assertEqual(self.user.farmer_profile.city, 'Nashik')

    def test_homepage_shows_farmer_harvesting_photo(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'alt="Woman farmer harvesting rice in a paddy field"')

    def test_farmer_can_add_crop_and_view_stage_guidance(self):
        response = self.client.post(reverse('crops'), {
            'name': 'tomato',
            'variety': 'Roma',
            'stage': 'flowering',
            'planted_on': '2026-09-01',
            'area_acres': '2.5',
            'notes': '',
        })

        self.assertRedirects(response, reverse('crops'))
        crop = FarmCrop.objects.get(user=self.user)
        self.assertEqual(crop.name, 'tomato')
        self.assertEqual(crop.stage, 'flowering')

        with patch('core.views.get_local_weather', return_value=(None, 'No weather data')):
            response = self.client.get(reverse('crops'))
        self.assertContains(response, 'Tomato')
        self.assertContains(response, 'flowering')
        self.assertContains(response, 'soil test')

    def test_farmer_can_upload_and_see_crop_photo(self):
        response = self.client.post(reverse('crops'), {
            'name': 'tomato',
            'variety': '',
            'stage': 'vegetative',
            'planted_on': '',
            'area_acres': '',
            'notes': '',
            'image': self.make_image_upload(),
        })

        self.assertRedirects(response, reverse('crops'))
        crop = FarmCrop.objects.get(user=self.user)
        self.assertTrue(crop.image.name.startswith(f'crop_photos/{self.user.pk}/'))
        self.assertTrue(crop.image.storage.exists(crop.image.name), crop.image.path)

        response = self.client.get(reverse('crops'))
        self.assertContains(response, crop.image.url)
        self.assertContains(response, 'crop photo')

        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, crop.image.url)

    def test_crop_photo_rejects_non_image_and_oversized_files(self):
        invalid_image = SimpleUploadedFile(
            'fake.png',
            b'this is not an image',
            content_type='image/png',
        )
        response = self.client.post(reverse('crops'), {
            'name': 'tomato',
            'stage': 'vegetative',
            'image': invalid_image,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(FarmCrop.objects.filter(user=self.user).exists())

    def test_farmer_can_log_completed_watering_and_crop_condition(self):
        crop = FarmCrop.objects.create(user=self.user, name='tomato', stage='flowering')
        prefix = f'activity-{crop.pk}'

        response = self.client.post(reverse('log-crop-activity', args=[crop.pk]), {
            f'{prefix}-activity_type': 'watering',
            f'{prefix}-completed': 'on',
            f'{prefix}-product_or_method': 'Drip irrigation',
            f'{prefix}-quantity': '250',
            f'{prefix}-unit': 'L',
            f'{prefix}-condition': 'watch',
            f'{prefix}-notes': 'Leaves slightly wilted before watering',
        })

        self.assertRedirects(response, reverse('crops'))
        activity = CropActivity.objects.get(crop=crop)
        self.assertTrue(activity.completed)
        self.assertEqual(activity.activity_type, 'watering')
        self.assertEqual(activity.condition, 'watch')
        self.assertEqual(activity.quantity, 250)
        self.assertEqual(activity.unit, 'L')
        with patch('core.views.get_local_weather', return_value=(None, 'No weather data')):
            response = self.client.get(reverse('crops'))
        self.assertContains(response, 'Drip irrigation')
        self.assertContains(response, 'Needs watching')

    def test_farmer_cannot_log_activity_to_another_farmers_crop(self):
        other_user = get_user_model().objects.create_user(
            username='another-crop-owner',
            password='TestPassword123!',
        )
        crop = FarmCrop.objects.create(user=other_user, name='rice')

        response = self.client.post(reverse('log-crop-activity', args=[crop.pk]), {
            f'activity-{crop.pk}-activity_type': 'watering',
            f'activity-{crop.pk}-completed': 'on',
            f'activity-{crop.pk}-condition': 'good',
        })

        self.assertEqual(response.status_code, 404)
        self.assertFalse(CropActivity.objects.filter(crop=crop).exists())

    def test_farmer_can_create_fertilizer_schedule_and_see_calculated_total(self):
        crop = FarmCrop.objects.create(
            user=self.user,
            name='tomato',
            stage='flowering',
            area_acres='2.50',
        )
        prefix = f'fertilizer-{crop.pk}'
        response = self.client.post(reverse('add-fertilizer-schedule', args=[crop.pk]), {
            f'{prefix}-fertilizer_name': 'Soil-test advised fertilizer',
            f'{prefix}-rate_per_acre': '12.500',
            f'{prefix}-unit': 'kg',
            f'{prefix}-interval_days': '14',
            f'{prefix}-last_applied_on': '2026-10-01',
            f'{prefix}-advisory_source': 'Farm soil test',
        })

        self.assertRedirects(response, reverse('crops'))
        schedule = FertilizerSchedule.objects.get(crop=crop)
        self.assertEqual(schedule.total_amount, 31.25000)
        self.assertEqual(str(schedule.next_due_on), '2026-10-15')
        with patch('core.views.get_local_weather', return_value=(None, 'No weather data')):
            response = self.client.get(reverse('crops'))
        self.assertContains(response, '31.25 kg')
        self.assertContains(response, 'Oct 15, 2026')
        self.assertContains(response, 'Farm soil test')

    def test_marking_schedule_applied_updates_next_date_and_activity_log(self):
        crop = FarmCrop.objects.create(
            user=self.user,
            name='wheat',
            area_acres='2.00',
        )
        schedule = FertilizerSchedule.objects.create(
            crop=crop,
            fertilizer_name='Advised fertilizer',
            rate_per_acre='5.000',
            unit='kg',
            interval_days=21,
            last_applied_on=timezone.localdate() - timedelta(days=30),
        )

        response = self.client.post(reverse('mark-fertilizer-applied', args=[schedule.pk]))

        self.assertRedirects(response, reverse('crops'))
        schedule.refresh_from_db()
        self.assertEqual(schedule.last_applied_on, timezone.localdate())
        self.assertEqual(schedule.next_due_on, timezone.localdate() + timedelta(days=21))
        activity = CropActivity.objects.get(crop=crop, activity_type='fertilizer')
        self.assertTrue(activity.completed)
        self.assertEqual(activity.quantity, 10)
        self.assertEqual(activity.unit, 'kg')

    def test_farmer_cannot_change_another_farmers_fertilizer_schedule(self):
        other_user = get_user_model().objects.create_user(
            username='another-fertilizer-owner',
            password='TestPassword123!',
        )
        crop = FarmCrop.objects.create(user=other_user, name='rice')
        schedule = FertilizerSchedule.objects.create(
            crop=crop,
            fertilizer_name='Advised fertilizer',
            rate_per_acre='1',
            unit='kg',
            interval_days=30,
            last_applied_on=timezone.localdate() - timedelta(days=30),
        )
        previous_date = schedule.last_applied_on

        response = self.client.post(reverse('mark-fertilizer-applied', args=[schedule.pk]))

        self.assertEqual(response.status_code, 404)
        schedule.refresh_from_db()
        self.assertEqual(schedule.last_applied_on, previous_date)

        oversized_image = SimpleUploadedFile(
            'too-large.png',
            b'x' * (5 * 1024 * 1024 + 1),
            content_type='image/png',
        )
        response = self.client.post(reverse('crops'), {
            'name': 'tomato',
            'stage': 'vegetative',
            'image': oversized_image,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(FarmCrop.objects.filter(user=self.user).exists())

    @patch('core.views.get_local_weather')
    def test_dashboard_uses_local_weather(self, get_weather):
        get_weather.return_value = ({
            'place': 'Pune, Maharashtra',
            'time': '2026-10-06T11:00',
            'temperature': 29,
            'humidity': 45,
            'description': 'Clear sky',
            'wind_speed': 3,
            'current_rain': 0,
            'today_rain': 0.2,
            'tomorrow_rain': 0,
            'rain_guidance': 'Check the root-zone soil.',
        }, None)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pune, Maharashtra')
        get_weather.assert_called_once_with('Pune', 'Maharashtra')


class CropSymptomTests(TestCase):
    def test_matching_and_insufficient_symptoms(self):
        match = screen_crop_symptoms('tomato', ['water_soaked', 'white_underside'])
        self.assertEqual(match[0]['name'], 'Late blight')
        self.assertEqual(screen_crop_symptoms('tomato', ['water_soaked']), [])

    def test_common_disease_patterns_cover_every_crop_choice(self):
        symptom_examples = {
            'tomato': ['water_soaked', 'white_underside'],
            'wheat': ['orange_pustules', 'pustules_rub_off'],
            'rice': ['diamond_lesions', 'grey_lesion_centres'],
            'potato': ['water_soaked', 'white_underside'],
            'maize': ['chewed_leaves', 'insect_frass'],
            'chickpea': ['yellowing_one_side', 'brown_vascular_tissue'],
            'cotton': ['leaf_curl', 'thickened_veins'],
            'sugarcane': ['red_pith_white_patches', 'sour_stalk_smell'],
        }

        self.assertEqual(set(symptom_examples), {crop for crop, _label in CROP_CHOICES})
        self.assertEqual(set(symptom_examples), set(DISEASE_GUIDES))
        for crop, symptoms in symptom_examples.items():
            with self.subTest(crop=crop):
                self.assertTrue(screen_crop_symptoms(crop, symptoms))

    def test_results_explain_matched_signs_and_pesticide_caution(self):
        user = get_user_model().objects.create_user(
            username='crop-health-farmer',
            password='TestPassword123!',
        )
        self.client.force_login(user)

        response = self.client.post(reverse('crop-health'), {
            'crop': 'rice',
            'symptoms': ['diamond_lesions', 'grey_lesion_centres'],
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rice blast')
        self.assertContains(response, 'Signs matched')
        self.assertContains(response, 'tricyclazole')
        self.assertContains(response, 'currently registered')


class SoilSuggestionTests(TestCase):
    def test_suggestion_uses_location_but_is_explicitly_a_broad_hint(self):
        suggestion = suggest_soil_type('Pune', 'Maharashtra')

        self.assertEqual(suggestion['soil_code'], 'black')
        self.assertEqual(suggestion['location'], 'Pune, Maharashtra')
        self.assertIn('also occur', suggestion['note'])
        self.assertIsNone(suggest_soil_type('Unknown', ''))


class FertilizerReferenceTests(TestCase):
    def test_reference_scales_nutrients_and_marks_regional_mismatch(self):
        crop = FarmCrop(name='wheat', area_acres='2.50')

        reference = get_fertilizer_reference(crop, crop.area_acres, 'Maharashtra')

        self.assertFalse(reference['region_matches'])
        general = reference['variants'][0]
        self.assertEqual(general['total']['n'], 125)
        self.assertEqual(general['total']['p'], 62.5)
        self.assertEqual(general['total']['k'], 30)
        low_k = reference['variants'][1]
        self.assertEqual(low_k['total']['k'], 60)

    def test_no_reference_is_returned_for_unlisted_crop(self):
        crop = FarmCrop(name='other', area_acres='1.00')

        self.assertIsNone(get_fertilizer_reference(crop, crop.area_acres, 'Punjab'))

    def test_ambiguous_tomato_source_does_not_produce_numeric_rates(self):
        crop = FarmCrop(name='tomato', area_acres='1.00')

        reference = get_fertilizer_reference(crop, crop.area_acres, 'Tamil Nadu')

        self.assertEqual(reference['variants'], [])
        self.assertIn('ambiguous', reference['note'])

    def test_crop_page_shows_per_acre_source_and_locality_warning(self):
        user = get_user_model().objects.create_user(
            username='fertilizer-reference-farmer',
            password='TestPassword123!',
        )
        FarmerProfile.objects.create(user=user, city='Pune', state='Maharashtra')
        self.client.force_login(user)
        crop = FarmCrop.objects.create(
            user=user,
            name='wheat',
            stage='flowering',
            area_acres='2.00',
        )

        with patch('core.views.get_local_weather', return_value=(None, 'No weather data')):
            response = self.client.get(reverse('crops'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '50.0 kg/acre')
        self.assertContains(response, 'For 2.00 acres')
        self.assertContains(response, 'Not locally verified for Maharashtra')
        self.assertContains(response, 'nutrient amounts, not urea/DAP/NPK fertilizer-product')
        self.assertFalse(FertilizerSchedule.objects.filter(crop=crop).exists())


class WeatherServiceTests(TestCase):
    @patch('core.weather.cache.get', return_value=None)
    @patch('core.weather._get_json')
    def test_returns_current_conditions_and_rain_forecast(self, get_json, _cache_get):
        get_json.side_effect = [
            {'results': [{'name': 'Pune', 'admin1': 'Maharashtra', 'latitude': 18.52, 'longitude': 73.85}]},
            {
                'current': {
                    'time': '2026-10-06T11:00',
                    'temperature_2m': 29,
                    'relative_humidity_2m': 50,
                    'precipitation': 0,
                    'weather_code': 0,
                    'wind_speed_10m': 4,
                },
                'daily': {
                    'time': ['2026-10-06', '2026-10-07'],
                    'precipitation_sum': [0, 8],
                },
            },
        ]

        weather, error = get_local_weather('Pune', 'Maharashtra')

        self.assertIsNone(error)
        self.assertEqual(weather['today_rain'], 0)
        self.assertEqual(weather['tomorrow_rain'], 8)
        self.assertEqual(weather['description'], 'Clear sky')

    @patch('core.weather.cache.get', return_value=None)
    @patch('core.weather._get_json', side_effect=WeatherServiceError('Weather offline'))
    def test_reports_weather_provider_failure(self, _get_json, _cache_get):
        with self.assertRaisesMessage(WeatherServiceError, 'Weather offline'):
            get_local_weather('Pune', 'Maharashtra')
