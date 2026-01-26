"""
Infrastructure layer - data access operations
"""


def insert_heartbeat(conn, site_id: str, timestamp: str):
    """
    Persists heartbeat data to the database.
    This is infrastructure - it handles I/O.
    """
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO heartbeats (site_id, timestamp) VALUES (?, ?)",
        (site_id, timestamp)
    )
    conn.commit()


def insert_alert(conn, timestamp: str, site_id: str, alert_type: str, 
                severity: str, latitude: float, longitude: float):
    """
    TODO: Implement alert insertion.
    
    Persists alert data to the database.
    
    Args:
        conn: SQLite connection
        timestamp: When the alert occurred
        site_id: Which site generated the alert
        alert_type: Type of alert (PRESSURE, TEMPERATURE, etc.)
        severity: CRITICAL or MODERATE
        latitude: Site latitude
        longitude: Site longitude
    """
    # TODO: Implement this function
    pass


def get_all_alerts(conn):
    """Retrieves all alerts from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts")
    return cursor.fetchall()
