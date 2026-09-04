"""
Pydantic Schemas for Regional Dashboard Summary
Provides aggregated situational awareness metrics across North-East India.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class RiskDistribution(BaseModel):
    low: int = Field(..., description="Count of low risk monitoring zones")
    moderate: int = Field(..., description="Count of moderate risk monitoring zones")
    high: int = Field(..., description="Count of high risk monitoring zones")
    critical: int = Field(..., description="Count of critical risk monitoring zones")


class RainfallTrendPoint(BaseModel):
    label: str = Field(..., description="Day or timestamp label (e.g. 'Day -6', 'Today')")
    average_rainfall_mm: float = Field(..., description="Average regional precipitation (mm)")
    max_recorded_mm: float = Field(..., description="Maximum localized spike (mm)")


class RecentIncidentItem(BaseModel):
    id: int
    location_name: str
    severity: str
    road_blocked: bool
    status: str
    submitted_at: str
    is_demo_data: bool


class ActiveAlertItem(BaseModel):
    id: int
    location_name: str
    state: str
    risk_level: str
    title: str
    message: str
    acknowledged: bool
    created_at: str
    is_demo_data: bool


class RegionalRiskSummary(BaseModel):
    total_monitored_locations: int
    high_risk_count: int
    critical_risk_count: int
    active_alerts_count: int
    recent_incidents_count: int
    average_regional_rainfall_24h_mm: float
    overall_status: str


class DashboardSummaryResponse(BaseModel):
    regional_summary: RegionalRiskSummary
    risk_distribution: RiskDistribution
    rainfall_trends: List[RainfallTrendPoint]
    recent_incidents: List[RecentIncidentItem]
    active_alerts: List[ActiveAlertItem]
    data_mode: str = Field(
        default="DEMO_MODE",
        description="Indicates whether data source is sample/demo or operational"
    )
    disclaimer: str = Field(
        default="Prototype demonstration data for SIH26001. Awaiting integration with validated trained models and operational state sensor feeds.",
        description="Clear transparency notice regarding prototype status"
    )
