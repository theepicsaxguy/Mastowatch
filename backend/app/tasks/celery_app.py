"""Celery application configuration for MastoWatch.

This module configures the Celery application with:
- Database-backed beat scheduler for production reliability
- Task execution settings optimized for moderation workloads
- Scheduled tasks for polling and monitoring
"""

from app.config import get_settings
from celery import Celery

settings = get_settings()

celery_app = Celery("mastowatch", broker=settings.REDIS_URL, backend=settings.REDIS_URL, include=["app.tasks.jobs"])

# Configure celery for production use with database-backed beat scheduler
celery_app.conf.update(
    # Task execution settings
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=4,
    
    # Broker settings for reliability
    broker_transport_options={"visibility_timeout": 3600},
    
    # Database scheduler configuration
    beat_scheduler="celery_sqlalchemy_scheduler.schedulers:DatabaseScheduler",
    beat_schedule_filename="",  # Not used with DatabaseScheduler
    
    # Use SQLAlchemy database URL for scheduler storage
    beat_sqlalchemy_url=settings.DATABASE_URL,
    
    # Task schedule definitions (will be stored in database)
    beat_schedule={
        "poll-admin-accounts": {
            "task": "app.tasks.jobs.poll_admin_accounts",
            "schedule": settings.POLL_ADMIN_ACCOUNTS_INTERVAL,
        },
        "poll-admin-accounts-local": {
            "task": "app.tasks.jobs.poll_admin_accounts_local",
            "schedule": settings.POLL_ADMIN_ACCOUNTS_LOCAL_INTERVAL,
        },
        "queue-stats": {
            "task": "app.tasks.jobs.record_queue_stats",
            "schedule": settings.QUEUE_STATS_INTERVAL,
        },
    },
)
