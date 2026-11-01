from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import CropActivity, FarmCrop, FarmerProfile, FertilizerSchedule, SensorReading, SOIL_TYPE_CHOICES
from PIL import Image, UnidentifiedImageError


INDIAN_STATES = [
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Chandigarh', 'Chandigarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Delhi', 'Delhi'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Puducherry', 'Puducherry'),
]


class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['farm_name', 'district', 'state', 'city', 'soil_type', 'crop_type', 'acreage', 'phone', 'location']
        widgets = {
            'farm_name': forms.TextInput(attrs={'placeholder': 'Alpha Crop Farm'}),
            'district': forms.TextInput(attrs={'placeholder': 'Pune'}),
            'state': forms.Select(choices=[('', 'Select state / UT')] + INDIAN_STATES),
            'city': forms.TextInput(attrs={'placeholder': 'Pune', 'autocomplete': 'address-level2'}),
            'soil_type': forms.Select(choices=[('', 'Select if known')] + SOIL_TYPE_CHOICES),
            'crop_type': forms.TextInput(attrs={'placeholder': 'Wheat'}),
            'acreage': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '25.5'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 98765 43210'}),
            'location': forms.TextInput(attrs={'placeholder': 'Near river belt, Maharashtra'}),
        }


class FarmerRegistrationForm(UserCreationForm):
    farm_name = forms.CharField(
        max_length=150,
        required=False,
        label='Farm name (optional)',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Green Valley Farm', 'autocomplete': 'organization'}),
    )
    state = forms.ChoiceField(
        required=False,
        choices=[('', 'Select state / UT')] + INDIAN_STATES,
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Pune', 'autocomplete': 'address-level2'}),
    )
    soil_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Choose if you know it')] + SOIL_TYPE_CHOICES,
        help_text='Optional. Use a soil test to confirm; state-level estimates are only a guide.',
    )

    class Meta:
        model = get_user_model()
        fields = ['username']

    field_order = ['username', 'farm_name', 'state', 'city', 'soil_type', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].label = 'State / Union Territory (optional)'
        self.fields['city'].label = 'City or district (optional)'
        self.fields['city'].help_text = 'Helps tailor local farm insights.'
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Choose a username',
            'autocomplete': 'username',
            'autofocus': True,
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a password',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Enter the password again',
            'autocomplete': 'new-password',
        })


class FarmerLoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'autocomplete': 'username',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
        }),
    )


