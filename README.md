# NER Landslide Sentinel

> **Landslide Risk Monitoring Prototype for North-East India**  
> *Developed for Smart India Hackathon — Problem Statement SIH26001*

---

## 📌 Project Overview
**NER Landslide Sentinel** is an SIH26001 prototype demonstrating a GIS dashboard, illustrative landslide-risk scores, sample reports, and a separate Open-Meteo weather-context feed for selected North-East India coordinates. It is not an operational early-warning service: seeded rainfall/risk values, alerts, reports, and historical records are demo data unless explicitly identified otherwise. Weather-context values are model-based and do not automatically update risk scores. Do not use this prototype for real-world safety decisions; follow official local disaster-management and weather advisories.

---

## ⚙️ Architecture Flow

```
DATA SOURCES (Historical + Terrain + Rainfall + Field Reports)
   │
   ▼
DEMO HEURISTIC ENGINE (No validated trained model)
   │
   ▼
ILLUSTRATIVE RISK CATEGORIES (LOW / MODERATE / HIGH / CRITICAL)
   │
   ▼
GIS MAPPING & OPERATIONAL DASHBOARDS
   │
   ▼
CITIZEN INCIDENT REPORTING & ROAD BLOCKAGE SENSING
   │
   ▼
EXPLAINABLE PROTOTYPE GUIDANCE (Not an official warning)
```

---

## 📁 Repository Structure
```
ner-landslide-sentinel/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── dashboard.py       # Aggregated summary & regional risk metrics
│   │   ├── database/
│   │   │   ├── database.py        # SQLite engine & session management
│   │   │   └── models.py          # ORM models (Locations, Alerts, Reports, Historical)
│   │   ├── schemas/
│   │   │   ├── common.py          # Enums for severity and risk levels
│   │   │   └── dashboard.py       # Pydantic schemas for dashboard responses
│   │   ├── data/
│   │   │   └── seed_demo_data.py  # Realistic North-East India demo datasets
│   │   ├── config.py              # Application settings & environment variables
│   │   └── main.py                # FastAPI entrypoint, lifespan & health checks
│   ├── tests/
│   │   └── test_phase2.py         # Automated API & DB integration test suite
│   ├── uploads/                   # Local storage for citizen hazard photos
│   └── requirements.txt           # Python dependencies
├── frontend/                      # React + Vite + Tailwind GIS dashboard (Phase 3+)
├── ml/                            # Model training, feature pipelines & datasets
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 How to Run the Backend (Phase 2)

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Required packages:
  ```bash
  pip install fastapi uvicorn sqlalchemy httpx python-multipart
  ```

### 2. Start the Backend Server
From the project root:
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Verify Endpoints
- Interactive Swagger Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- Regional Dashboard Summary: [http://127.0.0.1:8000/api/dashboard/summary](http://127.0.0.1:8000/api/dashboard/summary)\n- Separate model-based weather context: [http://127.0.0.1:8000/api/weather/live](http://127.0.0.1:8000/api/weather/live) (requires internet access; does not alter demo scores)

---

## 🧪 Run Automated Tests
```bash
cd backend
python tests/test_phase2.py
```

---

## 🛡️ Hackathon Transparency & Model Status
- **Current Model Status**: `DEMO_RISK_ENGINE` (heuristic prototype; no validated trained model is loaded).
- **Data Status**: Seeded risk scores, rainfall values, alerts, reports, and historical records are illustrative and flagged with `is_demo_data=True`. Coordinates are demo monitoring points, not proof of active sensor coverage.
- **Weather Context**: `/api/weather/live` retrieves Open-Meteo model-based weather context for the configured coordinates. It is intentionally separate from the heuristic risk score until inputs, calibration, and validation can be established.\n- **Integrity**: No ML accuracy claims are made. A trained model, validated datasets, operational sensors, and independent evaluation remain future work.
