from fastapi import FastAPI

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

app = FastAPI(title="SatGit API")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(sales.router)
app.include_router(channels.router)
app.include_router(messenger.router)
app.include_router(market.router)
app.include_router(agent.router)
app.include_router(reports.router)
app.include_router(jobs.router)
app.include_router(settings_router.router)
app.include_router(usage.router)


@app.get("/health")
def health():
    return {"status": "ok"}
