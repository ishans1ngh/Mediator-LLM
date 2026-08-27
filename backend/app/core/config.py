from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Mediator LLM"
    app_env: str = "development"
    debug: bool = True

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/mediator_llm"

    clinicaltrials_api_url: str = "https://clinicaltrials.gov/api/v2"

    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 500

    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    trial_candidate_limit: int = 20
    analysis_step_delay_seconds: float = 0.35
    http_timeout_seconds: float = 15.0

    # LLM Configuration
    llm_provider: str = "mock"
    llm_model: str = "mock-model"
    llm_api_key: str | None = None
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4000

    @field_validator("cors_origins", mode="before")
    @classmethod
    def coerce_cors(cls, value: str | list[str]) -> str:
        if isinstance(value, list):
            return ",".join(value)
        return value

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() in {"development", "dev", "local", "test"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
