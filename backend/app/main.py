import time
import uuid

import sentry_sdk
import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.routers import (
    agent,
    auth,
    channels,
    jobs,
    market,
    messenger,
    products,
    reports,
    sales,
)
from app.routers import settings as settings_router
from app.routers import usage

configure_logging()
logger = structlog.get_logger()

if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, integrations=[FastApiIntegration()], traces_sample_rate=0.1)

app = FastAPI(title="SatGit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5183"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        structlog.contextvars.bind_contextvars(request_id=request_id)
        start = time.perf_counter()
        try:
            response = await call_next(request)
        finally:
            duration_ms = int((time.perf_counter() - start) * 1000)
        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )
        structlog.contextvars.clear_contextvars()
        response.headers["X-Request-ID"] = request_id
        return response


app.add_middleware(RequestLoggingMiddleware)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(channels.router)
app.include_router(messenger.router)
app.include_router(market.router)
app.include_router(agent.router)
app.include_router(reports.router)
app.include_router(jobs.router)
app.include_router(jobs.ws_router)
app.include_router(settings_router.router)
app.include_router(usage.router)


@app.get("/health")
def health():
    return {"status": "ok"}
