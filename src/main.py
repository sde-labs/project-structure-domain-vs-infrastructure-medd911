from src.domain.processor import classify_alert, validate_heartbeat
from src.infrastructure.database import get_connection, initialize_database
from src.infrastructure.repositories import insert_heartbeat, insert_alert


def process_alert_reading(conn, timestamp: str, site_id: str, alert_type: str, 
    latitude: float, longitude: float):
    # Step 1: Classify alert (Domain layer - pure logic, no I/O)
    severity = classify_alert(alert_type)

    # Step 2: Persist to database (Infrastructure layer - I/O)
    insert_alert(conn, timestamp, site_id, alert_type, severity, latitude, longitude)

    print(f"Alert recorded with severity: {severity}")

