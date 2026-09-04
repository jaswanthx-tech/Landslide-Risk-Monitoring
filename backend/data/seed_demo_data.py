"""
Seed Script for Realistic Demo Data across North-East India
Populates monitoring locations, active alerts, citizen field reports,
and historical landslide records. All entities are explicitly flagged with is_demo_data=True.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.models import RiskLocation, Alert, IncidentReport, HistoricalLandslide


def seed_database(db: Session) -> dict:
    """Populates the database with initial demo data if tables are empty."""
    counts = {"locations": 0, "alerts": 0, "reports": 0, "historical": 0}

    # 1. Check if locations already exist
    if db.query(RiskLocation).count() == 0:
        demo_locations = [
            RiskLocation(
                name="Shillong Ridge & Bypass Corridor",
                state="Meghalaya",
                district="East Khasi Hills",
                latitude=25.5788,
                longitude=91.8933,
                elevation_m=1525.0,
                slope_deg=34.5,
                rainfall_1d_mm=82.4,
                rainfall_3d_mm=195.0,
                rainfall_7d_mm=380.0,
                soil_moisture_percent=88.5,
                risk_score=0.88,
                risk_level="CRITICAL",
                contributing_factors="Extreme 72h rainfall, steep cut-slopes, saturated clayey loam",
                is_demo_data=True
            ),
            RiskLocation(
                name="Mangan - Chungthang Highway",
                state="Sikkim",
                district="Mangan",
                latitude=27.5054,
                longitude=88.5284,
                elevation_m=1420.0,
                slope_deg=38.2,
                rainfall_1d_mm=94.0,
                rainfall_3d_mm=210.0,
                rainfall_7d_mm=410.0,
                soil_moisture_percent=92.0,
                risk_score=0.92,
                risk_level="CRITICAL",
                contributing_factors="Active tectonic shearing, intense precipitation, debris flow history",
                is_demo_data=True
            ),
            RiskLocation(
                name="Dima Hasao Hill Section (Haflong)",
                state="Assam",
                district="Dima Hasao",
                latitude=25.1764,
                longitude=93.0234,
                elevation_m=680.0,
                slope_deg=29.0,
                rainfall_1d_mm=64.0,
                rainfall_3d_mm=142.0,
                rainfall_7d_mm=275.0,
                soil_moisture_percent=81.0,
                risk_score=0.78,
                risk_level="HIGH",
                contributing_factors="Continuous hill track drainage issues, soft shale geology",
                is_demo_data=True
            ),
            RiskLocation(
                name="Kohima - Dimapur Highway (NH-29)",
                state="Nagaland",
                district="Kohima",
                latitude=25.6751,
                longitude=94.1086,
                elevation_m=1444.0,
                slope_deg=31.0,
                rainfall_1d_mm=58.0,
                rainfall_3d_mm=130.0,
                rainfall_7d_mm=245.0,
                soil_moisture_percent=76.0,
                risk_score=0.74,
                risk_level="HIGH",
                contributing_factors="Heavy vehicular corridor, unstable rock strata, moderate continuous rain",
                is_demo_data=True
            ),
            RiskLocation(
                name="Aizawl North Slope (Laipuitlang)",
                state="Mizoram",
                district="Aizawl",
                latitude=23.7271,
                longitude=92.7176,
                elevation_m=1132.0,
                slope_deg=35.0,
                rainfall_1d_mm=45.0,
                rainfall_3d_mm=98.0,
                rainfall_7d_mm=185.0,
                soil_moisture_percent=72.0,
                risk_score=0.69,
                risk_level="HIGH",
                contributing_factors="Dense slope settlement, sandstone bedrock slip planes",
                is_demo_data=True
            ),
            RiskLocation(
                name="Tawang Ghat Road",
                state="Arunachal Pradesh",
                district="Tawang",
                latitude=27.5861,
                longitude=91.8594,
                elevation_m=2669.0,
                slope_deg=36.0,
                rainfall_1d_mm=32.0,
                rainfall_3d_mm=75.0,
                rainfall_7d_mm=150.0,
                soil_moisture_percent=64.0,
                risk_score=0.55,
                risk_level="MODERATE",
                contributing_factors="High altitude frost action, moderate rainfall trigger",
                is_demo_data=True
            ),
            RiskLocation(
                name="Guwahati - Kamakhya Foothills",
                state="Assam",
                district="Kamrup Metropolitan",
                latitude=26.1664,
                longitude=91.7058,
                elevation_m=160.0,
                slope_deg=24.0,
                rainfall_1d_mm=28.0,
                rainfall_3d_mm=62.0,
                rainfall_7d_mm=120.0,
                soil_moisture_percent=58.0,
                risk_score=0.48,
                risk_level="MODERATE",
                contributing_factors="Urban hillside earth-cutting, clogged stormwater outlets",
                is_demo_data=True
            ),
            RiskLocation(
                name="Imphal - Jiribam Highway (NH-37)",
                state="Manipur",
                district="Noney",
                latitude=24.7865,
                longitude=93.6214,
                elevation_m=840.0,
                slope_deg=28.0,
                rainfall_1d_mm=35.0,
                rainfall_3d_mm=80.0,
                rainfall_7d_mm=160.0,
                soil_moisture_percent=62.0,
                risk_score=0.52,
                risk_level="MODERATE",
                contributing_factors="Riverbank toe erosion, slope overburden",
                is_demo_data=True
            ),
            RiskLocation(
                name="Jampui Hills Sector",
                state="Tripura",
                district="North Tripura",
                latitude=23.9450,
                longitude=92.2710,
                elevation_m=830.0,
                slope_deg=18.0,
                rainfall_1d_mm=15.0,
                rainfall_3d_mm=38.0,
                rainfall_7d_mm=72.0,
                soil_moisture_percent=42.0,
                risk_score=0.25,
                risk_level="LOW",
                contributing_factors="Dense vegetative cover, gentle slope gradients",
                is_demo_data=True
            ),
            RiskLocation(
                name="Itanagar Capital Complex Slopes",
                state="Arunachal Pradesh",
                district="Papum Pare",
                latitude=27.0844,
                longitude=93.6053,
                elevation_m=320.0,
                slope_deg=20.0,
                rainfall_1d_mm=18.0,
                rainfall_3d_mm=42.0,
                rainfall_7d_mm=85.0,
                soil_moisture_percent=46.0,
                risk_score=0.28,
                risk_level="LOW",
                contributing_factors="Stabilized retaining structures, low recent rainfall",
                is_demo_data=True
            )
        ]
        db.add_all(demo_locations)
        counts["locations"] = len(demo_locations)

    # 2. Check if alerts already exist
    if db.query(Alert).count() == 0:
        now = datetime.utcnow()
        demo_alerts = [
            Alert(
                location_name="Mangan - Chungthang Highway",
                state="Sikkim",
                latitude=27.5054,
                longitude=88.5284,
                risk_level="CRITICAL",
                title="Immediate Evacuation Warning: Active Mudslip & Slope Failure",
                message="Antecedent 72h precipitation crossed 210mm threshold. High probability of major rockslide across KM 18.",
                recommended_action="Suspend all transit immediately. Deploy SDRF / BRO heavy clearing machinery on standby.",
                acknowledged=False,
                created_at=now - timedelta(minutes=25),
                is_demo_data=True
            ),
            Alert(
                location_name="Shillong Ridge & Bypass Corridor",
                state="Meghalaya",
                latitude=25.5788,
                longitude=91.8933,
                risk_level="CRITICAL",
                title="Flash Slope Instability Advisory",
                message="Continuous torrential downpours causing severe tension cracking on cut slopes along NH-6 connect.",
                recommended_action="Divert heavy freight traffic. Issue civil defense broadcast to lower foothill settlements.",
                acknowledged=False,
                created_at=now - timedelta(hours=2),
                is_demo_data=True
            ),
            Alert(
                location_name="Dima Hasao Hill Section (Haflong)",
                state="Assam",
                latitude=25.1764,
                longitude=93.0234,
                risk_level="HIGH",
                title="High Risk Warning: Saturated Hillside Slips",
                message="Cumulative 7-day rainfall reached 275mm. Soil saturation index exceeds 80%. Railway cutting monitoring activated.",
                recommended_action="Impose speed restrictions on Lumding-Badarpur rail section. Monitor culvert discharge.",
                acknowledged=True,
                acknowledged_at=now - timedelta(hours=1),
                acknowledged_by="District Disaster Management Officer, Dima Hasao",
                created_at=now - timedelta(hours=4),
                is_demo_data=True
            ),
            Alert(
                location_name="Kohima - Dimapur Highway (NH-29)",
                state="Nagaland",
                latitude=25.6751,
                longitude=94.1086,
                risk_level="HIGH",
                title="Landslide Watch: Pagla Pahar Sector Vulnerability",
                message="Active mud seepage observed on uphill slope. Intermittent debris falling on highway carriage.",
                recommended_action="Station traffic police at Chumukedima checkpoint. Maintain one-way transit.",
                acknowledged=False,
                created_at=now - timedelta(hours=6),
                is_demo_data=True
            )
        ]
        db.add_all(demo_alerts)
        counts["alerts"] = len(demo_alerts)

    # 3. Check if incident reports already exist
    if db.query(IncidentReport).count() == 0:
        now = datetime.utcnow()
        demo_reports = [
            IncidentReport(
                reporter_name="Tenzing Lepcha (Field Surveyor)",
                contact_number="+91-98000-12345",
                location_name="Chungthang Road, Mile 14",
                latitude=27.5210,
                longitude=88.5410,
                severity="CRITICAL",
                description="Massive boulder displacement and mud debris fully covering 60 meters of road width. 15 vehicles stranded.",
                road_blocked=True,
                infrastructure_impact="Major highway blocked, telecommunication pole snapped",
                photo_url=None,
                status="VERIFIED",
                priority_score=0.95,
                priority_level="CRITICAL PRIORITY",
                submitted_at=now - timedelta(minutes=45),
                is_demo_data=True
            ),
            IncidentReport(
                reporter_name="Bokul Das (Citizen)",
                contact_number="+91-94350-67890",
                location_name="Barapani-Shillong Old Route",
                latitude=25.6510,
                longitude=91.9120,
                severity="HIGH",
                description="Mud overflow on the uphill curve near transformer. Single lane passable with high risk.",
                road_blocked=False,
                infrastructure_impact="High-tension power line in proximity to unstable verge",
                photo_url=None,
                status="VERIFIED",
                priority_score=0.76,
                priority_level="HIGH PRIORITY",
                submitted_at=now - timedelta(hours=3),
                is_demo_data=True
            ),
            IncidentReport(
                reporter_name="Lalrinzuala (Taxi Driver Association)",
                contact_number="+91-98620-11223",
                location_name="Zemabawk Slope, Aizawl",
                latitude=23.7420,
                longitude=92.7480,
                severity="MODERATE",
                description="Minor retaining wall deformation and water oozing through fissures behind residential structure.",
                road_blocked=False,
                infrastructure_impact="Residential building foundation within 5 meters",
                photo_url=None,
                status="PENDING",
                priority_score=0.58,
                priority_level="MEDIUM PRIORITY",
                submitted_at=now - timedelta(hours=5),
                is_demo_data=True
            ),
            IncidentReport(
                reporter_name="Arun Sharma (PWD Junior Engineer)",
                contact_number="+91-97740-99887",
                location_name="NH-29 Old Checkpost, Kohima",
                latitude=25.6890,
                longitude=94.1190,
                severity="HIGH",
                description="Slump in road pavement and cracked drainage culvert. Water pooling heavily on embankment.",
                road_blocked=True,
                infrastructure_impact="Arterial state logistics highway",
                photo_url=None,
                status="VERIFIED",
                priority_score=0.82,
                priority_level="HIGH PRIORITY",
                submitted_at=now - timedelta(hours=8),
                is_demo_data=True
            )
        ]
        db.add_all(demo_reports)
        counts["reports"] = len(demo_reports)

    # 4. Check historical landslide events
    if db.query(HistoricalLandslide).count() == 0:
        demo_historical = [
            HistoricalLandslide(
                location_name="Maligaon Railway Colony, Guwahati",
                state="Assam",
                district="Kamrup Metropolitan",
                latitude=26.1550,
                longitude=91.6890,
                event_date="2022-06-15",
                trigger_type="Extreme Monsoon Cloudburst",
                rainfall_cumulative_mm=212.0,
                slope_deg=32.0,
                damage_summary="Earth slip collapsed perimeter wall and engulfed 2 residential quarters. 4 injured.",
                fatalities=0,
                road_blocked=True,
                data_source="Assam State Disaster Management Authority (ASDMA)",
                is_demo_data=True
            ),
            HistoricalLandslide(
                location_name="Jowai-Ratacherra Highway (NH-06)",
                state="Meghalaya",
                district="East Jaintia Hills",
                latitude=25.2100,
                longitude=92.3500,
                event_date="2022-06-17",
                trigger_type="Continuous 5-day Downpour",
                rainfall_cumulative_mm=540.0,
                slope_deg=36.0,
                damage_summary="Massive slope rupture cut off Barak Valley, Tripura, and Mizoram for over 6 days.",
                fatalities=1,
                road_blocked=True,
                data_source="National Highways Authority of India & Meghalaya PWD",
                is_demo_data=True
            ),
            HistoricalLandslide(
                location_name="Mangan District HQ Sector",
                state="Sikkim",
                district="Mangan",
                latitude=27.5020,
                longitude=88.5310,
                event_date="2024-06-13",
                trigger_type="Severe Monsoon Precipitation & Flash Floods",
                rainfall_cumulative_mm=290.0,
                slope_deg=40.0,
                damage_summary="Series of landslides destroyed bridges and severed road connectivity to North Sikkim.",
                fatalities=6,
                road_blocked=True,
                data_source="Sikkim State Disaster Management Authority (SSDMA)",
                is_demo_data=True
            ),
            HistoricalLandslide(
                location_name="New Haflong Railway Station Track",
                state="Assam",
                district="Dima Hasao",
                latitude=25.1650,
                longitude=93.0180,
                event_date="2022-05-16",
                trigger_type="Incessant Rain & Hill Siltation",
                rainfall_cumulative_mm=365.0,
                slope_deg=28.0,
                damage_summary="Debris flow buried standing train wagons and washed out ballast across 12 track sections.",
                fatalities=0,
                road_blocked=True,
                data_source="Northeast Frontier Railway (NFR) Disaster Report",
                is_demo_data=True
            ),
            HistoricalLandslide(
                location_name="Laipuitlang Hillside, Aizawl",
                state="Mizoram",
                district="Aizawl",
                latitude=23.7310,
                longitude=92.7150,
                event_date="2013-05-11",
                trigger_type="Pre-monsoon Heavy Rain",
                rainfall_cumulative_mm=178.0,
                slope_deg=38.0,
                damage_summary="Major rock slide collapsed 17 multi-storey buildings down the slope.",
                fatalities=17,
                road_blocked=True,
                data_source="Geological Survey of India (GSI) Landslide Atlas",
                is_demo_data=True
            )
        ]
        db.add_all(demo_historical)
        counts["historical"] = len(demo_historical)

    db.commit()
    return counts
