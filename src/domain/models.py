"""
Domain models - pure data structures with no I/O logic
"""
from dataclasses import dataclass


@dataclass
class Heartbeat:
    site_id: str
    timestamp: str


@dataclass
class Alert:
    timestamp: str
    site_id: str
    alert_type: str
    severity: str
    latitude: float
    longitude: float