class SensorReadingForm(forms.ModelForm):
    class Meta:
        model = SensorReading
        fields = ['soil_moisture', 'temperature', 'humidity', 'rainfall', 'irrigation_status', 'notes']
        widgets = {
            'soil_moisture': forms.NumberInput(attrs={'step': '0.1', 'placeholder': '72'}),
            'temperature': forms.NumberInput(attrs={'step': '0.1', 'placeholder': '28'}),
            'humidity': forms.NumberInput(attrs={'step': '0.1', 'placeholder': '64'}),
            'rainfall': forms.NumberInput(attrs={'step': '0.1', 'placeholder': '12'}),
            'irrigation_status': forms.Select(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any field observation...'}),
        }


class FarmCropForm(forms.ModelForm):
    class Meta:
        model = FarmCrop
        fields = ['name', 'image', 'variety', 'stage', 'planted_on', 'area_acres', 'notes']
        help_texts = {
            'image': 'Optional. Add a clear crop photo (JPEG, PNG or WebP, up to 5 MB).',
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png,image/webp'}),
            'variety': forms.TextInput(attrs={'placeholder': 'Variety (optional)'}),
            'planted_on': forms.DateInput(attrs={'type': 'date'}),
            'area_acres': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01', 'placeholder': 'Area in acres'}),
            'notes': forms.TextInput(attrs={'placeholder': 'Optional field notes'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Image must be 5 MB or smaller.')

        try:
            with Image.open(image) as uploaded_image:
                if uploaded_image.format not in {'JPEG', 'PNG', 'WEBP'}:
                    raise forms.ValidationError('Upload a JPEG, PNG, or WebP image.')
                if uploaded_image.width > 6000 or uploaded_image.height > 6000:
                    raise forms.ValidationError('Image dimensions must be 6000 × 6000 pixels or smaller.')
                uploaded_image.verify()
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
            raise forms.ValidationError('This image could not be read. Try another JPEG, PNG, or WebP file.') from exc
        finally:
            image.seek(0)
        return image


class CropActivityForm(forms.ModelForm):
    class Meta:
        model = CropActivity
        fields = [
            'activity_type',
            'completed',
            'product_or_method',
            'quantity',
            'unit',
            'condition',
            'notes',
        ]
        widgets = {
            'completed': forms.CheckboxInput(),
            'product_or_method': forms.TextInput(attrs={
                'placeholder': 'e.g. drip irrigation, compost, or product name',
            }),
            'quantity': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01', 'placeholder': 'Optional'}),
            'unit': forms.TextInput(attrs={'placeholder': 'L, kg, bag, etc.'}),
            'notes': forms.TextInput(attrs={'placeholder': 'What did you observe?'}),
        }


class FertilizerScheduleForm(forms.ModelForm):
    class Meta:
        model = FertilizerSchedule
        fields = [
            'fertilizer_name',
            'rate_per_acre',
            'unit',
            'interval_days',
            'last_applied_on',
            'advisory_source',
        ]
        labels = {
            'fertilizer_name': 'Fertilizer / nutrient',
            'rate_per_acre': 'Advised amount per acre',
            'interval_days': 'Repeat after (days)',
            'last_applied_on': 'Last applied / first planned date',
            'advisory_source': 'Recommendation source (optional)',
        }
        help_texts = {
            'rate_per_acre': 'Enter the dose from your soil test, KVK or agriculture officer—not a guess.',
            'interval_days': 'Use the interval in your crop-specific local recommendation.',
            'advisory_source': 'For example: soil test report date or local KVK advice.',
        }
        widgets = {
            'fertilizer_name': forms.TextInput(attrs={
                'placeholder': 'e.g. Urea, compost, or NPK grade from your advice',
            }),
            'rate_per_acre': forms.NumberInput(attrs={'step': '0.001', 'min': '0.001'}),
            'interval_days': forms.NumberInput(attrs={'min': '1', 'max': '365'}),
            'last_applied_on': forms.DateInput(attrs={'type': 'date'}),
            'advisory_source': forms.TextInput(attrs={'placeholder': 'Soil test / KVK / agriculture officer'}),
        }

    def clean_interval_days(self):
        interval_days = self.cleaned_data['interval_days']
        if not 1 <= interval_days <= 365:
            raise forms.ValidationError('Enter an interval from 1 to 365 days.')
        return interval_days

    def clean_rate_per_acre(self):
        rate = self.cleaned_data['rate_per_acre']
        if rate <= 0:
            raise forms.ValidationError('Enter a positive amount from your soil test or local recommendation.')
        return rate


CROP_CHOICES = [
    ('tomato', 'Tomato'),
    ('wheat', 'Wheat'),
    ('rice', 'Rice'),
    ('potato', 'Potato'),
    ('maize', 'Maize'),
    ('chickpea', 'Chickpea / gram'),
    ('cotton', 'Cotton'),
    ('sugarcane', 'Sugarcane'),
]

SYMPTOM_CHOICES = [
    ('brown_spots', 'Brown spots on leaves'),
    ('concentric_rings', 'Spots with rings or a target-like pattern'),
    ('yellow_leaves', 'Leaves turning yellow'),
    ('leaf_curl', 'Leaves curling or twisting'),
    ('orange_pustules', 'Orange or rust-coloured powder/pustules'),
    ('pustules_rub_off', 'Orange powder rubs off onto fingers or tissue'),
    ('white_powder', 'White powdery coating'),
    ('white_growth_on_stems', 'White coating also appears on stems'),
    ('water_soaked', 'Dark, water-soaked patches'),
    ('white_underside', 'White growth under leaves'),
    ('rapid_spread', 'Leaf patches spread quickly in cool or wet weather'),
    ('lower_leaves_first', 'Older/lower leaves show spots first'),
    ('diamond_lesions', 'Diamond-shaped lesions with grey centres'),
    ('wavy_edges', 'Wavy brown edges or yellowing from leaf tips'),
    ('yellowing_from_tip', 'Yellowing starts at leaf tips and moves along edges'),
    ('milky_ooze', 'Milky-looking ooze from cut leaf/stem (do not taste or touch eyes)'),
    ('grey_lesion_centres', 'Long leaf lesions have grey or tan centres'),
    ('neck_rot', 'Dark lesion around the panicle/neck'),
    ('lesions_near_waterline', 'Rice lesions start on lower leaf sheath near waterline'),
    ('oval_sheath_lesions', 'Oval green-grey lesions on leaf sheath'),
    ('white_fungal_growth', 'White fungal growth near lower leaf sheath'),
    ('small_brown_spots', 'Many small brown spots on leaves'),
    ('yellow_halo', 'Brown spots have a yellow halo'),
    ('dead_heart', 'Central shoot dries but can be pulled out easily'),
    ('white_head', 'Rice panicle is white/empty while nearby panicles are green'),
    ('bore_hole_stem', 'Small bore hole or tunnel in stem/stalk'),
    ('elongated_lesions', 'Long, narrow tan/brown lesions'),
    ('windowpane_damage', 'Young leaves have scraped/windowpane patches'),
    ('chewed_leaves', 'Leaves with holes or scraped/windowpane patches'),
    ('insect_frass', 'Caterpillars or fresh droppings in the plant whorl'),
    ('frass_in_whorl', 'Fresh caterpillar droppings inside the whorl'),
    ('whole_plant_wilt', 'Whole plant wilts even though soil is moist'),
    ('green_leaves_wilt', 'Plant wilts while leaves remain green'),
    ('brown_vascular_tissue', 'Brown streaks inside a cut stem/root'),
    ('yellowing_one_side', 'One side of the plant yellows or wilts first'),
    ('small_leaves', 'New leaves are unusually small and curled'),
    ('whiteflies', 'Tiny white insects fly up from leaf undersides'),
    ('fruit_holes', 'Round holes in fruits, pods or bolls'),
    ('frass_on_fruit', 'Fresh droppings near a hole in fruit/pod'),
    ('frass_on_pod', 'Fresh droppings near a hole in pod'),
    ('caterpillar_on_fruit', 'Caterpillar feeding on fruit or pod'),
    ('caterpillar_on_pod', 'Caterpillar feeding on pod'),
    ('black_powder_ear', 'Wheat head replaced by black powder'),
    ('empty_black_ears', 'Some wheat heads are black and contain no grain'),
    ('black_spores', 'Black spores visible on a seed head'),
    ('aphids_on_ear', 'Clusters of small green/black insects on wheat ear'),
    ('sticky_leaves', 'Leaves feel sticky or have honeydew'),
    ('ants_on_plant', 'Many ants visiting the plant'),
    ('grey_tan_centres', 'Long maize leaf lesions have grey/tan centres'),
    ('frass_on_boll', 'Fresh droppings near a hole in cotton boll'),
    ('caterpillar_on_boll', 'Caterpillar feeding inside cotton boll'),
    ('thickened_veins', 'Cotton leaf veins look thickened/raised'),
    ('leaf_cup', 'Cotton leaves cup upward or downward'),
    ('angular_water_soaked_spots', 'Angular water-soaked spots between cotton leaf veins'),
    ('dark_veins', 'Cotton leaf veins turn dark'),
    ('black_stem_lesions', 'Dark lesions on cotton stem'),
    ('leaf_edges_brown', 'Cotton leaf edges turn bronze/brown'),
    ('downward_leaf_curl', 'Cotton leaves cup or curl downward'),
    ('small_sucking_insects', 'Tiny insects visible under cotton leaves'),
    ('red_pith_white_patches', 'Sugarcane split lengthwise has red tissue with white patches'),
    ('red_stalk_tissue', 'Inside of sugarcane stalk is red'),
    ('sour_stalk_smell', 'Cut cane has a sour smell'),
    ('black_whip', 'Long black whip-like growth from sugarcane shoot'),
    ('whip_from_shoot', 'Black whip emerges from the top of a shoot'),
    ('thin_grassy_stalks', 'Many thin, grassy-looking shoots in a clump'),
    ('stunted_growth', 'Stunted growth or poor vigour'),
]


class CropHealthForm(forms.Form):
    crop = forms.ChoiceField(choices=CROP_CHOICES, label='Which crop is affected?')
    symptoms = forms.MultipleChoiceField(
        choices=SYMPTOM_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='What are you seeing?',
        help_text='Choose all symptoms you can clearly observe. More detail improves this preliminary screening.',
    )
