"""
Startup validation for critical environment variables and configuration.
"""

import logging
import sys
from typing import List

from pydantic import ValidationError

from app.config import get_settings

logger = logging.getLogger(__name__)


def validate_startup_configuration() -> None:
    """
    Validate that all critical configuration is present and properly formatted.
    Fail fast with clear error messages if anything is missing or invalid.
    """
    errors: List[str] = []

    try:
        settings = get_settings()

        # Critical API tokens
        if not settings.BOT_TOKEN or settings.BOT_TOKEN == "REPLACE_WITH_BOT_ACCESS_TOKEN":
            errors.append("BOT_TOKEN is missing or contains placeholder value")

        if not settings.ADMIN_TOKEN or settings.ADMIN_TOKEN == "REPLACE_WITH_ADMIN_ACCESS_TOKEN":
            errors.append("ADMIN_TOKEN is missing or contains placeholder value")

        # Database and Redis connectivity
        if not settings.DATABASE_URL:
            errors.append("DATABASE_URL is required")
        elif "REPLACE" in settings.DATABASE_URL.upper():
            errors.append("DATABASE_URL contains placeholder values")

        if not settings.REDIS_URL:
            errors.append("REDIS_URL is required")
        elif "REPLACE" in settings.REDIS_URL.upper():
            errors.append("REDIS_URL contains placeholder values")

        # Instance configuration
        if not settings.INSTANCE_BASE:
            errors.append("INSTANCE_BASE is required")
        elif str(settings.INSTANCE_BASE) == "https://your.instance":
            errors.append("INSTANCE_BASE contains placeholder value")

        # API security
        if settings.API_KEY == "REPLACE_ME":
            errors.append("API_KEY contains placeholder value (set to secure value or null to disable)")

        # Webhook security (if webhooks enabled)
        if settings.WEBHOOK_SECRET == "REPLACE_ME":
            errors.append("WEBHOOK_SECRET contains placeholder value (set to secure value or null to disable webhooks)")

        # Validate numeric ranges
        if settings.MAX_PAGES_PER_POLL < 1:
            errors.append("MAX_PAGES_PER_POLL must be >= 1")

        if settings.MAX_STATUSES_TO_FETCH < 1:
            errors.append("MAX_STATUSES_TO_FETCH must be >= 1")

        if settings.BATCH_SIZE < 1:
            errors.append("BATCH_SIZE must be >= 1")

        # Validate report category
        valid_categories = {"spam", "violation", "legal", "other"}
        if settings.REPORT_CATEGORY_DEFAULT not in valid_categories:
            errors.append(f"REPORT_CATEGORY_DEFAULT must be one of: {valid_categories}")

    except ValidationError as e:
        errors.append(f"Configuration validation failed: {e}")
    except Exception as e:
        errors.append(f"Unexpected error during configuration validation: {e}")

    if errors:
        logger.error("STARTUP VALIDATION FAILED:")
        for error in errors:
            logger.error(f"  - {error}")
        logger.error("Please fix the above configuration issues before starting the application.")
        sys.exit(1)
    else:
        logger.info("✓ Startup configuration validation passed")


def validate_database_connection() -> None:
    """
    Test database connectivity and migration status.
    """
    try:
        from sqlalchemy import text

        from app.db import SessionLocal

        with SessionLocal() as db:
            # Test basic connectivity
            result = db.execute(text("SELECT 1")).scalar()
            if result != 1:
                raise Exception("Database connectivity test failed")

            # Check if migrations table exists (indicates Alembic is set up)
            try:
                db.execute(text("SELECT version_num FROM alembic_version LIMIT 1"))
                logger.info("✓ Database connected and migrations table found")
            except Exception:
                logger.warning("⚠ Database connected but no migrations table found - run 'alembic upgrade head'")

    except Exception as e:
        logger.error(f"Database validation failed: {e}")
        sys.exit(1)


def validate_redis_connection() -> None:
    """
    Test Redis connectivity.
    """
    try:
        import redis

        from app.config import get_settings

        settings = get_settings()
        r = redis.from_url(settings.REDIS_URL)

        if not r.ping():
            raise Exception("Redis ping failed")

        logger.info("✓ Redis connection validated")

    except Exception as e:
        logger.error(f"Redis validation failed: {e}")
        sys.exit(1)


def run_all_startup_validations() -> None:
    """
    Run all startup validations. Call this early in application startup.
    Can be disabled by setting SKIP_STARTUP_VALIDATION environment variable.
    """
    import os

    if os.getenv("SKIP_STARTUP_VALIDATION"):
        logger.info("Startup validations skipped (SKIP_STARTUP_VALIDATION set)")
        return

    logger.info("Running startup validations...")
    validate_startup_configuration()
    validate_database_connection()
    validate_redis_connection()
    logger.info("✓ All startup validations passed")
