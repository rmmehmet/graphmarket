from sqlalchemy import select
from sqlalchemy.orm import Session

from app.agents.graphs.sales_insight import get_graph
from app.models.agent_query import AgentQuery


def run_ask(
    db: Session, team_id: str, question: str, context_product_id: str | None
) -> tuple[str, list[dict]]:
    graph = get_graph()
    final_state = graph.invoke(
        {
            "job_id": None,
            "team_id": team_id,
            "question": question,
            "context_product_id": context_product_id,
            "retry_count": 0,
        }
    )
    answer = final_state.get("synthesis_output", "")
    citations = final_state.get("citations", [])

    row = AgentQuery(team_id=team_id, question=question, answer=answer, citations=citations, mode="ask")
    db.add(row)
    db.commit()

    return answer, citations


def create_ask_deep_record(db: Session, team_id: str, question: str, job_id: str) -> AgentQuery:
    row = AgentQuery(team_id=team_id, question=question, mode="ask_deep", job_id=job_id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def complete_ask_deep_record(db: Session, job_id: str, answer: str, citations: list[dict]) -> None:
    row = db.scalar(select(AgentQuery).where(AgentQuery.job_id == job_id))
    if row is not None:
        row.answer = answer
        row.citations = citations
        db.commit()


def list_history(db: Session, team_id: str, limit: int) -> list[AgentQuery]:
    stmt = (
        select(AgentQuery)
        .where(AgentQuery.team_id == team_id)
        .order_by(AgentQuery.created_at.desc())
        .limit(limit)
    )
    return db.scalars(stmt).all()
