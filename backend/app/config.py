"""Configuration settings for Mindmesh Backend."""

from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "Mindmesh API"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")

    # Database
    database_url: str = Field(..., env="DATABASE_URL")

    # Supabase
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_anon_key: str = Field(..., env="SUPABASE_ANON_KEY")
    supabase_service_key: str = Field(..., env="SUPABASE_SERVICE_KEY")
    supabase_jwt_secret: str = Field(..., env="SUPABASE_JWT_SECRET")

    # Gemini AI
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    gemini_model: str = Field(default="gemini-2.5-flash", env="GEMINI_MODEL")
    gemini_temperature: float = Field(default=0.3, env="GEMINI_TEMPERATURE")
    gemini_max_tokens: int = Field(default=2048, env="GEMINI_MAX_TOKENS")

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "https://mindmesh.vercel.app"],
        env="CORS_ORIGINS"
    )

    @field_validator("cors_origins", mode="before")
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()