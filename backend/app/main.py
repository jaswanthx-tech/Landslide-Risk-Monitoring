"""
NER Landslide Sentinel - Backend API Entrypoint
FastAPI server providing early warning risk monitoring, dynamic alerts,
incident reporting, and response priority orchestration for North-East India.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.config import APP_NAME, APP_VERSION, DEBUG, CORS_ORIGINS
from app.database.database import Base, engine, get_db
from app.data.seed_demo_data import seed_database
from app.api.dashboard import router as dashboard_router
from app.api.endpoints import router as endpoints_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    Initializes database tables and populates baseline demo data for North-East India.
    """
    # 1. Initialize SQLite tables
    Base.metadata.create_all(bind=engine)

    # 2. Seed initial demo dataset if fresh database & sync Risk Engine
    db = next(get_db())
    try:
        seed_result = seed_database(db)
        from app.services.risk_engine import calculate_risk_assessment
        from app.database.models import RiskLocation, HistoricalLandslide
        locations = db.query(RiskLocation).all()
        historical = db.query(HistoricalLandslide).all()
        for loc in locations:
            assessment = calculate_risk_assessment(loc, historical)
            loc.risk_score = round(assessment["overall_risk_score"] / 100.0, 2)
            loc.risk_level = assessment["risk_level"]
        db.commit()
        print(f"[STARTUP] Database initialized. Seeded: {seed_result}. Risk Engine Synced.")
    finally:
        db.close()

    yield

    print("[SHUTDOWN] NER Landslide Sentinel API stopped.")


# Initialize FastAPI application
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "AI-Powered Dynamic Landslide Early Warning and Risk Monitoring System "
        "for North-East India (SIH26001 Prototype)."
    ),
    lifespan=lifespan,
    debug=DEBUG,
)

# Configure Cross-Origin Resource Sharing (CORS) for Vite/React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(dashboard_router)
app.include_router(endpoints_router)


@app.get("/", tags=["General"])
def root():
    """Root metadata endpoint."""
    return {
        "system": APP_NAME,
        "version": APP_VERSION,
        "status": "operational",
        "region": "North-East India",
        "data_mode": "DEMO_MODE",
        "docs_url": "/docs",
        "disclaimer": (
            "Prototype system for SIH26001. Awaiting integration with "
            "validated trained models and operational field sensors."
        ),
    }


@app.get("/health", tags=["General"])
def health_check(db: Session = Depends(get_db)):
    """
    System and Database Health Check.
    Verifies SQLite connectivity and returns operational mode.
    """
    db_status = "unreachable"
    try:
        # Ping the database
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "service": APP_NAME,
        "version": APP_VERSION,
        "database": db_status,
        "data_mode": "DEMO_MODE",
        "ml_model_status": "DEMO_RISK_ENGINE (heuristic prototype, awaiting trained model.joblib)",
    }
