import json
import time

from app.agents.graphs.trend_research import get_graph
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


_STEP_PROGRESS = {
    "planner": 15,
    "search_tool": 30,
    "extraction": 50,
    "graph_writer": 65,
    "vector_writer": 65,
    "synthesis": 85,
    "verification": 95,
}


@celery_app.task(name="jobs.trend_research")
def run_trend_research(job_id: str, team_id: str, category: str, product_id: str | None = None) -> str:
    with db_session() as db:
        update_job(db, job_id, status_="running", progress=5, step="queued")

    initial_state = {
        "job_id": job_id,
        "team_id": team_id,
        "category": category,
        "product_id": product_id,
        "retry_count": 0,
    }

    final_state = dict(initial_state)
    graph = get_graph()

    try:
        for step_update in graph.stream(initial_state, stream_mode="updates"):
            for node_name, node_state in step_update.items():
                final_state.update(node_state)
                with db_session() as db:
                    update_job(db, job_id, progress=_STEP_PROGRESS.get(node_name, 50), step=node_name)
    except Exception as exc:
        with db_session() as db:
            update_job(db, job_id, status_="error", error_message=str(exc), step="error")
        raise

    report = final_state.get("report", {})
    with db_session() as db:
        update_job(
            db,
            job_id,
            status_="done",
            progress=100,
            result_ref=json.dumps(report, ensure_ascii=False),
            step="done",
        )

    return job_id
