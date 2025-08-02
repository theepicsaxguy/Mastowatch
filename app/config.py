from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field
from functools import lru_cache

class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    INSTANCE_BASE: AnyUrl
    BOT_TOKEN: str
    ADMIN_TOKEN: str = Field(..., min_length=1)
    DATABASE_URL: str
    REDIS_URL: str
    DRY_RUN: bool = True
    BATCH_SIZE: int = 80
    MAX_PAGES_PER_POLL: int = 3
    USER_AGENT: str = "MastoWatch/1.0 (+moderation-sidecar)"
    MAX_STATUSES_TO_FETCH: int = 5

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

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings():
    return Settings()
