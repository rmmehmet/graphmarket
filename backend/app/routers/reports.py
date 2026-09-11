from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.schemas.report import ReportGenerateRequest, ReportGenerateResponse, ReportOut
from app.services.auth_service import AuthenticatedUser, get_current_user
from app.services.job_service import create_job
from app.services.report_service import create_report_stub, get_report, list_reports
from app.workers.celery_tasks import run_report_generate

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/", response_model=list[ReportOut])
def list_reports_endpoint(
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_reports(db, current_user.team_id)


@router.post("/generate", response_model=ReportGenerateResponse)
def generate_report_endpoint(
    payload: ReportGenerateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = create_job(
        db,
        current_user.team_id,
        "report_generate",
        input_payload={
            "type": payload.type,
            "period_start": payload.period.start.isoformat(),
            "period_end": payload.period.end.isoformat(),
            "channel_ids": [str(c) for c in payload.channel_ids],
        },
    )
    report = create_report_stub(
        db, current_user.team_id, str(job.id), payload.period.start, payload.period.end
    )
    run_report_generate.delay(
        str(job.id),
        current_user.team_id,
        str(report.id),
        payload.type,
        payload.period.start.isoformat(),
        payload.period.end.isoformat(),
        [str(c) for c in payload.channel_ids],
    )
    return ReportGenerateResponse(job_id=job.id)


@router.get("/{report_id}", response_model=ReportOut)
def get_report_endpoint(
    report_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_report(db, current_user.team_id, report_id)
