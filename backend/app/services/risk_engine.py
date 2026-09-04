"""
NER Landslide Sentinel — Risk Engine & Early Warning Service
Provides transparent, explainable, and multi-factor landslide risk assessment logic.
"""

import math
from typing import Dict, Any, List, Optional
from app.config import (
    RISK_WEIGHT_RAINFALL,
    RISK_WEIGHT_SLOPE,
    RISK_WEIGHT_HISTORICAL,
    RISK_WEIGHT_ENVIRONMENT,
    RAINFALL_24H_MAX_MM,
    RAINFALL_7D_MAX_MM,
    SLOPE_MAX_DEG,
    RISK_THRESHOLD_MODERATE,
    RISK_THRESHOLD_HIGH,
    RISK_THRESHOLD_CRITICAL,
)


def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates distance between two lat/lng coordinates in km."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_recommended_action(risk_level: str) -> str:
    """Generates prototype safety advisory based on risk level."""
    if risk_level == "CRITICAL":
        return (
            "CRITICAL EMERGENCY WARNING: High probability of active slope displacement. "
            "Suspend transit on cut-slope corridors. Station SDRF/BRO heavy machinery on standby. "
            "Local authorities should issue immediate civil defense advisories for foothill settlements."
        )
    elif risk_level == "HIGH":
        return (
            "HIGH RISK ADVISORY: Soil saturation high. Increase slope monitoring and station traffic police "
            "at checkposts. Prepare response teams for rapid road clearance in case of debris flow."
        )
    elif risk_level == "MODERATE":
        return (
            "MODERATE WATCH: Monitor weather forecasts and official advisories. "
            "Avoid unnecessary heavy transport through vulnerable hill sectors during intense rainfall."
        )
    else:
        return (
            "LOW RISK / ROUTINE MONITORING: Weather parameters within normal thresholds. "
            "Maintain standard automated sensor & telemetry surveillance."
        )


