from celery import Celery
import os

broker_url = os.environ.get("REDIS_URL")
backend_url = os.environ.get("REDIS_URL")

celery_app = Celery("mastowatch", broker=broker_url, backend=backend_url, include=["app.tasks.jobs"])
celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=4,
    broker_transport_options={"visibility_timeout": 3600},
    beat_schedule={
        "poll-admin-accounts-every-30s": {
            "task": "app.tasks.jobs.poll_admin_accounts",
            "schedule": 30.0,
        }
    }
)
