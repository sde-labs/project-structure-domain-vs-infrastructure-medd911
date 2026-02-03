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
    classification = {
        "PRESSURE": "MODERATE",
        "TEMPERATURE": "MODERATE",
        "LEAK": "CRITICAL",
        "ACOUSTIC": "MODERATE",
        "BLOCKAGE": "CRITICAL",
    }

    return classification.get(alert_type, "MODERATE")

