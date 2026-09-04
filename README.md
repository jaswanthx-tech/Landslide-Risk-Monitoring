# NER Landslide Sentinel

> **AI-Powered Dynamic Landslide Early Warning and Risk Monitoring System for North-East India**  
> *Developed for Smart India Hackathon — Problem Statement SIH26001*

---

## 📌 Project Overview
North-East India faces high susceptibility to precipitation-induced landslides across major connectivity lifelines (e.g. NH-29 Kohima-Dimapur, NH-06 Meghalaya-Barak corridor, Chungthang Sikkim highway, and Dima Hasao railway tracks). **NER Landslide Sentinel** monitors geological and meteorological parameters, processes antecedent rainfall triggers, visualizes spatial vulnerabilities on interactive GIS maps, crowdsources field reports, and calculates operational response priorities for disaster response authorities (NDRF/SDRF).

---

## ⚙️ Architecture Flow

```
DATA SOURCES (Historical + Terrain + Rainfall + Field Reports)
   │
   ▼
FEATURE EXTRACTION & HEURISTIC ENGINE (Awaiting trained model.joblib)
   │
   ▼
DYNAMIC RISK STRATIFICATION (LOW / MODERATE / HIGH / CRITICAL)
   │
   ▼
GIS MAPPING & OPERATIONAL DASHBOARDS
   │
   ▼
CITIZEN INCIDENT REPORTING & ROAD BLOCKAGE SENSING
   │
   ▼
TRANSPARENT RESPONSE PRIORITY SCORING (SDRF / District Authorities)
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
- Regional Dashboard Summary: [http://127.0.0.1:8000/api/dashboard/summary](http://127.0.0.1:8000/api/dashboard/summary)

---

## 🧪 Run Automated Tests
```bash
cd backend
python tests/test_phase2.py
```

---

## 🛡️ Hackathon Transparency & Model Status
- **Current Model Status**: `DEMO_RISK_ENGINE` (calibrated multi-factor heuristic prototype).
- **Data Status**: Seeded with representative North-East India geological and rainfall coordinates, all explicitly labeled with `is_demo_data=True`.
- **Integrity Guarantee**: No unsupported or fabricated ML accuracy claims (e.g. "99% accuracy") are made. The backend interface is architected for seamless drop-in integration of trained `model.joblib` (Random Forest, XGBoost, or LightGBM) in subsequent phases.
