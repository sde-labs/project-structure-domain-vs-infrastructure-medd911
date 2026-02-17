import os
from dotenv import load_dotenv
from pydantic import BaseModel, field_validator

# Load variables once when the module is imported
load_dotenv()


class Settings(BaseModel):
    env: str
    database_url: str
    api_token: str

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

    @field_validator("env")
    @classmethod
    def validate_env(cls, v: str):
        allowed = {"dev", "test", "prod"}
        if v not in allowed:
            raise ValueError(f"env must be one of {allowed}")
        return v

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str):
        if not v or not v.strip():
            raise ValueError("database_url cannot be empty")
        if not v.endswith(".db"):
            raise ValueError("database_url must end with .db")
        return v

    @field_validator("api_token")
    @classmethod
    def validate_api_token(cls, v: str):
        if not v or not v.strip():
            raise ValueError("api_token cannot be empty")
        return v
