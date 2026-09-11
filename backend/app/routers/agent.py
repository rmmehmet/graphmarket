from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.schemas.agent import (
    AgentHistoryItem,
    AskDeepRequest,
    AskDeepResponse,
    AskRequest,
    AskResponse,
)
from app.services.agent_service import create_ask_deep_record, list_history, run_ask
from app.services.auth_service import AuthenticatedUser, get_current_user
from app.services.job_service import create_job
from app.services.quota_service import check_and_increment
from app.workers.celery_tasks import run_sales_insight_deep

router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("/ask", response_model=AskResponse)
def ask_endpoint(
    payload: AskRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    answer, citations = run_ask(
        db,
        current_user.team_id,
        payload.question,
        str(payload.context_product_id) if payload.context_product_id else None,
    )
    return AskResponse(answer=answer, citations=citations)


@router.post("/ask-deep", response_model=AskDeepResponse)
def ask_deep_endpoint(
    payload: AskDeepRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_and_increment(db, current_user.team_id, "agent_ask_deep")

    job = create_job(
        db, current_user.team_id, "agent_ask_deep", input_payload={"question": payload.question}
    )
    create_ask_deep_record(db, current_user.team_id, payload.question, str(job.id))
    run_sales_insight_deep.delay(str(job.id), current_user.team_id, payload.question)
    return AskDeepResponse(job_id=job.id)


@router.get("/history", response_model=list[AgentHistoryItem])
def history_endpoint(
    limit: int = 20,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_history(db, current_user.team_id, limit)
