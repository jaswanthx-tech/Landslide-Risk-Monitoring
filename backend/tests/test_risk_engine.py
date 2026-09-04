"""
Unit Test Suite for Landslide Risk Engine (Phase 7 Validation)
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.risk_engine import calculate_risk_assessment


def test_low_risk_scenario():
    """Scenario 1: Gentle slope, zero rainfall, no history."""
    loc = {
        "id": 1,
        "name": "Flat Valley",
        "state": "Assam",
        "district": "Kamrup",
        "latitude": 26.1,
        "longitude": 91.7,
        "elevation_m": 50.0,
        "slope_deg": 5.0,
        "rainfall_1d_mm": 0.0,
        "rainfall_7d_mm": 5.0,
        "soil_moisture_percent": 20.0,
    }
    result = calculate_risk_assessment(loc, historical_records=[])
    print("[TEST 1] Low Risk Scenario:", result["overall_risk_score"], result["risk_level"])
    assert result["risk_level"] == "LOW"
    assert result["overall_risk_score"] < 25.0
    assert 0.0 <= result["overall_risk_score"] <= 100.0


def test_moderate_risk_scenario():
    """Scenario 2: Moderate slope and moderate rainfall."""
    loc = {
        "id": 2,
        "name": "Moderate Hill",
        "state": "Nagaland",
        "district": "Kohima",
        "latitude": 25.6,
        "longitude": 94.1,
        "elevation_m": 800.0,
        "slope_deg": 22.0,
        "rainfall_1d_mm": 35.0,
        "rainfall_7d_mm": 90.0,
        "soil_moisture_percent": 50.0,
    }
    result = calculate_risk_assessment(loc, historical_records=[])
    print("[TEST 2] Moderate Risk Scenario:", result["overall_risk_score"], result["risk_level"])
    assert result["risk_level"] == "MODERATE"
    assert 25.0 <= result["overall_risk_score"] < 50.0


def test_high_risk_scenario():
    """Scenario 3: Steep slope, heavy 24h rainfall."""
    loc = {
        "id": 3,
        "name": "Steep Highway Cut",
        "state": "Meghalaya",
        "district": "East Khasi Hills",
        "latitude": 25.5,
        "longitude": 91.8,
        "elevation_m": 1200.0,
        "slope_deg": 32.0,
        "rainfall_1d_mm": 65.0,
        "rainfall_7d_mm": 180.0,
        "soil_moisture_percent": 75.0,
    }
    result = calculate_risk_assessment(loc, historical_records=[])
    print("[TEST 3] High Risk Scenario:", result["overall_risk_score"], result["risk_level"])
    assert result["risk_level"] == "HIGH"
    assert 50.0 <= result["overall_risk_score"] < 75.0


def test_critical_risk_scenario():
    """Scenario 4: Extreme rainfall, very steep slope, near historical landslides."""
    loc = {
        "id": 4,
        "name": "Mangan Ridge Pass",
        "state": "Sikkim",
        "district": "Mangan",
        "latitude": 27.5,
        "longitude": 88.5,
        "elevation_m": 1600.0,
        "slope_deg": 42.0,
        "rainfall_1d_mm": 95.0,
        "rainfall_7d_mm": 380.0,
        "soil_moisture_percent": 90.0,
    }
    hist = [
        {"district": "Mangan", "latitude": 27.502, "longitude": 88.531},
        {"district": "Mangan", "latitude": 27.510, "longitude": 88.540},
    ]
    result = calculate_risk_assessment(loc, historical_records=hist)
    print("[TEST 4] Critical Risk Scenario:", result["overall_risk_score"], result["risk_level"])
    assert result["risk_level"] == "CRITICAL"
    assert result["overall_risk_score"] >= 75.0


def test_missing_data_scenario():
    """Scenario 5: Soil moisture is None / null."""
    loc = {
        "id": 5,
        "name": "Unmonitored Sensor Spot",
        "state": "Assam",
        "district": "Dima Hasao",
        "latitude": 25.1,
        "longitude": 93.0,
        "elevation_m": 600.0,
        "slope_deg": 28.0,
        "rainfall_1d_mm": 40.0,
        "rainfall_7d_mm": 100.0,
        "soil_moisture_percent": None,  # Missing sensor
    }
    result = calculate_risk_assessment(loc, historical_records=[])
    print("[TEST 5] Missing Data Scenario:", result["data_completeness"])
    assert "soil_moisture_percent" in result["data_completeness"]["missing_factors"]
    assert result["data_completeness"]["completeness_percent"] < 100
    assert 0.0 <= result["overall_risk_score"] <= 100.0


def test_boundary_values():
    """Scenario 6: Extreme upper/lower bounds."""
    # Zero bounds
    loc_zero = {
        "id": 6,
        "name": "Zero Bounds",
        "state": "Assam",
        "district": "Kamrup",
        "latitude": 26.0,
        "longitude": 91.0,
        "elevation_m": 0.0,
        "slope_deg": 0.0,
        "rainfall_1d_mm": 0.0,
        "rainfall_7d_mm": 0.0,
        "soil_moisture_percent": 0.0,
    }
    res_zero = calculate_risk_assessment(loc_zero, historical_records=[])
    assert res_zero["overall_risk_score"] >= 0.0
    assert res_zero["overall_risk_score"] <= 100.0

    # Extreme upper bounds (>300mm rain, >60° slope + historical events)
    loc_extreme = {
        "id": 7,
        "name": "Extreme Bounds",
        "state": "Sikkim",
        "district": "Mangan",
        "latitude": 27.5,
        "longitude": 88.5,
        "elevation_m": 4000.0,
        "slope_deg": 75.0,
        "rainfall_1d_mm": 500.0,
        "rainfall_7d_mm": 1200.0,
        "soil_moisture_percent": 100.0,
    }
    hist_extreme = [
        {"district": "Mangan", "latitude": 27.5, "longitude": 88.5},
        {"district": "Mangan", "latitude": 27.5, "longitude": 88.5},
    ]
    res_extreme = calculate_risk_assessment(loc_extreme, historical_records=hist_extreme)
    assert res_extreme["overall_risk_score"] == 100.0  # Capped at 100.0 max
    assert res_extreme["risk_level"] == "CRITICAL"


if __name__ == "__main__":
    test_low_risk_scenario()
    test_moderate_risk_scenario()
    test_high_risk_scenario()
    test_critical_risk_scenario()
    test_missing_data_scenario()
    test_boundary_values()
    print("\nALL RISK ENGINE UNIT TESTS PASSED SUCCESSFULLY!")
