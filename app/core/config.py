from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Core services
    DATABASE_URL: str = Field(..., description="Database connection string")
    REDIS_URL: str = Field(..., description="Redis connection URL")
    COINGECKO_API: str = Field(
        default="https://api.coingecko.com/api/v3",
        description="Base URL for CoinGecko API",
    )

    # Environment awareness
    ENV: str = Field(
        default="development",
        description="Application environment (development, staging, production)",
    )
    DEBUG: bool = Field(
        default=True,
        description="Enable debug mode",
    )

    # Configuration for loading and parsing environment variables
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Singleton settings instance to be imported and reused across the app
settings = Settings()

