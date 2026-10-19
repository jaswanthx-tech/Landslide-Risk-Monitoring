"""
API Endpoints for Risk Locations, Historical Landslides, and Citizen Reports.
"""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import RiskLocation, HistoricalLandslide, IncidentReport
from app.schemas.endpoints import (
    RiskLocationSchema,
    HistoricalLandslideSchema,
    IncidentReportSchema,
    IncidentReportCreateSchema,
)

router = APIRouter(prefix="/api", tags=["Sentinel Core APIs"])


@router.get("/risk/locations", response_model=List[RiskLocationSchema])
def get_risk_locations(db: Session = Depends(get_db)):
    """Returns all monitored landslide risk locations with dynamically updated risk engine indicators."""
    locations = db.query(RiskLocation).all()
    historical_records = db.query(HistoricalLandslide).all()

    # Synchronize live calculated risk scores and risk levels across database entities
    for loc in locations:
        assessment = calculate_risk_assessment(loc, historical_records)
        loc.risk_score = round(assessment["overall_risk_score"] / 100.0, 2)
        loc.risk_level = assessment["risk_level"]

    locations.sort(key=lambda x: x.risk_score, reverse=True)
    return locations


@router.get("/historical-landslides", response_model=List[HistoricalLandslideSchema])
def get_historical_landslides(db: Session = Depends(get_db)):
    """Returns historical-record samples; callers must check is_demo_data before treating them as verified."""
    events = db.query(HistoricalLandslide).order_by(HistoricalLandslide.id.desc()).all()
    return events


@router.get("/reports", response_model=List[IncidentReportSchema])
def get_incident_reports(db: Session = Depends(get_db)):
    """Returns submitted reports and samples; callers must check is_demo_data before treating them as verified."""
    reports = db.query(IncidentReport).order_by(IncidentReport.submitted_at.desc()).all()
    return reports


@router.post("/reports", response_model=IncidentReportSchema, status_code=status.HTTP_201_CREATED)
def create_incident_report(report_data: IncidentReportCreateSchema, db: Session = Depends(get_db)):
    """Submits a new citizen hazard report and assigns automated initial priority score."""
    # Priority scoring heuristic based on severity and road blockage
    severity_weights = {"LOW": 0.25, "MODERATE": 0.50, "HIGH": 0.75, "CRITICAL": 0.95}
    base_score = severity_weights.get(report_data.severity.upper(), 0.5)
    if report_data.road_blocked:
        base_score = min(1.0, base_score + 0.15)
    
    priority_level = "LOW PRIORITY"
    if base_score >= 0.85:
        priority_level = "CRITICAL PRIORITY"
    elif base_score >= 0.70:
        priority_level = "HIGH PRIORITY"
    elif base_score >= 0.45:
        priority_level = "MEDIUM PRIORITY"

    new_report = IncidentReport(
        reporter_name=report_data.reporter_name,
        contact_number=report_data.contact_number,
        location_name=report_data.location_name,
        latitude=report_data.latitude,
        longitude=report_data.longitude,
        severity=report_data.severity.upper(),
        description=report_data.description,
        road_blocked=report_data.road_blocked,
        infrastructure_impact=report_data.infrastructure_impact,
        status="PENDING",
        priority_score=round(base_score, 2),
        priority_level=priority_level,
        submitted_at=datetime.utcnow(),
        is_demo_data=False,
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


# =====================================================================
# Phase 4 & 5: Explainable Risk Engine & Early Warning Endpoints
# =====================================================================
from app.services.risk_engine import calculate_risk_assessment
from app.schemas.risk_engine import RiskAssessmentResponse


@router.get("/risk/assessment/{location_id}", response_model=RiskAssessmentResponse)
def get_location_risk_assessment(location_id: int, db: Session = Depends(get_db)):
    """
    Returns a transparent, explainable multi-factor risk assessment for a specific location.
    Calculates Factor Breakdown (Rainfall 35%, Slope 30%, History 20%, Environment 15%),
    Main Contributing Triggers, Data Completeness, and Recommended Safety Actions.
    """
    location = db.query(RiskLocation).filter(RiskLocation.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail=f"Risk location with ID {location_id} not found.")

    historical_records = db.query(HistoricalLandslide).all()
    assessment = calculate_risk_assessment(location, historical_records)
    return assessment


@router.get("/risk/assessments", response_model=List[RiskAssessmentResponse])
def get_all_risk_assessments(db: Session = Depends(get_db)):
    """Returns dynamic risk assessment and explainability breakdowns for all monitored locations."""
    locations = db.query(RiskLocation).all()
    historical_records = db.query(HistoricalLandslide).all()
    
    assessments = [calculate_risk_assessment(loc, historical_records) for loc in locations]
    assessments.sort(key=lambda x: x["overall_risk_score"], reverse=True)
    return assessments


@router.post("/risk/recalculate")
def recalculate_all_risk_scores(db: Session = Depends(get_db)):
    """
    Recalculates risk scores and risk levels across all monitored locations using the Risk Engine
    and updates SQLite database records.
    """
    locations = db.query(RiskLocation).all()
    historical_records = db.query(HistoricalLandslide).all()
    updated_count = 0

    for loc in locations:
        assessment = calculate_risk_assessment(loc, historical_records)
        loc.risk_score = round(assessment["overall_risk_score"] / 100.0, 2)
        loc.risk_level = assessment["risk_level"]
        loc.contributing_factors = ", ".join(assessment["main_contributors"])
        loc.updated_at = datetime.utcnow()
        updated_count += 1

    db.commit()
    return {
        "status": "success",
        "message": f"Successfully recalculated risk scores for {updated_count} locations.",
        "updated_locations_count": updated_count,
    }
