"""
Application Configuration Module
Provides centralized application settings with sensible defaults for local development.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads"))

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/ner_landslide_sentinel.db")

# App Metadata
APP_NAME = "NER Landslide Sentinel API"
APP_VERSION = "0.1.0-prototype"
DEBUG = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

# CORS Configuration
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://127.0.0.1:3000"
    ).split(",")
    if origin.strip()
]

# Risk Engine Configuration & Weights (Phase 4 & 5)
RISK_WEIGHT_RAINFALL = float(os.getenv("RISK_WEIGHT_RAINFALL", "0.35"))       # 35%
RISK_WEIGHT_SLOPE = float(os.getenv("RISK_WEIGHT_SLOPE", "0.30"))          # 30%
RISK_WEIGHT_HISTORICAL = float(os.getenv("RISK_WEIGHT_HISTORICAL", "0.20"))   # 20%
RISK_WEIGHT_ENVIRONMENT = float(os.getenv("RISK_WEIGHT_ENVIRONMENT", "0.15")) # 15%

# Trigger Thresholds
RAINFALL_24H_MAX_MM = float(os.getenv("RAINFALL_24H_MAX_MM", "100.0"))
RAINFALL_7D_MAX_MM = float(os.getenv("RAINFALL_7D_MAX_MM", "400.0"))
SLOPE_MAX_DEG = float(os.getenv("SLOPE_MAX_DEG", "45.0"))

# Risk Level Classification Thresholds (0-100)
RISK_THRESHOLD_MODERATE = 25.0  # 0 - 24.9 -> LOW, 25 - 49.9 -> MODERATE
RISK_THRESHOLD_HIGH = 50.0      # 50 - 74.9 -> HIGH
RISK_THRESHOLD_CRITICAL = 75.0  # 75 - 100 -> CRITICAL
