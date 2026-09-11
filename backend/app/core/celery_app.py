import sentry_sdk
from celery import Celery
from sentry_sdk.integrations.celery import CeleryIntegration

from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, integrations=[CeleryIntegration()], traces_sample_rate=0.1)

celery_app = Celery(
    "satgit",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.celery_tasks"],
)
