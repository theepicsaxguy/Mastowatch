from functools import lru_cache

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


APP_VERSION = "0.1.0"


class Settings(BaseSettings):
    VERSION: str = APP_VERSION
    INSTANCE_BASE: AnyUrl
    BOT_TOKEN: str = Field(..., min_length=1)
    ADMIN_TOKEN: str = Field(..., min_length=1)
    DATABASE_URL: str = Field(..., min_length=1)
    REDIS_URL: str = Field(..., min_length=1)
    DRY_RUN: bool = True
    MAX_PAGES_PER_POLL: int = 3
    USER_AGENT: str = f"MastoWatch/{APP_VERSION} (+moderation-sidecar)"
    HTTP_TIMEOUT: float = 30.0
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
    OAUTH_SCOPE: str = "read:accounts"
    OAUTH_POPUP_REDIRECT_URI: str | None = None
    SESSION_SECRET_KEY: str | None = None
    SESSION_COOKIE_NAME: str = "mastowatch_session"
    SESSION_COOKIE_MAX_AGE: int = 86400  # 24 hours in seconds

    UI_ORIGIN: str = Field(..., min_length=1)

    MIN_MASTODON_VERSION: str = "4.0.0"
    POLL_ADMIN_ACCOUNTS_INTERVAL: int = 30
    POLL_ADMIN_ACCOUNTS_LOCAL_INTERVAL: int = 30
    QUEUE_STATS_INTERVAL: int = 15

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings():
    return Settings()
