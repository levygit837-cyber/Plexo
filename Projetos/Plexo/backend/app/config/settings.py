"""
Plexo Multi-Agent System - Application Settings

This module defines all application settings using Pydantic Settings.
Settings are loaded from environment variables with validation.
"""
from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables.
    See .env.example for available configuration options.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )
    
    # Application
    APP_NAME: str = Field(default="Plexo", description="Application name")
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    APP_ENV: str = Field(default="development", description="Environment (development/staging/production)")
    DEBUG: bool = Field(default=True, description="Debug mode")
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    
    # Server
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    
    # Database (PostgreSQL)
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://plexo:plexo@localhost:5432/plexo",
        description="PostgreSQL database URL"
    )
    DATABASE_POOL_SIZE: int = Field(default=20, description="Database connection pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=10, description="Database max overflow connections")
    
    # KuzuDB (Graph Database for Embeddings)
    KUZU_DB_PATH: str = Field(default="./data/kuzu", description="KuzuDB database path")
    
    # RabbitMQ
    RABBITMQ_URL: str = Field(
        default="amqp://guest:guest@localhost:5672/",
        description="RabbitMQ connection URL"
    )
    RABBITMQ_QUEUE_AGENTS: str = Field(default="plexo.agents", description="Agents queue name")
    RABBITMQ_QUEUE_TASKS: str = Field(default="plexo.tasks", description="Tasks queue name")
    RABBITMQ_QUEUE_BACKGROUND: str = Field(default="plexo.background", description="Background tasks queue name")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis connection URL")
    REDIS_CACHE_TTL: int = Field(default=3600, description="Redis cache TTL in seconds")
    
    # SPADE (XMPP)
    XMPP_SERVER: str = Field(default="localhost", description="XMPP server address")
    XMPP_PORT: int = Field(default=5222, description="XMPP server port")
    XMPP_DOMAIN: str = Field(default="localhost", description="XMPP domain")
    XMPP_ADMIN_JID: str = Field(default="admin@localhost", description="XMPP admin JID")
    XMPP_ADMIN_PASSWORD: str = Field(default="admin", description="XMPP admin password")
    
    # LangChain
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    LANGCHAIN_TRACING_V2: bool = Field(default=False, description="Enable LangChain tracing")
    LANGCHAIN_API_KEY: str = Field(default="", description="LangChain API key")
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for JWT encoding"
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration in minutes")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins"
    )
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            # Handle JSON string format from env
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # Handle comma-separated format
                return [origin.strip() for origin in v.split(",")]
        return v
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(default="json", description="Log format (json/text)")
    
    # Metrics
    METRICS_ENABLED: bool = Field(default=True, description="Enable metrics collection")
    PROMETHEUS_PORT: int = Field(default=9090, description="Prometheus metrics port")
    
    # Workers (Celery)
    CELERY_BROKER_URL: str = Field(
        default="amqp://guest:guest@localhost:5672/",
        description="Celery broker URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/1",
        description="Celery result backend URL"
    )
    CELERY_WORKER_CONCURRENCY: int = Field(default=4, description="Celery worker concurrency")
    
    @field_validator("APP_ENV")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"APP_ENV must be one of {allowed}")
        return v
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level value."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v_upper
    
    @field_validator("LOG_FORMAT")
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        """Validate log format value."""
        allowed = ["json", "text"]
        if v not in allowed:
            raise ValueError(f"LOG_FORMAT must be one of {allowed}")
        return v
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.APP_ENV == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.APP_ENV == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    This function uses lru_cache to ensure settings are loaded only once
    and reused across the application.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings()


def validate_settings(settings: Settings) -> bool:
    """
    Validate settings configuration.
    
    Args:
        settings: Settings instance to validate
        
    Returns:
        bool: True if settings are valid
        
    Raises:
        ValueError: If settings are invalid
    """
    # Validate production settings
    if settings.is_production():
        if settings.DEBUG:
            raise ValueError("DEBUG must be False in production")
        if settings.SECRET_KEY == "your-secret-key-here-change-in-production":
            raise ValueError("SECRET_KEY must be changed in production")
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set in production")
    
    return True