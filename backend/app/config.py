"""Application configuration settings."""
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # Application
    APP_NAME: str = "Agrimatco Smart Crop Advisor"
    APP_DESCRIPTION: str = "AI-powered agricultural assistant"
    API_ENV: str = "development"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://agrimatco:agrimatco_password@localhost:5432/agrimatco_db"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600

    # JWT
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    JWT_REFRESH_EXPIRATION_DAYS: int = 30

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_EXPIRATION: int = 3600

    # OpenAI
    OPENAI_API_KEY: str = "sk-"
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_VISION_MODEL: str = "gpt-4-turbo-with-vision"
    OPENAI_MAX_TOKENS: int = 2000
    OPENAI_TEMPERATURE: float = 0.7

    # File Upload
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    ALLOWED_IMAGE_FORMATS: str = "jpg,jpeg,png,webp,gif"
    UPLOAD_DIR: str = "./uploads"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
    CORS_ALLOW_HEADERS: List[str] = ["Content-Type", "Authorization"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "*"]

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Feature Flags
    FEATURE_PDF_EXPORT: bool = True
    FEATURE_CHAT_ASSISTANT: bool = True
    FEATURE_PRODUCT_RECOMMENDATIONS: bool = True

    # Internationalization
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: List[str] = ["en", "ar"]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
