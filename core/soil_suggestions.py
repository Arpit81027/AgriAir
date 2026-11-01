from .models import SOIL_TYPE_CHOICES


# Broad predominant-soil hints only; state boundaries do not describe an individual field.
STATE_SOIL_HINTS = {
    'Andhra Pradesh': ('red_yellow', 'Mixed alluvial and black soils also occur.'),
    'Arunachal Pradesh': ('mountain', 'Soil varies with altitude and valley.'),
    'Assam': ('alluvial', 'Hill and other soil groups also occur.'),
    'Bihar': ('alluvial', 'Soil texture differs between north and south districts.'),
    'Chhattisgarh': ('red_yellow', 'Black soils occur in some districts.'),
    'Goa': ('laterite', 'Coastal and valley soils can differ.'),
    'Gujarat': ('black', 'Arid, alluvial and coastal soils also occur.'),
    'Haryana': ('alluvial', 'Sandy and saline patches occur in some areas.'),
    'Himachal Pradesh': ('mountain', 'Soil varies considerably by altitude.'),
    'Jharkhand': ('red_yellow', 'Soils vary across plateau and valley areas.'),
    'Karnataka': ('red_yellow', 'Black soils are common in several districts.'),
    'Kerala': ('laterite', 'Coastal and valley soils also occur.'),
    'Madhya Pradesh': ('black', 'Red and other soil groups occur in some districts.'),
    'Maharashtra': ('black', 'Lateritic, coastal and other soils also occur.'),
    'Manipur': ('red_yellow', 'Valley and hill soils differ.'),
    'Meghalaya': ('mountain', 'Soil varies by slope and rainfall.'),
    'Mizoram': ('mountain', 'Soil varies by slope and location.'),
    'Nagaland': ('mountain', 'Soil varies by slope and valley.'),
    'Odisha': ('red_yellow', 'Alluvial and coastal soils also occur.'),
    'Punjab': ('alluvial', 'Texture and drainage vary by district.'),
    'Rajasthan': ('arid', 'Irrigated eastern districts may have different soils.'),
    'Sikkim': ('mountain', 'Soil varies considerably by altitude.'),
    'Tamil Nadu': ('red_yellow', 'Black, alluvial and coastal soils also occur.'),
    'Telangana': ('red_yellow', 'Black soils are common in several districts.'),
    'Tripura': ('red_yellow', 'Hill and valley soils differ.'),
    'Uttar Pradesh': ('alluvial', 'Bundelkhand and other districts have different soils.'),
    'Uttarakhand': ('mountain', 'Terai plains differ from hill soils.'),
    'West Bengal': ('alluvial', 'Lateritic western districts and coastal soils differ.'),
    'Andaman and Nicobar Islands': ('laterite', 'Island soils vary by location.'),
    'Chandigarh': ('alluvial', 'Field-level soil testing is still recommended.'),
    'Dadra and Nagar Haveli and Daman and Diu': ('black', 'Soil varies across this territory.'),
    'Delhi': ('alluvial', 'Urban and local field conditions vary.'),
    'Jammu and Kashmir': ('mountain', 'Valley and high-altitude soils differ.'),
    'Ladakh': ('arid', 'Soil varies with altitude and irrigation.'),
    'Lakshadweep': ('laterite', 'Island soils vary by location.'),
    'Puducherry': ('red_yellow', 'Coastal and alluvial soils also occur.'),
}

SOIL_LABELS = dict(SOIL_TYPE_CHOICES)


def suggest_soil_type(city, state):
    if not state or state not in STATE_SOIL_HINTS:
        return None
    soil_code, note = STATE_SOIL_HINTS[state]
    city_label = city.strip() if city and city.strip() else state
    return {
        'soil_code': soil_code,
        'soil_label': SOIL_LABELS[soil_code],
        'location': f'{city_label}, {state}' if city_label != state else state,
        'note': note,
    }
