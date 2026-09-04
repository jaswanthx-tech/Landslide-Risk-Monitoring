"""
Pydantic Schemas for Risk Locations, Historical Landslides, and Citizen Reports
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class RiskLocationSchema(BaseModel):
    id: int
    name: str
    state: str
    district: str
    latitude: float
    longitude: float
    elevation_m: float
    slope_deg: float
    rainfall_1d_mm: float
    rainfall_3d_mm: float
    rainfall_7d_mm: float
    soil_moisture_percent: Optional[float] = None
    risk_score: float
    risk_level: str
    contributing_factors: Optional[str] = None
    updated_at: Optional[datetime] = None
    is_demo_data: bool = True

    class Config:
        from_attributes = True


class HistoricalLandslideSchema(BaseModel):
    id: int
    location_name: str
    state: str
    district: str
    latitude: float
    longitude: float
    event_date: str
    trigger_type: str
    rainfall_cumulative_mm: Optional[float] = None
    slope_deg: Optional[float] = None
    damage_summary: Optional[str] = None
    fatalities: int = 0
    road_blocked: bool = True
    data_source: str
    is_demo_data: bool = True

    class Config:
        from_attributes = True


class IncidentReportSchema(BaseModel):
    id: int
    reporter_name: str
    contact_number: Optional[str] = None
    location_name: str
    latitude: float
    longitude: float
    severity: str
    description: str
    road_blocked: bool
    infrastructure_impact: Optional[str] = None
    photo_url: Optional[str] = None
    status: str
    priority_score: float
    priority_level: str
    submitted_at: Optional[datetime] = None
    is_demo_data: bool = True

    class Config:
        from_attributes = True


class IncidentReportCreateSchema(BaseModel):
    reporter_name: str = Field(default="Anonymous")
    contact_number: Optional[str] = None
    location_name: str
    latitude: float
    longitude: float
    severity: str = Field(default="MODERATE")  # LOW, MODERATE, HIGH, CRITICAL
    description: str
    road_blocked: bool = False
    infrastructure_impact: Optional[str] = None
