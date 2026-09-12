import json
from contextlib import contextmanager

import redis
import structlog
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.postgres import SessionLocal
from app.models.job import Job

_redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
logger = structlog.get_logger()


def job_channel(job_id: str) -> str:
    return f"job:{job_id}"


@contextmanager
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_job(db: Session, team_id: str, job_type: str, input_payload: dict | None = None) -> Job:
    job = Job(team_id=team_id, type=job_type, status="queued", progress=0, input_payload=input_payload)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job(db: Session, team_id: str, job_id: str) -> Job:
    job = db.scalar(select(Job).where(Job.id == job_id, Job.team_id == team_id))
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")
    return job


def list_jobs(db: Session, team_id: str, job_type: str | None, limit: int = 50) -> list[Job]:
    query = select(Job).where(Job.team_id == team_id)
    if job_type:
        query = query.where(Job.type == job_type)
    query = query.order_by(Job.created_at.desc()).limit(limit)
    return list(db.scalars(query))


def update_job(
    db: Session,
    job_id: str,
    *,
    status_: str | None = None,
    progress: int | None = None,
    result_ref: str | None = None,
    error_message: str | None = None,
    step: str | None = None,
) -> Job:
    job = db.scalar(select(Job).where(Job.id == job_id))
    if job is None:
        raise ValueError(f"job {job_id} not found")

    if status_ is not None:
        job.status = status_
    if progress is not None:
        job.progress = progress
    if result_ref is not None:
        job.result_ref = result_ref
    if error_message is not None:
        job.error_message = error_message
    db.commit()
    db.refresh(job)

    logger.info(
        "job_updated",
        job_id=str(job.id),
        job_type=job.type,
        status=job.status,
        progress=job.progress,
        step=step,
    )

    _redis_client.publish(
        job_channel(str(job.id)),
        json.dumps({"step": step or job.status, "status": job.status, "progress": job.progress}),
    )
    return job
