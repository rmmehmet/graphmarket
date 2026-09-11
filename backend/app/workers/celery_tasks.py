import json
import time
from datetime import date as date_cls
from decimal import Decimal

from app.agents.graphs.messenger_extraction import get_graph as get_messenger_graph
from app.agents.graphs.sales_insight import get_graph as get_sales_insight_graph
from app.agents.graphs.trend_research import get_graph as get_trend_research_graph
from app.agents.nodes import synthesis as synthesis_node
from app.core.celery_app import celery_app
from app.services.agent_service import complete_ask_deep_record
from app.services.job_service import db_session, update_job
from app.services.report_service import gather_sales_summary, save_report_content


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
    graph = get_trend_research_graph()

    try:
        for step_update in graph.stream(initial_state, stream_mode="updates"):
            for node_name, node_state in step_update.items():
                if node_state:
                    final_state.update(node_state)
                with db_session() as db:
                    update_job(db, job_id, progress=_STEP_PROGRESS.get(node_name, 50), step=node_name)
    except Exception as exc:
        with db_session() as db:
            update_job(db, job_id, status_="error", error_message=str(exc), step="error")
        raise

    extracted = final_state.get("extracted", {})
    report = {
        "category": category,
        "text": final_state.get("synthesis_output", ""),
        "sources": extracted.get("source_count", 0),
    }
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


_SALES_INSIGHT_STEP_PROGRESS = {"planner": 20, "retrieval": 50, "synthesis": 80, "verification": 95}


@celery_app.task(name="jobs.sales_insight_deep")
def run_sales_insight_deep(job_id: str, team_id: str, question: str) -> str:
    with db_session() as db:
        update_job(db, job_id, status_="running", progress=5, step="queued")

    initial_state = {
        "job_id": job_id,
        "team_id": team_id,
        "question": question,
        "context_product_id": None,
        "retry_count": 0,
    }

    final_state = dict(initial_state)
    graph = get_sales_insight_graph()

    try:
        for step_update in graph.stream(initial_state, stream_mode="updates"):
            for node_name, node_state in step_update.items():
                if node_state:
                    final_state.update(node_state)
                with db_session() as db:
                    update_job(
                        db, job_id, progress=_SALES_INSIGHT_STEP_PROGRESS.get(node_name, 50), step=node_name
                    )
    except Exception as exc:
        with db_session() as db:
            update_job(db, job_id, status_="error", error_message=str(exc), step="error")
        raise

    answer = final_state.get("synthesis_output", "")
    citations = final_state.get("citations", [])
    result = {"answer": answer, "citations": citations}

    with db_session() as db:
        update_job(
            db,
            job_id,
            status_="done",
            progress=100,
            result_ref=json.dumps(result, ensure_ascii=False),
            step="done",
        )
        complete_ask_deep_record(db, job_id, answer, citations)

    return job_id


def _maybe_log_inferred_sale(team_id: str, final_state: dict, channel_id: str | None) -> None:
    """extraction bir ürün eşleşmesi + fiyat bulduysa, sales_records'a source='messenger_inferred'
    ile otomatik bir satış kaydı düşer (Mimari doc bölüm 5 — sales_records.source enum'u).
    """
    extracted = final_state.get("extracted", {})
    product_id = final_state.get("matched_product_id")
    price = extracted.get("price")
    if not product_id or price is None or channel_id is None:
        return

    from app.services.sales_service import create_sale

    with db_session() as db:
        try:
            sale = create_sale(db, team_id, product_id, channel_id, Decimal(str(price)), 1, None)
            sale.source = "messenger_inferred"
            db.commit()
        except Exception:
            db.rollback()


@celery_app.task(name="jobs.messenger_webhook_message")
def run_messenger_webhook_message(
    job_id: str, team_id: str, message_text: str, customer_ref: str, channel_id: str | None, source: str
) -> str:
    with db_session() as db:
        update_job(db, job_id, status_="running", progress=10, step="extraction")

    graph = get_messenger_graph()
    try:
        final_state = graph.invoke(
            {
                "job_id": job_id,
                "team_id": team_id,
                "message_text": message_text,
                "customer_ref": customer_ref,
                "channel_id": channel_id,
                "source": source,
            }
        )
    except Exception as exc:
        with db_session() as db:
            update_job(db, job_id, status_="error", error_message=str(exc), step="error")
        raise

    _maybe_log_inferred_sale(team_id, final_state, channel_id)

    with db_session() as db:
        update_job(
            db,
            job_id,
            status_="done",
            progress=100,
            step="done",
            result_ref=json.dumps({"extracted": final_state.get("extracted", {})}, ensure_ascii=False),
        )

    return job_id


@celery_app.task(name="jobs.messenger_import_batch")
def run_messenger_import_batch(
    job_id: str, team_id: str, messages: list[dict], channel_id: str | None = None
) -> str:
    total = len(messages) or 1
    with db_session() as db:
        update_job(db, job_id, status_="running", progress=0, step="started")

    graph = get_messenger_graph()
    processed = 0
    errors: list[str] = []

    for msg in messages:
        try:
            final_state = graph.invoke(
                {
                    "job_id": job_id,
                    "team_id": team_id,
                    "message_text": msg["text"],
                    "customer_ref": msg["customer_ref"],
                    "channel_id": channel_id,
                    "source": "messenger_export",
                }
            )
            _maybe_log_inferred_sale(team_id, final_state, channel_id)
        except Exception as exc:
            errors.append(str(exc))

        processed += 1
        with db_session() as db:
            update_job(db, job_id, progress=int(processed / total * 100), step=f"message_{processed}")

    with db_session() as db:
        update_job(
            db,
            job_id,
            status_="done",
            progress=100,
            step="done",
            result_ref=json.dumps({"processed": processed, "errors": errors}, ensure_ascii=False),
        )

    return job_id


@celery_app.task(name="jobs.report_generate")
def run_report_generate(
    job_id: str,
    team_id: str,
    report_id: str,
    report_type: str,
    period_start: str,
    period_end: str,
    channel_ids: list[str],
) -> str:
    with db_session() as db:
        update_job(db, job_id, status_="running", progress=20, step="gathering")

    with db_session() as db:
        summary = gather_sales_summary(
            db,
            team_id,
            date_cls.fromisoformat(period_start),
            date_cls.fromisoformat(period_end),
            channel_ids,
        )

    prompt = (
        f"Aşağıdaki satış özetine dayanarak {period_start} - {period_end} dönemi için kısa bir "
        "Türkçe iş raporu yaz (toplam gelir, en iyi kanal, kısa yorum, 4-5 madde):\n\n"
        f"Toplam gelir: {summary['total_revenue']:.2f}\n"
        f"Toplam adet: {summary['total_quantity']}\n"
        f"Satış sayısı: {summary['sale_count']}\n"
        f"Kanal dağılımı: {summary['breakdown']}"
    )

    with db_session() as db:
        update_job(db, job_id, progress=60, step="synthesis")

    # Sentez düğümü doğrudan reuse ediliyor (Trend Research/Sales Insight ile aynı fonksiyon)
    synthesis_result = synthesis_node.run({"team_id": team_id, "synthesis_prompt": prompt})
    narrative = synthesis_result.get("synthesis_output", "")

    content = {"type": report_type, "summary": summary, "narrative": narrative}

    with db_session() as db:
        save_report_content(db, report_id, content)
        update_job(
            db,
            job_id,
            status_="done",
            progress=100,
            step="done",
            result_ref=json.dumps({"report_id": report_id}, ensure_ascii=False),
        )

    return job_id
