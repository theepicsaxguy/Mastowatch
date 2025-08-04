"""Application configuration."""

from functools import lru_cache

from pydantic import AnyUrl, Field, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Pydantic settings for the application."""

    VERSION: str = "0.1.0"
    INSTANCE_BASE: AnyUrl
    BOT_TOKEN: str = Field(..., min_length=1)
    ADMIN_TOKEN: str = Field(..., min_length=1)
    DATABASE_URL: str = Field(..., min_length=1)
    REDIS_URL: str = Field(..., min_length=1)
    DRY_RUN: bool = True
    MAX_PAGES_PER_POLL: int = 3
    USER_AGENT: str | None = None
    MAX_STATUSES_TO_FETCH: int = 5
    BATCH_SIZE: int = 20

    # Reporting behavior
    REPORT_CATEGORY_DEFAULT: str = "spam"  # spam | violation | legal | other
    FORWARD_REMOTE_REPORTS: bool = False
    POLICY_VERSION: str = "v1"

    # Ops toggles
    PANIC_STOP: bool = False
    API_KEY: str | None = None

    # Webhooks
    WEBHOOK_SECRET: str | None = None
    WEBHOOK_SIG_HEADER: str = "X-Hub-Signature-256"  # sha256=<hexdigest>

    # CORS for dashboard if served separately (not required when embedded)
    CORS_ORIGINS: list[str] = []

    # OAuth Configuration for admin login
    OAUTH_CLIENT_ID: str | None = None
    OAUTH_CLIENT_SECRET: str | None = None
    OAUTH_REDIRECT_URI: str | None = None
    OAUTH_POPUP_REDIRECT_URI: str | None = None
    SESSION_SECRET_KEY: str | None = None
    SESSION_COOKIE_NAME: str = "mastowatch_session"
    SESSION_COOKIE_MAX_AGE: int = 86400  # 24 hours in seconds

    # Frontend UI origin for popup postMessage
    UI_ORIGIN: str = "http://localhost:5173"

    @model_validator(mode="after")
    def set_user_agent(self) -> "Settings":
        """Populate USER_AGENT from VERSION when missing."""
        if not self.USER_AGENT:
            self.USER_AGENT = f"MastoWatch/{self.VERSION} (+moderation-sidecar)"
        return self

    class Config:
        """Pydantic configuration."""

        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return Settings()