def calculate_risk_assessment(location: Any, historical_records: Optional[List[Any]] = None) -> Dict[str, Any]:
    """
    Computes a transparent, multi-factor risk assessment for a location.
    
    Weights (Configurable via app.config):
    - Rainfall Trigger: 35%
    - Terrain Slope: 30%
    - Historical Susceptibility: 20%
    - Environmental Factors: 15%
    """
    # Extract location attributes safely (handles SQLAlchemy model or dict)
    loc_id = getattr(location, "id", location.get("id", 0) if isinstance(location, dict) else 0)
    name = getattr(location, "name", location.get("name", "Unknown Location") if isinstance(location, dict) else "Unknown Location")
    state = getattr(location, "state", location.get("state", "") if isinstance(location, dict) else "")
    district = getattr(location, "district", location.get("district", "") if isinstance(location, dict) else "")
    lat = getattr(location, "latitude", location.get("latitude", 0.0) if isinstance(location, dict) else 0.0)
    lng = getattr(location, "longitude", location.get("longitude", 0.0) if isinstance(location, dict) else 0.0)
    elevation = getattr(location, "elevation_m", location.get("elevation_m", 0.0) if isinstance(location, dict) else 0.0)
    slope = getattr(location, "slope_deg", location.get("slope_deg", 0.0) if isinstance(location, dict) else 0.0)
    
    r_1d = getattr(location, "rainfall_1d_mm", location.get("rainfall_1d_mm", 0.0) if isinstance(location, dict) else 0.0)
    r_7d = getattr(location, "rainfall_7d_mm", location.get("rainfall_7d_mm", 0.0) if isinstance(location, dict) else 0.0)
    soil_m = getattr(location, "soil_moisture_percent", location.get("soil_moisture_percent", None) if isinstance(location, dict) else None)

    available_factors = ["24h_rainfall", "7d_rainfall", "slope_deg", "elevation_m"]
    missing_factors = []

    # 1. Factor A: Rainfall Trigger (Max 35.0 points)
    max_rainfall_pts = RISK_WEIGHT_RAINFALL * 100.0  # 35.0
    norm_24h = min(1.0, max(0.0, r_1d / RAINFALL_24H_MAX_MM))
    norm_7d = min(1.0, max(0.0, r_7d / RAINFALL_7D_MAX_MM))
    rainfall_norm = 0.65 * norm_24h + 0.35 * norm_7d
    rainfall_score = round(rainfall_norm * max_rainfall_pts, 1)

    # 2. Factor B: Terrain Slope (Max 30.0 points)
    max_slope_pts = RISK_WEIGHT_SLOPE * 100.0  # 30.0
    norm_slope = min(1.0, max(0.0, slope / SLOPE_MAX_DEG))
    slope_score = round(norm_slope * max_slope_pts, 1)

    # 3. Factor C: Historical Susceptibility (Max 20.0 points)
    max_hist_pts = RISK_WEIGHT_HISTORICAL * 100.0  # 20.0
    nearby_count = 0
    if historical_records:
        for ev in historical_records:
            ev_lat = getattr(ev, "latitude", ev.get("latitude", 0.0) if isinstance(ev, dict) else 0.0)
            ev_lng = getattr(ev, "longitude", ev.get("longitude", 0.0) if isinstance(ev, dict) else 0.0)
            dist_km = calculate_haversine_distance(lat, lng, ev_lat, ev_lng)
            ev_state = getattr(ev, "state", ev.get("state", "") if isinstance(ev, dict) else "")
            ev_district = getattr(ev, "district", ev.get("district", "") if isinstance(ev, dict) else "")
            if dist_km <= 100.0 or (district and ev_district.lower() == district.lower()) or (state and ev_state.lower() == state.lower()):
                nearby_count += 1

    if nearby_count >= 2:
        norm_hist = 1.0
    elif nearby_count == 1:
        norm_hist = 0.70
    else:
        norm_hist = 0.25
    historical_score = round(norm_hist * max_hist_pts, 1)
    available_factors.append("historical_records")

    # 4. Factor D: Environmental Context (Max 15.0 points)
    max_env_pts = RISK_WEIGHT_ENVIRONMENT * 100.0  # 15.0
    if soil_m is not None:
        norm_soil = min(1.0, max(0.0, soil_m / 100.0))
        norm_elev = min(1.0, max(0.0, elevation / 2500.0))
        norm_env = 0.75 * norm_soil + 0.25 * norm_elev
        available_factors.append("soil_moisture_percent")
    else:
        norm_elev = min(1.0, max(0.0, elevation / 2500.0))
        norm_env = norm_elev * 0.60
        missing_factors.append("soil_moisture_percent")

    environment_score = round(norm_env * max_env_pts, 1)

    # Calculate Total Score (Range 0.0 to 100.0)
    raw_total = rainfall_score + slope_score + historical_score + environment_score
    overall_risk_score = round(min(100.0, max(0.0, raw_total)), 1)

    # Classify Risk Level
    if overall_risk_score >= RISK_THRESHOLD_CRITICAL:
        risk_level = "CRITICAL"
    elif overall_risk_score >= RISK_THRESHOLD_HIGH:
        risk_level = "HIGH"
    elif overall_risk_score >= RISK_THRESHOLD_MODERATE:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"

    # Identify Main Contributors
    main_contributors = []
    if r_1d >= 50.0:
        main_contributors.append(f"Heavy 24-hour precipitation ({r_1d} mm)")
    elif r_7d >= 200.0:
        main_contributors.append(f"High accumulated 7-day rainfall ({r_7d} mm)")

    if slope >= 30.0:
        main_contributors.append(f"Steep terrain gradient ({slope}°)")

    if nearby_count > 0:
        main_contributors.append(f"Historical landslide activity nearby ({nearby_count} past event(s))")

    if soil_m and soil_m >= 75.0:
        main_contributors.append(f"High soil moisture saturation ({soil_m}%)")

    if not main_contributors:
        main_contributors.append("Normal terrain and precipitation baseline")

    # Data Completeness Calculation
    completeness_percent = round((len(available_factors) / (len(available_factors) + len(missing_factors))) * 100)

    return {
        "location_id": loc_id,
        "location_name": name,
        "state": state,
        "district": district,
        "latitude": lat,
        "longitude": lng,
        "overall_risk_score": overall_risk_score,
        "risk_level": risk_level,
        "factor_breakdown": {
            "rainfall": {
                "score": rainfall_score,
                "max": max_rainfall_pts,
                "weight_percent": int(RISK_WEIGHT_RAINFALL * 100),
                "raw_24h_mm": r_1d,
                "raw_7d_mm": r_7d,
            },
            "slope": {
                "score": slope_score,
                "max": max_slope_pts,
                "weight_percent": int(RISK_WEIGHT_SLOPE * 100),
                "raw_slope_deg": slope,
            },
            "historical": {
                "score": historical_score,
                "max": max_hist_pts,
                "weight_percent": int(RISK_WEIGHT_HISTORICAL * 100),
                "nearby_events_count": nearby_count,
            },
            "environment": {
                "score": environment_score,
                "max": max_env_pts,
                "weight_percent": int(RISK_WEIGHT_ENVIRONMENT * 100),
                "elevation_m": elevation,
                "soil_moisture_percent": soil_m,
            },
        },
        "main_contributors": main_contributors,
        "data_completeness": {
            "completeness_percent": completeness_percent,
            "available_factors": available_factors,
            "missing_factors": missing_factors,
        },
        "recommended_action": get_recommended_action(risk_level),
    }
