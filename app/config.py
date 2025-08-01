from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from functools import lru_cache

class Settings(BaseSettings):
    MST_BASE_URL: AnyUrl
    BOT_TOKEN: str
    ADMIN_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str
    DRY_RUN: bool = True
    BATCH_SIZE: int = 80
    MAX_PAGES_PER_POLL: int = 3
    USER_AGENT: str = "MastoWatch/1.0 (+moderation-sidecar)"

    class Config:
        case_sensitive = True

@lru_cache
def get_settings():
    return Settings()
