import asyncio

import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.postgres import get_db
from app.schemas.job import JobOut, JobSummaryOut
from app.services.auth_service import AuthenticatedUser, get_current_user
from app.services.job_service import get_job, job_channel, list_jobs

router = APIRouter(prefix="/api/jobs", tags=["jobs"])
ws_router = APIRouter()


@router.get("/", response_model=list[JobSummaryOut])
def list_jobs_endpoint(
    type: str | None = None,
    limit: int = 50,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_jobs(db, current_user.team_id, type, limit)


@router.get("/{job_id}", response_model=JobOut)
def get_job_endpoint(
    job_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_job(db, current_user.team_id, job_id)


@ws_router.websocket("/ws/jobs/{job_id}")
async def job_status_ws(websocket: WebSocket, job_id: str):
    await websocket.accept()
    redis_client = aioredis.Redis(
        host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
    )
    pubsub = redis_client.pubsub()
    channel = job_channel(job_id)
    await pubsub.subscribe(channel)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message is not None:
                data = message["data"]
                await websocket.send_text(data.decode() if isinstance(data, bytes) else data)
            else:
                await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(channel)
        await redis_client.close()
