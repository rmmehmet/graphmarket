import time

from app.core.celery_app import celery_app
from app.services.job_service import db_session, update_job


@celery_app.task(name="jobs.mock_job")
def mock_job(job_id: str) -> str:
    """Faz 3 kuyruk altyapısını doğrulamak için kullanılan test task'ı."""
    steps = ["step_1", "step_2", "step_3"]

    with db_session() as db:
        update_job(db, job_id, status_="running", progress=0, step="started")

    for i, step in enumerate(steps, start=1):
        time.sleep(1)
        with db_session() as db:
            update_job(db, job_id, progress=int(i / len(steps) * 100), step=step)

    with db_session() as db:
        update_job(db, job_id, status_="done", progress=100, result_ref="mock result", step="done")

    return job_id
