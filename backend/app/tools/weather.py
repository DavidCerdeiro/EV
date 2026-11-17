import asyncio
import logging
from datetime import date
from functools import lru_cache
from typing import Optional

import httpx
from geopy.geocoders import Nominatim
from langchain_core.tools import tool

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)

_TIMEOUT = httpx.Timeout(10.0)
_WEATHER_URL = "https://weather.googleapis.com/v1/"
_geolocator = Nominatim(user_agent="ev-voice-assistant/1.0", timeout=10)
_MAX_FORECAST_DAYS = 7
_WEEKDAYS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


class LocationError(Exception):
    """No se pudo determinar la ubicación. El mensaje es apto para el usuario."""


@lru_cache(maxsize=128)
def _geocode(location: str):
    # Cacheado: Nominatim limita a una petición por segundo
    return _geolocator.geocode(location, language="es")


def _get_user_city_sync() -> Optional[str]:
    """Extrae la ciudad del usuario desde la BD."""
    db_generator = get_db()
    db = next(db_generator)
    try:
        user = db.query(User).first()
        if user and user.city_name:
            return user.city_name
        return None
    except Exception as e:
        logger.error(f"Error accediendo a la BD para obtener ciudad: {e}")
        return None
    finally:
        # Cierra la sesión limpiamente avanzando el generador de FastAPI
        try:
            next(db_generator)
        except StopIteration:
            pass


async def _resolve_coordinates(location: Optional[str]) -> tuple[float, float, str]:
    """
    Obtiene coordenadas y devuelve (latitud, longitud, ciudad_resuelta).
    Si location es None, extrae el dato de la base de datos.
    """
    actual_location = location

    if not actual_location:
        # Ejecutamos la consulta síncrona en un thread para no bloquear el event loop
        db_city = await asyncio.to_thread(_get_user_city_sync)
        # Hacemos fallback al nombre por defecto si la BD estuviese vacía
        actual_location = db_city

    place = await asyncio.to_thread(_geocode, actual_location)
    if place is None:
        raise LocationError(f"No encuentro el lugar {actual_location}.")
        
    return place.latitude, place.longitude, actual_location


async def _call_weather_api(endpoint: str, lat: float, lon: float, **extra) -> dict:
    async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
        r = await client.get(
            _WEATHER_URL + endpoint,
            params={
                "location.latitude": lat,
                "location.longitude": lon,
                "languageCode": "es",
                **extra,
            },
            headers={"X-Goog-Api-Key": settings.GOOGLE_WEATHER_API_KEY},
        )
        r.raise_for_status()
        return r.json()


@tool
async def get_current_weather(location: Optional[str] = None) -> str:
    """Obtiene el tiempo actual: condición, temperatura, sensación térmica,
    humedad y viento. Úsala solo cuando el usuario pregunte cómo está el
    tiempo ahora mismo.

    Args:
        location: Nombre de la ciudad o lugar, por ejemplo "Cádiz". Si el
            usuario no menciona ningún lugar, déjalo vacío para usar su
            ubicación habitual.
    """
    try:
        lat, lon, resolved_loc = await _resolve_coordinates(location)
    except LocationError as e:
        return str(e)
    except Exception:
        logger.exception("Fallo al resolver la ubicación")
        return "No he podido determinar la ubicación."

    try:
        d = await _call_weather_api("currentConditions:lookup", lat, lon)
    except httpx.HTTPError:
        logger.exception("Fallo al consultar la API del tiempo")
        return "No he podido consultar el tiempo en este momento."

    summary = {
        "lugar": resolved_loc, # Inyectamos directamente el nombre final validado
        "condicion": d.get("weatherCondition", {}).get("description", {}).get("text"),
        "temperatura_grados_celsius": d.get("temperature", {}).get("degrees"),
        "sensacion_termica_grados_celsius": d.get("feelsLikeTemperature", {}).get("degrees"),
        "humedad_relativa_porcentaje": d.get("relativeHumidity"),
        "viento_kilometros_por_hora": d.get("wind", {}).get("speed", {}).get("value"),
    }
    return str(summary)


@tool
async def get_lookup_weather(
    location: Optional[str] = None,
    start_day: int = 0,
    days: int = 1,
) -> str:
    """Obtiene la previsión del tiempo para días futuros: condición,
    temperaturas máxima y mínima, probabilidad de lluvia y viento.

    Args:
        location: Nombre de la ciudad o lugar, por ejemplo "Cádiz". Si el
            usuario no menciona ningún lugar, déjalo vacío.
        start_day: Primer día que se quiere, contando desde hoy. 0 es hoy,
            1 es mañana, 2 es pasado mañana, y así sucesivamente.
        days: Cuántos días seguidos se quieren a partir de start_day.
            Por ejemplo, para solo mañana: start_day=1 y days=1.
            Para los próximos tres días: start_day=0 y days=3.
    """
    start_day = max(0, start_day)
    days = max(1, days)
    total = start_day + days
    if total > _MAX_FORECAST_DAYS:
        return f"Solo puedo dar la previsión de los próximos {_MAX_FORECAST_DAYS} días."

    try:
        # Desempaquetamos los 3 valores
        lat, lon, resolved_loc = await _resolve_coordinates(location)
    except LocationError as e:
        return str(e)
    except Exception:
        logger.exception("Fallo al resolver la ubicación")
        return "No he podido determinar la ubicación."

    try:
        d = await _call_weather_api(
            "forecast/days:lookup", lat, lon, days=total, pageSize=total
        )
    except httpx.HTTPError:
        logger.exception("Fallo al consultar la API del tiempo")
        return "No he podido consultar el tiempo en este momento."

    forecast_days = d.get("forecastDays", [])
    daily = []
    for offset, day_data in enumerate(forecast_days):
        if offset < start_day or offset >= total:
            continue

        di = day_data.get("displayDate", {})
        try:
            weekday = _WEEKDAYS[date(di["year"], di["month"], di["day"]).weekday()]
        except (KeyError, ValueError):
            weekday = None

        relative = {0: "hoy", 1: "mañana", 2: "pasado mañana"}.get(offset)
        label = f"{relative}, {weekday}" if relative and weekday else (relative or weekday)

        daytime = day_data.get("daytimeForecast", {})
        daily.append({
            "dia": label,
            "condicion": daytime.get("weatherCondition", {}).get("description", {}).get("text"),
            "temperatura_maxima_grados_celsius": day_data.get("maxTemperature", {}).get("degrees"),
            "temperatura_minima_grados_celsius": day_data.get("minTemperature", {}).get("degrees"),
            "probabilidad_lluvia_porcentaje": daytime.get("precipitation", {}).get("probability", {}).get("percent"),
            "viento_kilometros_por_hora": daytime.get("wind", {}).get("speed", {}).get("value"),
        })

    if not daily:
        return "No he obtenido datos de previsión para esos días."

    return str({"lugar": resolved_loc, "prevision": daily})

WEATHER_TOOLS = [get_current_weather, get_lookup_weather]