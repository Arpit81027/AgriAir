import json
import hashlib
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.core.cache import cache


class WeatherServiceError(Exception):
    pass


def _get_json(url):
    request = Request(url, headers={'User-Agent': 'AgriAir/1.0'})
    try:
        with urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode('utf-8'))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise WeatherServiceError('Weather service is temporarily unavailable. Please try again later.') from exc


def _weather_description(code):
    if code == 0:
        return 'Clear sky'
    if code in (1, 2):
        return 'Mainly clear / partly cloudy'
    if code == 3:
        return 'Overcast'
    if code in (45, 48):
        return 'Fog'
    if code in (51, 53, 55, 56, 57):
        return 'Drizzle'
    if code in (61, 63, 65, 66, 67):
        return 'Rain'
    if code in (71, 73, 75, 77):
        return 'Snow / ice'
    if code in (80, 81, 82):
        return 'Rain showers'
    if code in (85, 86):
        return 'Snow showers'
    if code in (95, 96, 99):
        return 'Thunderstorm'
    return 'Conditions unavailable'


def get_local_weather(city, state):
    location = ', '.join(part.strip() for part in (city, state) if part and part.strip())
    if not location:
        return None, 'Add your city and state in Farm Profile to see local weather.'

    cache_key = f'local-weather:{hashlib.sha256(location.casefold().encode()).hexdigest()}'
    cached = cache.get(cache_key)
    if cached:
        return cached, None

    geocode_query = urlencode({'name': location, 'count': 1, 'language': 'en', 'format': 'json'})
    geocoding = _get_json(f'https://geocoding-api.open-meteo.com/v1/search?{geocode_query}')
    results = geocoding.get('results') or []
    if not results:
        return None, f'Could not find weather coordinates for {location}. Check your city/state in Farm Profile.'

    place = results[0]
    if 'latitude' not in place or 'longitude' not in place:
        raise WeatherServiceError('Weather service could not resolve the farm location. Check your city/state and try again.')
    weather_query = urlencode({
        'latitude': place['latitude'],
        'longitude': place['longitude'],
        'current': 'temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m',
        'daily': 'precipitation_sum,temperature_2m_max,temperature_2m_min',
        'forecast_days': 2,
        'timezone': 'auto',
    })
    forecast = _get_json(f'https://api.open-meteo.com/v1/forecast?{weather_query}')
    current = forecast.get('current')
    daily = forecast.get('daily')
    if not current or not daily or not daily.get('time'):
        raise WeatherServiceError('Weather service returned incomplete forecast data. Please try again later.')

    rainfall = daily.get('precipitation_sum') or []
    upcoming_rain = rainfall[0] if rainfall else None
    rain_guidance = (
        'Rain is forecast today; check the root-zone soil before irrigating.'
        if upcoming_rain is not None and upcoming_rain >= 5
        else 'No heavy rain is currently forecast today; decide irrigation from crop stage and root-zone soil.'
    )

    weather = {
        'place': ', '.join(part for part in (place.get('name'), place.get('admin1')) if part),
        'time': current.get('time'),
        'temperature': current.get('temperature_2m'),
        'humidity': current.get('relative_humidity_2m'),
        'description': _weather_description(current.get('weather_code')),
        'wind_speed': current.get('wind_speed_10m'),
        'current_rain': current.get('precipitation'),
        'today_rain': upcoming_rain,
        'tomorrow_rain': rainfall[1] if len(rainfall) > 1 else None,
        'rain_guidance': rain_guidance,
    }
    cache.set(cache_key, weather, timeout=600)
    return weather, None
