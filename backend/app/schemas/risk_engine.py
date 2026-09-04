"""
Pydantic Schemas for Landslide Risk Assessment & Explainability
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FactorScoreDetail(BaseModel):
    score: float = Field(..., description="Calculated factor score")
    max: float = Field(..., description="Maximum possible points for this factor")
    weight_percent: int = Field(..., description="Weight percentage in overall model")


class FactorBreakdownSchema(BaseModel):
    rainfall: Dict[str, Any]
    slope: Dict[str, Any]
    historical: Dict[str, Any]
    environment: Dict[str, Any]


class DataCompletenessSchema(BaseModel):
    completeness_percent: int
    available_factors: List[str]
    missing_factors: List[str]


class RiskAssessmentResponse(BaseModel):
    location_id: int
    location_name: str
    state: str
    district: str
    latitude: float
    longitude: float
    overall_risk_score: float = Field(..., ge=0.0, le=100.0, description="Normalized risk score (0-100)")
    risk_level: str = Field(..., description="LOW, MODERATE, HIGH, CRITICAL")
    factor_breakdown: FactorBreakdownSchema
    main_contributors: List[str]
    data_completeness: DataCompletenessSchema
    recommended_action: str
    model_mode: str = Field(default="CONFIGURABLE_WEIGHTED_HEURISTIC_V1", description="Transparency indicator")
    disclaimer: str = Field(
        default="Prototype early warning risk index for SIH26001. Awaiting integration with validated operational ML models and sensor feeds.",
        description="SIH transparency notice"
    )
