from domain.processor import classify_alert
from infrastructure.repositories import insert_alert
from infrastructure.database import get_connection, initialize_database

def process_alert_reading(
    conn,
    timestamp: str,
    site_id: str,
    alert_type: str,
    latitude: float,
    longitude: float,
):
    # --- Domain logic ---
    severity = classify_alert(alert_type)

    # --- Infrastructure I/O ---
    insert_alert(
        conn,
        timestamp,
        site_id,
        alert_type,
        severity,
        latitude,
        longitude,
    )

    # --- Feedback ---
    print(f"Processing alert: {alert_type} at {site_id}...")
    print(f"Alert recorded with severity: {severity}\n")


def process_heartbeat(site_id: str):
    print(f"Processing heartbeat for {site_id}...")
    print("Heartbeat recorded successfully.\n")


if __name__ == "__main__":
    # 1. Setup database connection
    conn = get_connection()
    initialize_database(conn)

    # 2. Process a heartbeat
    process_heartbeat("SITE_001")

    # 3. Process some alerts
    process_alert_reading(
        conn,
        timestamp="2024-01-26T10:00:00Z",
        site_id="SITE_001",
        alert_type="LEAK",
        latitude=29.7604,
        longitude=-95.3698,
    )

    process_alert_reading(
        conn,
        timestamp="2024-01-26T10:05:00Z",
        site_id="SITE_002",
        alert_type="TEMPERATURE",
        latitude=40.7128,
        longitude=-74.0060,
    )

    # 4. Close connection
    conn.close()
