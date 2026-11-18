from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # LLM
    GEMINI_API_KEY: str = ""

    # Website extraction
    MAX_CONTENT_LENGTH: int = 8000  # max chars sent to LLM after cleaning
    REQUEST_TIMEOUT: int = 15       # seconds for HTTP fetch

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
