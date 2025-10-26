from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class WeatherData:
    city: str
    temperature: float
    description: str
    icon: str


class WeatherAPIError(RuntimeError):
    pass


def _cache_key(city: str) -> str:
    return f"weather:{city.lower()}"


def fetch_weather(city: str) -> WeatherData:
    city = city.strip()
    if not city:
        raise WeatherAPIError('City cannot be empty')

    if not settings.WEATHER_API_KEY:
        raise WeatherAPIError('Weather API key is not configured')

    cached = cache.get(_cache_key(city))
    if cached:
        return WeatherData(**cached)

    params = {
        'q': city,
        'appid': settings.WEATHER_API_KEY,
        'units': settings.WEATHER_UNITS,
        'lang': 'en',
    }

    try:
        response = requests.get(settings.WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:  # pragma: no cover - network
        logger.exception('Weather API error: %s', exc)
        raise WeatherAPIError('Failed to fetch weather data') from exc

    payload: dict[str, Any] = response.json()
    weather_info = payload.get('weather', [{}])[0]
    main_info = payload.get('main', {})

    data = WeatherData(
        city=payload.get('name') or city,
        temperature=float(main_info.get('temp', 0.0)),
        description=weather_info.get('description', 'N/A').capitalize(),
        icon=weather_info.get('icon', ''),
    )

    cache.set(_cache_key(city), data.__dict__, timeout=600)
    return data
