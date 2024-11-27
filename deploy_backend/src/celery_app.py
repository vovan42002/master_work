from config import settings
from celery import Celery


app = Celery(
    __name__,
    include=["celery_tasks"],
    broker=settings.celery_broker,
    broker_connection_retry_on_startup=True,
)
