from decimal import Decimal


# Regional package-of-practice references, not universal prescriptions.
# Rates are kg of nutrient per acre converted from the cited source where noted.
FERTILIZER_REFERENCES = {
    'wheat': {
        'region_state': 'Punjab',
        'region': 'Punjab, PAU Rabi 2025–26; medium-fertility soils',
        'source_name': 'PAU Package of Practices for Crops of Punjab, Rabi 2025–26',
        'source_url': 'https://pau.edu/content/ccil/pf/pp_rabi.pdf',
        'variants': [
            {
                'label': 'General reference',
                'n': Decimal('50'),
                'p': Decimal('25'),
                'k': Decimal('12'),
                'p_label': 'P₂O₅',
                'k_label': 'K₂O, low-K soil reference',
                'timing': 'Apply P₂O₅ (and K₂O if needed) at sowing. Split N between first and second irrigation; if the second irrigation is delayed, PAU advises the second N split at 55 days after sowing.',
            },
            {
                'label': 'Selected Punjab districts with low K',
                'n': Decimal('50'),
                'p': Decimal('25'),
                'k': Decimal('24'),
                'p_label': 'P₂O₅',
                'k_label': 'K₂O',
                'districts': 'Gurdaspur, Hoshiarpur, Rupnagar and SBS Nagar',
                'timing': 'Apply P₂O₅ and K₂O at sowing. Split N between first and second irrigation; if the second irrigation is delayed, use the PAU 55-days-after-sowing timing.',
            },
        ],
    },
    'rice': {
        'region_state': 'Punjab',
        'region': 'Punjab, PAU Kharif 2026',
        'source_name': 'PAU Package of Practices for Crops of Punjab, Kharif 2026',
        'source_url': 'https://pau.edu/content/ccil/pf/pp_kharif.pdf',
        'variants': [
            {
                'label': 'PR 132',
                'n': Decimal('31.5'),
                'p': Decimal('12'),
                'k': Decimal('12'),
                'p_label': 'P₂O₅; only if soil test indicates need',
                'k_label': 'K₂O; only if soil test indicates need',
                'timing': 'Apply needed P₂O₅/K₂O before puddling. Split N into three equal parts: up to 7 and 21 days after transplanting, then 35 days after transplanting.',
            },
            {
                'label': 'Other varieties listed by PAU',
                'n': Decimal('42'),
                'p': Decimal('12'),
                'k': Decimal('12'),
                'p_label': 'P₂O₅; only if soil test indicates need',
                'k_label': 'K₂O; only if soil test indicates need',
                'timing': 'Apply needed P₂O₅/K₂O before puddling. Split N into three equal parts: up to 7 and 21 days after transplanting, then 42 days after transplanting.',
            },
        ],
        'note': 'PAU says apply P/K only where soil tests show deficiency; omit P if the preceding wheat crop received its recommended P.',
    },
    'maize': {
        'region_state': 'Punjab',
        'region': 'Punjab, PAU Kharif 2026',
        'source_name': 'PAU Package of Practices for Crops of Punjab, Kharif 2026',
        'source_url': 'https://pau.edu/content/ccil/pf/pp_kharif.pdf',
        'variants': [
            {
                'label': 'Listed hybrids / sweet corn',
                'n': Decimal('50'),
                'p': Decimal('24'),
                'k': Decimal('12'),
                'p_label': 'P₂O₅; conditional on previous crop/soil test',
                'k_label': 'K₂O; only if soil test indicates need',
                'timing': 'Apply one-third N at sowing, one-third at knee-high, and one-third before tasseling. Apply P/K at sowing only when locally advised.',
            },
            {
                'label': 'PMH 2, JC 4 and pearl popcorn',
                'n': Decimal('35'),
                'p': Decimal('12'),
                'k': Decimal('8'),
                'p_label': 'P₂O₅; conditional on previous crop/soil test',
                'k_label': 'K₂O; only if soil test indicates need',
                'timing': 'Apply one-third N at sowing, one-third at knee-high, and one-third before tasseling. Apply P/K at sowing only when locally advised.',
            },
        ],
        'note': 'PAU says omit P where the preceding wheat received its recommended P; apply K only where soil tests show deficiency.',
    },
    'tomato': {
        'region_state': 'Tamil Nadu',
        'region': 'Tamil Nadu, TNAU tomato hybrids under drip fertigation',
        'source_name': 'TNAU Agritech Portal, Fertigation schedule for tomato hybrids',
        'source_url': 'https://agritech.tnau.ac.in/horticulture/horti_vegetables_tomato_fertigation.html',
        'variants': [],
        'note': 'The source table notation and basal-vs-fertigation quantities are ambiguous, so AgriAir does not calculate or display a numeric dose. Ask your local KVK/agriculture officer for a clear soil-test-based recommendation.',
    },
    'potato': {
        'region_state': 'Tamil Nadu',
        'region': 'Tamil Nadu, TNAU potato reference',
        'source_name': 'TNAU Agritech Portal, Potato',
        'source_url': 'https://agritech.tnau.ac.in/horticulture/horti_vegetables_potato.html',
        'variants': [
            {
                'label': 'TNAU source notation (N:P:K)',
                'n': Decimal('48.6'),
                'p': Decimal('97.1'),
                'k': Decimal('48.6'),
                'p_label': 'P, source notation',
                'k_label': 'K, source notation',
                'timing': 'TNAU describes 50% as basal and the balance as top dressing at 30 days after sowing. The source labels P and K without oxide units; do not treat these numbers as P₂O₅/K₂O or product/bag rates.',
            },
        ],
        'note': 'Converted from TNAU 120 kg N, 240 kg P and 120 kg K/ha. Source is regional and does not specify oxide notation for P/K.',
    },
    'chickpea': {
        'region_state': 'Tamil Nadu',
        'region': 'Tamil Nadu, TNAU Bengalgram',
        'source_name': 'TNAU Agritech Portal, Bengalgram management',
        'source_url': 'https://agritech.tnau.ac.in/agriculture/CropProduction/Pulses/pulses_bengalgram.html',
        'variants': [
            {
                'label': 'Rainfed',
                'n': Decimal('5.1'),
                'p': Decimal('10.1'),
                'k': Decimal('5.1'),
                'p_label': 'P₂O₅',
                'k_label': 'K₂O',
                'timing': 'Apply the listed nutrients basally before sowing.',
            },
            {
                'label': 'Irrigated',
                'n': Decimal('10.1'),
                'p': Decimal('20.2'),
                'k': Decimal('10.1'),
                'p_label': 'P₂O₅',
                'k_label': 'K₂O',
                'timing': 'Apply the listed nutrients basally before sowing.',
            },
        ],
        'note': 'TNAU rates are for Bengalgram in Tamil Nadu. Sulphur is also listed separately in the source; soil-test and local guidance are required.',
    },
    'cotton': {
        'region_state': 'Punjab',
        'region': 'Punjab, PAU Kharif 2026; medium-fertility soils',
        'source_name': 'PAU Package of Practices for Crops of Punjab, Kharif 2026',
        'source_url': 'https://pau.edu/content/ccil/pf/pp_kharif.pdf',
        'variants': [
            {
                'label': 'Non-Bt',
                'n': Decimal('30'),
                'p': Decimal('12'),
                'k': None,
                'p_label': 'P₂O₅',
                'k_label': 'K₂O: soil-test/local advice',
                'timing': 'Drill P₂O₅ at sowing; apply half the N at thinning and the rest at flowering.',
            },
            {
                'label': 'Bt',
                'n': Decimal('37'),
                'p': Decimal('12'),
                'k': None,
                'p_label': 'P₂O₅',
                'k_label': 'K₂O: soil-test/local advice',
                'timing': 'Drill P₂O₅ at sowing; apply half the N at thinning and the rest at flowering.',
            },
            {
                'label': 'Bt hybrid',
                'n': Decimal('55'),
                'p': Decimal('12'),
                'k': None,
                'p_label': 'P₂O₅',
                'k_label': 'K₂O: soil-test/local advice',
                'timing': 'Drill P₂O₅ at sowing; apply half the N at thinning and the rest at flowering.',
            },
        ],
        'note': 'PAU notes K/product decisions for light soils separately; no blanket K₂O nutrient rate is inferred here.',
    },
    'sugarcane': {
        'region_state': 'Tamil Nadu',
        'region': 'Tamil Nadu, TNAU soil application; water-belt and crop-purpose dependent',
        'source_name': 'TNAU Agritech Portal, Sugarcane crop management',
        'source_url': 'https://agritech.tnau.ac.in/agriculture/sugarcrops_sugarcane.html',
        'variants': [
            {
                'label': 'Assured water / coastal and flow-irrigated belts',
                'n': Decimal('111.3'),
                'p': None,
                'k': Decimal('45.5'),
                'p_label': 'P₂O₅: soil-test/local basal advice',
                'k_label': 'K₂O',
                'timing': 'Apply N and K₂O in three equal splits at 30, 60 and 90 days after planting.',
            },
            {
                'label': 'Lift-irrigated / water-scarcity belts',
                'n': Decimal('91.1'),
                'p': None,
                'k': Decimal('45.5'),
                'p_label': 'P₂O₅: soil-test/local basal advice',
                'k_label': 'K₂O',
                'timing': 'Apply N and K₂O in three equal splits at 30, 60 and 90 days after planting.',
            },
            {
                'label': 'Jaggery areas',
                'n': Decimal('70.8'),
                'p': None,
                'k': Decimal('45.5'),
                'p_label': 'P₂O₅: soil-test/local basal advice',
                'k_label': 'K₂O',
                'timing': 'Apply N and K₂O in three equal splits at 30, 60 and 90 days after planting.',
            },
        ],
        'note': 'Rates converted from TNAU recommendations per hectare; choose the matching water belt and crop purpose. Do not combine with another blanket dose.',
    },
}


def get_fertilizer_reference(crop, area_acres, farm_state=''):
    reference = FERTILIZER_REFERENCES.get(crop.name)
    if not reference:
        return None

    area_acres = Decimal(str(area_acres)) if area_acres is not None else None
    variants = []
    for variant in reference['variants']:
        total = None
        if area_acres is not None:
            total = {
                nutrient: value * area_acres if value is not None else None
                for nutrient, value in (
                    ('n', variant['n']),
                    ('p', variant['p']),
                    ('k', variant['k']),
                )
            }
        variants.append({**variant, 'total': total})

    return {
        **reference,
        'region_matches': farm_state.strip().casefold() == reference['region_state'].casefold(),
        'variants': variants,
    }
