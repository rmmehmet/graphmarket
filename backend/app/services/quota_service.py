from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.plan_limit import PlanLimit
from app.models.usage_counter import UsageCounter
from app.models.user import Team

_JOB_TYPE_TO_LIMIT_COLUMN = {
    "trend_research": "monthly_trend_research",
    "agent_ask_deep": "monthly_agent_ask_deep",
    "messenger_sync": "monthly_messenger_sync",
}


def current_period() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def _team_plan(db: Session, team_id: str) -> str:
    team = db.scalar(select(Team).where(Team.id == team_id))
    return team.plan if team else "free"


def check_and_increment(db: Session, team_id: str, job_type: str) -> None:
    """Maliyetli job'ları enqueue etmeden önce çağrılır: limit aşılmışsa 429, değilse sayaç
    artırılır. plan_limits'te satır yoksa ya da ilgili kolon NULL ise sınırsız kabul edilir.
    """
    limit_column = _JOB_TYPE_TO_LIMIT_COLUMN.get(job_type)
    if limit_column is None:
        return

    plan = _team_plan(db, team_id)
    plan_limit = db.scalar(select(PlanLimit).where(PlanLimit.plan == plan))
    limit_value = getattr(plan_limit, limit_column, None) if plan_limit else None

    if limit_value is None:
        return

    period = current_period()
    counter = db.scalar(
        select(UsageCounter).where(
            UsageCounter.team_id == team_id,
            UsageCounter.period == period,
            UsageCounter.job_type == job_type,
        )
    )
    used = counter.count if counter else 0

    if used >= limit_value:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Bu ayki '{job_type}' limitine ulaştınız ({limit_value}).",
        )

    if counter is None:
        db.add(UsageCounter(team_id=team_id, period=period, job_type=job_type, count=1))
    else:
        counter.count += 1
    db.commit()


def get_usage_breakdown(db: Session, team_id: str) -> dict:
    plan = _team_plan(db, team_id)
    plan_limit = db.scalar(select(PlanLimit).where(PlanLimit.plan == plan))
    period = current_period()

    breakdown = []
    for job_type, column in _JOB_TYPE_TO_LIMIT_COLUMN.items():
        limit_value = getattr(plan_limit, column, None) if plan_limit else None
        counter = db.scalar(
            select(UsageCounter).where(
                UsageCounter.team_id == team_id,
                UsageCounter.period == period,
                UsageCounter.job_type == job_type,
            )
        )
        used = counter.count if counter else 0
        remaining = None if limit_value is None else max(limit_value - used, 0)
        breakdown.append(
            {"job_type": job_type, "used": used, "limit": limit_value, "remaining": remaining}
        )

    return {"period": period, "plan": plan, "breakdown": breakdown}
