"""
Live model-based weather context from Open-Meteo for the prototype's monitored coordinates.
This endpoint deliberately does NOT alter demo risk scores or issue warnings.
"""
from datetime import datetime, timezone
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException
from app.database.database import SessionLocal
from app.database.models import RiskLocation

router = APIRouter(prefix="/api/weather", tags=["Weather Context"])
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


@router.get("/live")
def get_weather_context() -> dict[str, Any]:
    """Fetch current/forecast model weather for monitored coordinates, without changing risk records."""
    db = SessionLocal()
    try:
        locations = db.query(RiskLocation).order_by(RiskLocation.id.asc()).all()
        if not locations:
            return {
                "status": "no_locations",
                "source": "Open-Meteo Forecast API",
                "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "notice": "Weather context only; not an official warning and not used to calculate demo risk scores.",
                "locations": [],
            }

        params = {
            "latitude": ",".join(str(loc.latitude) for loc in locations),
            "longitude": ",".join(str(loc.longitude) for loc in locations),
            "current": "temperature_2m,precipitation",
            "hourly": "precipitation",
            "daily": "precipitation_sum",
            "past_days": 1,
            "forecast_days": 1,
            "timezone": "auto",
        }
        try:
            response = httpx.get(OPEN_METEO_URL, params=params, timeout=12.0)
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise HTTPException(
                status_code=502,
                detail="Weather provider is temporarily unavailable. Existing demo scores were not changed.",
            ) from exc

        # Open-Meteo returns a list when multiple coordinates are requested.
        items = payload if isinstance(payload, list) else [payload]
        by_coords = {}
        for item in items:
            key = (round(float(item.get("latitude", 0)), 3), round(float(item.get("longitude", 0)), 3))
            by_coords[key] = item

        result = []
        for loc in locations:
            item = by_coords.get((round(float(loc.latitude), 3), round(float(loc.longitude), 3)))
            if not item:
                result.append({
                    "location_id": loc.id,
                    "location_name": loc.name,
                    "state": loc.state,
                    "status": "unavailable",
                })
                continue

            current = item.get("current") or {}
            daily = item.get("daily") or {}
            hourly = item.get("hourly") or {}
            precip_times = hourly.get("time") or []
            precip_values = hourly.get("precipitation") or []
            recent_24h = [
                float(value) for time_value, value in zip(precip_times, precip_values)
                if value is not None and time_value <= str(current.get("time", "")) and
                time_value >= str(current.get("time", ""))[:10] + "T00:00"
            ]
            result.append({
                "location_id": loc.id,
                "location_name": loc.name,
                "state": loc.state,
                "status": "available",
                "latitude": item.get("latitude"),
                "longitude": item.get("longitude"),
                "timezone": item.get("timezone"),
                "current_time": current.get("time"),
                "temperature_2m_c": current.get("temperature_2m"),
                "current_precipitation_mm": current.get("precipitation"),
                "hourly_precipitation_since_local_midnight_mm": round(sum(recent_24h), 1) if recent_24h else None,
                "daily_precipitation_forecast_mm": (daily.get("precipitation_sum") or [None])[0],
                "units": {
                    "temperature": (item.get("current_units") or {}).get("temperature_2m", "°C"),
                    "precipitation": (item.get("current_units") or {}).get("precipitation", "mm"),
                },
            })

        return {
            "status": "ok",
            "source": "Open-Meteo Forecast API",
            "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
            "notice": "Model-based weather context, not a verified station observation or official warning. It does not change the demo risk scores.",
            "locations": result,
        }
    finally:
        db.close()
