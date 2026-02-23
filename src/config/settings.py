import os
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator

# Load variables once when the module is imported
load_dotenv()


class Settings(BaseModel):
    """
    Application configuration sourced from environment variables.

    TODO (Week 4): Implement the following:
    - from_env classmethod to read required env vars
    - validators for env, database_url, api_token, and log_level
    """
    env: str
    database_url: str
    api_token: str
    log_level: str = "INFO"

    @classmethod
    def from_env(cls):
        env = os.getenv("APP_ENV")
        database_url = os.getenv("DATABASE_URL")
        api_token = os.getenv("API_TOKEN")

        # Explicit check for missing vars (required by tests)
        missing = [k for k, v in {"APP_ENV": env, "DATABASE_URL": database_url, "API_TOKEN": api_token}.items() if v is None]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return cls(
            env=env,
            database_url=database_url,
            api_token=api_token
        )

        Optional variables:
        - LOG_LEVEL (defaults to INFO)

        TODO: Implement reading and missing-variable handling.
        """
        load_dotenv()

        values = {
            "env": os.getenv("APP_ENV"),
            "database_url": os.getenv("DATABASE_URL"),
            "api_token": os.getenv("API_TOKEN"),
        }

        missing = [
            field
            for field in ("env", "database_url", "api_token")
            if values[field] is None
        ]
        if missing:
            raise ValueError(
                "Missing required environment variable(s): " + ", ".join(missing)
            )

        return cls(**values)

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str):
        if not v or not v.strip():
            raise ValueError("database_url cannot be empty")
        if not v.endswith(".db"):
            raise ValueError("database_url must end with .db")
        return v

    @field_validator("env")
    def validate_env(cls, value):
        valid = {"dev", "test", "prod"}
        if value not in valid:
            raise ValueError("env must be one of: dev, test, prod")
        return value

    # TODO: Add @field_validator for database_url
    # Must end with .db and not be empty

    @field_validator("database_url")
    def validate_database_url(cls, value):
        if value is None or value.strip() == "":
            raise ValueError("database_url must be non-empty")
        if not value.endswith(".db"):
            raise ValueError("database_url must end with .db")
        return value

    # TODO: Add @field_validator for api_token
    # Must be non-empty

    @field_validator("api_token")
    def validate_api_token(cls, value):
        if value is None or value.strip() == "":
            raise ValueError("api_token must be non-empty")
        return value

    # TODO: Add @field_validator for log_level
    # Valid values: DEBUG, INFO, WARNING, ERROR, CRITICAL
