DISEASE_GUIDES = {
    'tomato': [
        {
            'name': 'Early blight',
            'symptoms': {'brown_spots', 'concentric_rings', 'lower_leaves_first'},
            'cause': 'Fungal disease',
            'care': 'Remove badly affected lower leaves, avoid wetting foliage and rotate crops where possible.',
            'pesticide': 'For a confirmed case, ask whether a mancozeb-based protectant is currently registered and labelled for tomato early blight in your state. Rotate modes of action as directed on the label.',
        },
        {
            'name': 'Late blight',
            'symptoms': {'water_soaked', 'white_underside', 'rapid_spread'},
            'cause': 'Oomycete disease',
            'care': 'This can spread quickly in cool, wet weather. Remove infected foliage safely, improve airflow and avoid overhead irrigation.',
            'pesticide': 'Ask a local agriculture officer about a currently registered tomato late-blight product; cymoxanil+mancozeb is one active-ingredient combination used in some regions. Confirm the crop, disease and label before use.',
        },
        {
            'name': 'Bacterial wilt',
            'symptoms': {'whole_plant_wilt', 'green_leaves_wilt', 'brown_vascular_tissue'},
            'cause': 'Bacterial disease',
            'care': 'No reliable spray cures infected plants. Remove affected plants with roots, avoid moving contaminated soil or water, and rotate with non-host crops.',
            'pesticide': 'No pesticide spray cures bacterial wilt. Do not use antibiotics; seek local advice on resistant varieties, clean seedlings and rotation.',
        },
        {
            'name': 'Possible tomato leaf-curl virus',
            'symptoms': {'leaf_curl', 'small_leaves', 'whiteflies'},
            'cause': 'Likely viral; whiteflies may spread it',
            'care': 'Remove severely affected plants after confirmation, control weeds and monitor seedlings and leaf undersides for whiteflies.',
            'pesticide': 'There is no cure for an infected plant. Manage whiteflies only when present, using locally approved integrated pest-management advice; spraying cannot reverse virus symptoms.',
        },
        {
            'name': 'Fruit borer',
            'symptoms': {'fruit_holes', 'frass_on_fruit', 'caterpillar_on_fruit'},
            'cause': 'Insect pest',
            'care': 'Remove bored fruits and scout plants regularly; use pheromone traps and conserve beneficial insects.',
            'pesticide': 'For a confirmed damaging infestation, ask whether emamectin benzoate or chlorantraniliprole is currently registered for tomato fruit borer locally. Follow the exact label and pre-harvest interval.',
        },
    ],
    'wheat': [
        {
            'name': 'Wheat rust (leaf or stripe rust)',
            'symptoms': {'orange_pustules', 'yellow_leaves', 'pustules_rub_off'},
            'cause': 'Fungal disease',
            'care': 'Check whether orange pustules rub off onto white tissue, inspect nearby rows and ask about locally resistant varieties.',
            'pesticide': 'If rust is confirmed and treatment is advised locally, ask about a wheat-labelled triazole fungicide such as propiconazole. Observe label rate, protective equipment and harvest interval.',
        },
        {
            'name': 'Powdery mildew',
            'symptoms': {'white_powder', 'yellow_leaves', 'white_growth_on_stems'},
            'cause': 'Fungal disease',
            'care': 'Confirm the white growth is fungal, improve airflow where possible and avoid excess nitrogen.',
            'pesticide': 'Ask an agriculture officer whether a sulphur- or other mildew fungicide product is registered for wheat in your district; follow the product label.',
        },
        {
            'name': 'Loose smut',
            'symptoms': {'black_powder_ear', 'empty_black_ears', 'black_spores'},
            'cause': 'Seed-borne fungal disease',
            'care': 'Infected heads produce black spores instead of grain. Use certified, disease-free seed and locally recommended resistant varieties next season.',
            'pesticide': 'A foliar spray does not cure infected heads. Ask about approved seed treatment before the next sowing; use only a wheat-seed label product.',
        },
        {
            'name': 'Aphids',
            'symptoms': {'aphids_on_ear', 'sticky_leaves', 'ants_on_plant'},
            'cause': 'Sap-sucking insect pest',
            'care': 'Check colonies on ears and leaves and preserve ladybird beetles and other beneficial insects. Treat only if local economic thresholds are met.',
            'pesticide': 'Do not spray automatically. If a damaging infestation is confirmed, ask your extension officer for a currently registered wheat aphid product and pollinator precautions.',
        },
    ],
    'rice': [
        {
            'name': 'Rice blast',
            'symptoms': {'diamond_lesions', 'grey_lesion_centres', 'neck_rot'},
            'cause': 'Fungal disease',
            'care': 'Scout neighbouring plots early, avoid excessive nitrogen and remove volunteer rice and infected residues where practical.',
            'pesticide': 'For confirmed blast, ask about a rice-labelled tricyclazole product where currently registered. Follow label timing, dose, protective equipment and pre-harvest interval.',
        },
        {
            'name': 'Bacterial leaf blight',
            'symptoms': {'wavy_edges', 'yellowing_from_tip', 'milky_ooze'},
            'cause': 'Bacterial disease',
            'care': 'Avoid moving water or tools from affected to healthy plots, avoid excess nitrogen and confirm with a local extension officer.',
            'pesticide': 'Fungicides do not cure bacterial blight. Do not use antibiotics or pesticide mixtures without explicit local registration and professional advice.',
        },
        {
            'name': 'Sheath blight',
            'symptoms': {'lesions_near_waterline', 'oval_sheath_lesions', 'white_fungal_growth'},
            'cause': 'Fungal disease',
            'care': 'Check lower leaf sheaths near the waterline, avoid dense overgrowth and excessive nitrogen, and confirm the disease before treatment.',
            'pesticide': 'For confirmed sheath blight, ask whether a rice-labelled validamycin or hexaconazole product is currently registered in your state. Use only according to its label.',
        },
        {
            'name': 'Brown spot',
            'symptoms': {'small_brown_spots', 'yellow_halo', 'brown_spots'},
            'cause': 'Fungal disease; stress and nutrition can worsen symptoms',
            'care': 'Check seed quality, drainage and crop nutrition; have leaf symptoms confirmed because nutrient stress can look similar.',
            'pesticide': 'If fungal brown spot is confirmed, ask about a rice-labelled mancozeb product where registered. Correct underlying crop stress as advised.',
        },
        {
            'name': 'Stem borer',
            'symptoms': {'dead_heart', 'white_head', 'bore_hole_stem'},
            'cause': 'Insect pest',
            'care': 'Look for dead central shoots or white empty panicles and bore holes; remove affected tillers where practical and use pheromone monitoring.',
            'pesticide': 'If local scouting confirms damaging stem-borer levels, ask for a currently registered rice product and application timing. Do not spray by symptom alone.',
        },
    ],
    'potato': [
        {
            'name': 'Late blight',
            'symptoms': {'water_soaked', 'white_underside', 'rapid_spread'},
            'cause': 'Oomycete disease',
            'care': 'Remove infected foliage safely, avoid overhead watering and inspect nearby plants because this disease can spread quickly.',
            'pesticide': 'Ask local extension services for a potato-labelled late-blight product; cymoxanil+mancozeb may be an option where currently registered. Confirm label and harvest interval.',
        },
        {
            'name': 'Early blight',
            'symptoms': {'brown_spots', 'concentric_rings', 'lower_leaves_first'},
            'cause': 'Fungal disease',
            'care': 'Remove badly affected leaves, avoid wet foliage, rotate crops and maintain balanced plant nutrition.',
            'pesticide': 'For confirmed early blight, ask whether a mancozeb-based protectant is currently registered for potato in your area; follow the label.',
        },
        {
            'name': 'Bacterial wilt',
            'symptoms': {'whole_plant_wilt', 'green_leaves_wilt', 'brown_vascular_tissue'},
            'cause': 'Bacterial disease',
            'care': 'No reliable spray cures infected plants. Remove affected plants and tubers, avoid moving contaminated soil or water and rotate crops.',
            'pesticide': 'No spray cures bacterial wilt. Use clean seed tubers and locally recommended rotation; do not use antibiotics.',
        },
    ],
    'maize': [
        {
            'name': 'Northern corn leaf blight',
            'symptoms': {'elongated_lesions', 'grey_tan_centres', 'brown_spots'},
            'cause': 'Fungal disease',
            'care': 'Scout the whole field, remove volunteer maize and choose locally resistant varieties for future planting.',
            'pesticide': 'Only consider a maize-labelled fungicide after local confirmation; verify the target disease and product label with an agriculture officer.',
        },
        {
            'name': 'Fall armyworm',
            'symptoms': {'chewed_leaves', 'insect_frass', 'windowpane_damage'},
            'cause': 'Insect pest',
            'care': 'Inspect whorls for larvae and fresh frass, especially early in the morning; hand-pick small infestations where practical and conserve beneficial insects.',
            'pesticide': 'For confirmed damaging infestation, ask whether a maize-labelled chlorantraniliprole or emamectin benzoate product is currently registered locally. Follow label and avoid spraying beneficial insects.',
        },
        {
            'name': 'Maize stem borer',
            'symptoms': {'dead_heart', 'bore_hole_stem', 'frass_in_whorl'},
            'cause': 'Insect pest',
            'care': 'Look for dead hearts, stem holes and fresh frass; remove affected shoots where practical and consult local scouting advice.',
            'pesticide': 'If local scouting confirms damaging levels, ask for a currently registered maize stem-borer product and the correct crop-stage timing.',
        },
    ],
    'chickpea': [
        {
            'name': 'Fusarium wilt',
            'symptoms': {'whole_plant_wilt', 'yellowing_one_side', 'brown_vascular_tissue'},
            'cause': 'Soil-borne fungal disease',
            'care': 'Remove wilted plants, avoid moving infested soil and use resistant varieties and seed from a reliable source.',
            'pesticide': 'A foliar pesticide cannot cure wilted plants. Ask locally about resistant varieties, seed treatment and rotation before the next crop.',
        },
        {
            'name': 'Ascochyta blight',
            'symptoms': {'dark_stem_lesions', 'brown_spots', 'black_dots_lesions'},
            'cause': 'Fungal disease',
            'care': 'Remove heavily infected debris, avoid working in wet plants and use disease-free seed and locally adapted varieties.',
            'pesticide': 'For confirmed blight, ask whether a mancozeb-based fungicide is registered for chickpea in your area. Follow the crop label and local advisory.',
        },
        {
            'name': 'Gram pod borer',
            'symptoms': {'fruit_holes', 'caterpillar_on_pod', 'frass_on_pod'},
            'cause': 'Insect pest',
            'care': 'Scout flowers and pods, remove caterpillars where practical, and use pheromone traps and bird perches as local IPM guidance recommends.',
            'pesticide': 'If a damaging infestation is confirmed, ask about a currently registered chickpea pod-borer product such as emamectin benzoate or chlorantraniliprole. Check label and harvest interval.',
        },
    ],
    'cotton': [
        {
            'name': 'Cotton leaf-curl disease',
            'symptoms': {'leaf_curl', 'thickened_veins', 'leaf_cup'},
            'cause': 'Viral disease often spread by whiteflies',
            'care': 'Remove severely affected plants after confirmation, control weeds and monitor leaf undersides for whiteflies.',
            'pesticide': 'No pesticide cures the virus. Manage whiteflies only when present and with locally approved integrated pest management; spraying cannot reverse infected plants.',
        },
        {
            'name': 'Bacterial blight (angular leaf spot)',
            'symptoms': {'angular_water_soaked_spots', 'dark_veins', 'black_stem_lesions'},
            'cause': 'Bacterial disease',
            'care': 'Use clean seed, avoid moving infected residue between fields and seek local confirmation.',
            'pesticide': 'There is no curative spray recommendation here. Do not use antibiotics; ask about clean seed, resistant varieties and locally approved seed treatment.',
        },
        {
            'name': 'Cotton bollworm',
            'symptoms': {'fruit_holes', 'caterpillar_on_boll', 'frass_on_boll'},
            'cause': 'Insect pest',
            'care': 'Scout squares and bolls, identify the caterpillar before acting, and conserve natural enemies.',
            'pesticide': 'Treat only after local threshold-based confirmation. Ask whether an active ingredient such as emamectin benzoate is currently registered for the identified bollworm and cotton; follow label and resistance guidance.',
        },
        {
            'name': 'Jassid or sucking-pest injury',
            'symptoms': {'leaf_edges_brown', 'downward_leaf_curl', 'small_sucking_insects'},
            'cause': 'Sap-sucking insect pest',
            'care': 'Check leaf undersides and field distribution; preserve beneficial insects and confirm the pest before treatment.',
            'pesticide': 'Do not spray by leaf symptoms alone. Ask local extension for threshold-based, currently registered cotton advice and pollinator precautions.',
        },
    ],
    'sugarcane': [
        {
            'name': 'Red rot',
            'symptoms': {'red_pith_white_patches', 'red_stalk_tissue', 'sour_stalk_smell'},
            'cause': 'Fungal disease of stalks',
            'care': 'Split a stalk to inspect internal tissue; remove diseased clumps and do not use infected setts for planting.',
            'pesticide': 'No spray reliably cures infected stalks. Use clean setts, resistant varieties and locally advised sanitation.',
        },
        {
            'name': 'Smut',
            'symptoms': {'black_whip', 'whip_from_shoot', 'thin_grassy_stalks'},
            'cause': 'Fungal disease',
            'care': 'Remove and safely destroy smut whips before spores spread; use clean planting material and resistant varieties.',
            'pesticide': 'A foliar spray does not cure smut. Ask about locally approved sett treatment and resistant varieties before planting.',
        },
        {
            'name': 'Early shoot borer',
            'symptoms': {'dead_heart', 'bore_hole_stem', 'frass_in_whorl'},
            'cause': 'Insect pest',
            'care': 'Check young shoots for dead hearts and bore holes, remove affected shoots where practical and follow local field sanitation advice.',
            'pesticide': 'If scouting confirms damaging levels, ask a local sugarcane extension officer for a currently registered product and timing; do not spray by symptom alone.',
        },
    ],
}


def screen_crop_symptoms(crop, selected_symptoms):
    selected = set(selected_symptoms)
    if len(selected) < 2:
        return []

    candidates = []
    for disease in DISEASE_GUIDES.get(crop, []):
        matched = disease['symptoms'] & selected
        if len(matched) >= 2:
            candidates.append({
                **disease,
                'match_count': len(matched),
                'matched_symptoms': matched,
            })

    return sorted(candidates, key=lambda candidate: candidate['match_count'], reverse=True)
