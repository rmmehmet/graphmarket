import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.schemas.market import (
    CompetitorOut,
    MarketResearchJobOut,
    MarketResearchRequest,
    MarketResearchResultOut,
    TrendSignalOut,
)
from app.services.auth_service import AuthenticatedUser, get_current_user
from app.services.job_service import create_job, get_job
from app.services.market_service import list_competitors, list_trend_signals
from app.workers.celery_tasks import run_trend_research

router = APIRouter(prefix="/api/market", tags=["market"])


@router.post("/research", response_model=MarketResearchJobOut)
def start_research(
    payload: MarketResearchRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = create_job(
        db,
        current_user.team_id,
        "trend_research",
        input_payload={
            "category": payload.category,
            "product_id": str(payload.product_id) if payload.product_id else None,
        },
    )
    run_trend_research.delay(
        str(job.id),
        current_user.team_id,
        payload.category,
        str(payload.product_id) if payload.product_id else None,
    )
    return MarketResearchJobOut(job_id=job.id)


@router.get("/research/{job_id}", response_model=MarketResearchResultOut)
def get_research(
    job_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, current_user.team_id, job_id)
    result = json.loads(job.result_ref) if job.result_ref else None
    return MarketResearchResultOut(status=job.status, result=result)


@router.get("/trends", response_model=list[TrendSignalOut])
def get_trends(
    category: str | None = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return list_trend_signals(category)


@router.get("/competitors", response_model=list[CompetitorOut])
def get_competitors(
    category: str | None = None,
    product_id: str | None = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    return list_competitors(category, product_id)
