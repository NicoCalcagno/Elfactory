"""Configuration management using Pydantic settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    openai_api_key: str
    openai_model: str = "gpt-4"

    workshop_email: str = "letterine@santas-workshop.ai"
    max_concurrent_gifts: int = 5

    enable_tracing: bool = True
    log_level: str = "INFO"

    # Test settings
    test_email_content: str = ""
    test_recipient_email: str = ""


settings = Settings()
