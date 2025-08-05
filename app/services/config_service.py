"""Database-backed configuration helpers."""

from typing import Any

from app.db import SessionLocal
from app.models import Config


class ConfigService:
    """CRUD operations for application configuration."""

    def get_config(self, key: str) -> Any | None:
        """Return configuration value for key."""
        with SessionLocal() as session:
            row = session.get(Config, key)
            return row.value if row else None

    def set_flag(self, key: str, enabled: bool, updated_by: str | None = None) -> dict[str, bool]:
        """Store boolean flag in configuration."""
        with SessionLocal() as session:
            config = session.get(Config, key)
            if config:
                config.value = {"enabled": enabled}
                config.updated_by = updated_by
            else:
                session.add(Config(key=key, value={"enabled": enabled}, updated_by=updated_by))
            session.commit()
            return {"enabled": enabled}

    def set_threshold(self, key: str, threshold: float, updated_by: str | None = None) -> dict[str, float]:
        """Store numeric threshold in configuration."""
        with SessionLocal() as session:
            config = session.get(Config, key)
            if config:
                config.value = {"threshold": threshold}
                config.updated_by = updated_by
            else:
                session.add(Config(key=key, value={"threshold": threshold}, updated_by=updated_by))
            session.commit()
            return {"threshold": threshold}


config_service = ConfigService()


def get_config_service() -> ConfigService:
    """Return ConfigService instance."""
    return config_service
