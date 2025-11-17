"""Application configuration"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Project Info
    PROJECT_NAME: str = "Acquisition Lead Generation Engine"
    API_VERSION: str = "v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/leadgen"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS - Add ngrok URLs or use "*" for demos (set CORS_ALLOW_ALL=true in .env)
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_ALL: bool = False  # Set to True for demos/development

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Anthropic Claude
    ANTHROPIC_API_KEY: str = ""

    # CRM Integrations
    HUBSPOT_API_KEY: str = ""
    SALESFORCE_USERNAME: str = ""
    SALESFORCE_PASSWORD: str = ""
    SALESFORCE_SECURITY_TOKEN: str = ""

    # Email Services
    SENDGRID_API_KEY: str = ""

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Lead Scoring
    LEAD_SCORE_THRESHOLD: int = 70

    # Data Enrichment
    CLEARBIT_API_KEY: str = ""
    HUNTER_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
