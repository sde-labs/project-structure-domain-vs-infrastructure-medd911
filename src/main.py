"""
Main application demonstrating clean architecture with validation.
"""
import logging

from pydantic import ValidationError

from src.config.settings import Settings
from src.domain.models import Alert
from src.domain.processor import classify_alert
from src.infrastructure.database import get_connection, initialize_database
from src.infrastructure.repositories import insert_alert


def process_alert_reading(conn, timestamp: str, site_id: str, alert_type: str,
                          latitude: float, longitude: float):
    """
    Process and store alert data with severity classification.

    Week 2 Note: This function now benefits from Pydantic validation in the
    Alert model. Invalid data (e.g., latitude > 90) will raise ValidationError
    before reaching this point if you use the Alert model to validate inputs.
    """
    # Step 1: Classify alert (Domain layer - pure logic, no I/O)
    severity = classify_alert(alert_type)

    # Step 2: Persist to database (Infrastructure layer - I/O)
    insert_alert(conn, timestamp, site_id, alert_type, severity, latitude, longitude)

    print(f"Alert recorded with severity: {severity}")


def load_settings() -> Settings:
    """
    Load application settings from environment.

    This fails fast if required environment variables are missing or invalid.
    """
    return Settings.from_env()


def build_logger(log_level: str, stream=None) -> logging.Logger:
    """
    Build and return the application logger.

    - Creates/gets a logger named "oil_well_monitoring"
    - Sets the logger level from `log_level`
    - Attaches one StreamHandler (uses `stream` if provided, else default stderr)
    - Format: %(asctime)s,%(levelname)s,%(message)s
    - Clears existing handlers first to avoid duplicates across repeated calls
    """
    logger = logging.getLogger("oil_well_monitoring")
    logger.setLevel(getattr(logging, log_level))

    # Remove any existing handlers to avoid duplicates when called repeatedly
    logger.handlers.clear()

    handler = logging.StreamHandler(stream)
    formatter = logging.Formatter(
        fmt="%(asctime)s,%(levelname)s,%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def process_alert_event(conn, logger: logging.Logger, timestamp: str, site_id: str,
                        alert_type: str, latitude: float, longitude: float,
                        max_retries: int = 2) -> Alert:
    """
    Validate, classify, persist, and log one alert.

    1. Validate input by constructing an Alert (fails fast, no retry)
    2. Classify severity (pure domain logic)
    3. Persist to DB with retry on failure
    """
    logger.debug("processing_alert site_id=%s type=%s", site_id, alert_type)

    # --- Step 1: Validate (no retry — bad data won't fix itself) ---
    try:
        severity = classify_alert(alert_type)
        alert = Alert(
            timestamp=timestamp,
            site_id=site_id,
            alert_type=alert_type,
            severity=severity,
            latitude=latitude,
            longitude=longitude,
        )
    except ValidationError:
        logger.exception("validation_failed site_id=%s", site_id)
        raise

    # --- Step 2: Persist with bounded retries ---
    for attempt in range(1, max_retries + 2):  # e.g. max_retries=2 → attempts 1,2,3
        try:
            insert_alert(
                conn, timestamp, site_id, alert_type,
                alert.severity, latitude, longitude,
            )
            logger.info("alert_recorded site_id=%s severity=%s", site_id, alert.severity)
            return alert
        except Exception as exc:
            if attempt <= max_retries:
                logger.warning(
                    "retrying_persist attempt=%d/%d site_id=%s error=%s",
                    attempt, max_retries, site_id, exc,
                )
            else:
                # All retries exhausted — log WITH traceback, then re-raise
                logger.exception(
                    "alert_processing_failed site_id=%s after %d retries",
                    site_id, max_retries,
                )
                raise


# Example usage
if __name__ == "__main__":
    settings = load_settings()
    print(f"Running in {settings.env} with DB {settings.database_url}")
