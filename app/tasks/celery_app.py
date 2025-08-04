from celery import Celery

from app.config import get_settings

settings = get_settings()

celery_app = Celery("mastowatch", broker=settings.REDIS_URL, backend=settings.REDIS_URL, include=["app.tasks.jobs"])
celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=4,
    broker_transport_options={"visibility_timeout": 3600},
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
