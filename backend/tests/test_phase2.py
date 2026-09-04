"""
Phase 2 Test Suite for NER Landslide Sentinel
Verifies:
1. Application initialization & Lifespan
2. /health endpoint connectivity and database status
3. /api/dashboard/summary calculations, response structure, and DEMO disclosures
4. Integrity checks (no fake accuracy claims, explicit prototype labels)
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from app.main import app


def test_phase2_endpoints():
    print("=" * 65)
    print("RUNNING PHASE 2 AUTOMATED TEST SUITE: NER LANDSLIDE SENTINEL")
    print("=" * 65)

    with TestClient(app) as client:
        # Test 1: Root endpoint
        print("\n[TEST 1] Testing Root Endpoint GET /")
        r_root = client.get("/")
        assert r_root.status_code == 200, f"Root endpoint returned {r_root.status_code}"
        root_data = r_root.json()
        print("  Root response:", root_data)
        assert root_data["system"] == "NER Landslide Sentinel API"
        assert root_data["data_mode"] == "DEMO_MODE"
        print("  --> PASSED: Root endpoint verified.")

        # Test 2: Health check endpoint
        print("\n[TEST 2] Testing Health Check GET /health")
        r_health = client.get("/health")
        assert r_health.status_code == 200, f"Health endpoint returned {r_health.status_code}"
        health_data = r_health.json()
        print("  Health response:", health_data)
        assert health_data["status"] == "healthy"
        assert health_data["database"] == "connected"
        assert health_data["data_mode"] == "DEMO_MODE"
        assert "DEMO_RISK_ENGINE" in health_data["ml_model_status"]
        print("  --> PASSED: Health check & SQLite database connectivity verified.")

        # Test 3: Dashboard Summary endpoint
        print("\n[TEST 3] Testing Dashboard Summary GET /api/dashboard/summary")
        r_summary = client.get("/api/dashboard/summary")
        assert r_summary.status_code == 200, f"Dashboard summary returned {r_summary.status_code}"
        summary_data = r_summary.json()
        
        reg = summary_data["regional_summary"]
        dist = summary_data["risk_distribution"]
        trends = summary_data["rainfall_trends"]
        incidents = summary_data["recent_incidents"]
        alerts = summary_data["active_alerts"]
        
        print(f"  Total Monitored Locations: {reg['total_monitored_locations']}")
        print(f"  Risk Distribution: LOW={dist['low']}, MODERATE={dist['moderate']}, HIGH={dist['high']}, CRITICAL={dist['critical']}")
        print(f"  Active Alerts: {len(alerts)} (Unacknowledged: {reg['active_alerts_count']})")
        print(f"  Recent Incidents: {len(incidents)}")
        print(f"  Rainfall 24h Average: {reg['average_regional_rainfall_24h_mm']} mm")
        print(f"  Overall Status: {reg['overall_status']}")
        print(f"  Data Mode: {summary_data['data_mode']}")
        print(f"  Disclaimer: {summary_data['disclaimer']}")

        # Verifications
        assert reg["total_monitored_locations"] >= 10, "Expected at least 10 monitored locations seeded"
        assert dist["critical"] >= 1, "Expected critical locations in seed data"
        assert len(incidents) >= 4, "Expected seeded incident reports"
        assert len(alerts) >= 4, "Expected seeded alert notifications"
        assert len(trends) == 7, "Expected 7-day trend series"
        assert summary_data["data_mode"] == "DEMO_MODE"
        assert "Prototype demonstration data" in summary_data["disclaimer"]
        print("  --> PASSED: Dashboard summary calculated and structured correctly.")

        # Test 4: Integrity check - ensure no fake accuracy claims anywhere
        print("\n[TEST 4] Integrity Audit: Ensuring no fake accuracy claims")
        dumped_text = str(summary_data) + str(health_data) + str(root_data)
        assert "%" not in health_data["ml_model_status"], "No percentage accuracy claim allowed"
        assert "99%" not in dumped_text and "98%" not in dumped_text
        print("  --> PASSED: Integrity check confirmed no misleading accuracy claims.")

    print("\n" + "=" * 65)
    print("ALL PHASE 2 TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    test_phase2_endpoints()
