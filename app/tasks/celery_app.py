from celery import Celery
from app.config import settings


celery_app = Celery(
    "crypto_price_tracker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

celery_app.conf.beat_schedule = {
    "fetch-crypto-prices-every-minute": {
        "task": "app.tasks.tasks.fetch_and_save_prices",
        "schedule": settings.CELERY_BEAT_SCHEDULE_INTERVAL,
    },
}

celery_app.autodiscover_tasks(["app.tasks"])
