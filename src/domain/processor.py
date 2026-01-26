"""
Domain layer - pure business logic with no I/O operations
"""


def validate_heartbeat(site_id: str, timestamp: str) -> bool:
    """
    Validates heartbeat data according to business rules.
    This is pure logic - no database, no files, no network calls.
    """
    if not site_id or len(site_id) < 3:
        return False
    if not timestamp:
        return False
    return True


def classify_alert(alert_type: str) -> str:
    """
    TODO: Implement alert classification logic.
    
    Takes an alert type and returns its severity level.
    Business rules:
    - LEAK: CRITICAL
    - BLOCKAGE: CRITICAL
    - PRESSURE: MODERATE
    - TEMPERATURE: MODERATE
    - ACOUSTIC: MODERATE
    
    Args:
        alert_type: One of PRESSURE, TEMPERATURE, LEAK, ACOUSTIC, BLOCKAGE
        
    Returns:
        "CRITICAL" or "MODERATE"
    """
    # TODO: Implement this function
    pass
