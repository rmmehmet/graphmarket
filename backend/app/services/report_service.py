from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.channel import Channel
from app.models.report import Report
from app.models.sale import SalesRecord


def create_report_stub(
    db: Session, team_id: str, job_id: str, period_start: date, period_end: date
) -> Report:
    report = Report(
        team_id=team_id, job_id=job_id, period_start=period_start, period_end=period_end, content=None
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def save_report_content(db: Session, report_id: str, content: dict) -> None:
    report = db.scalar(select(Report).where(Report.id == report_id))
    if report is not None:
        report.content = content
        db.commit()


def list_reports(db: Session, team_id: str) -> list[Report]:
    stmt = select(Report).where(Report.team_id == team_id).order_by(Report.period_end.desc())
    return db.scalars(stmt).all()


def get_report(db: Session, team_id: str, report_id: str) -> Report:
    report = db.scalar(select(Report).where(Report.id == report_id, Report.team_id == team_id))
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="report not found")
    return report


def gather_sales_summary(
    db: Session, team_id: str, period_start: date, period_end: date, channel_ids: list[str]
) -> dict:
    stmt = select(SalesRecord).where(
        SalesRecord.team_id == team_id,
        SalesRecord.sold_at >= period_start,
        SalesRecord.sold_at <= period_end,
    )
    if channel_ids:
        stmt = stmt.where(SalesRecord.channel_id.in_(channel_ids))
    sales = db.scalars(stmt).all()

    total_revenue = sum(float(s.price) * s.quantity for s in sales)
    total_quantity = sum(s.quantity for s in sales)

    by_channel: dict[str, dict] = {}
    for s in sales:
        key = str(s.channel_id)
        bucket = by_channel.setdefault(key, {"revenue": 0.0, "quantity": 0})
        bucket["revenue"] += float(s.price) * s.quantity
        bucket["quantity"] += s.quantity

    channel_names = {str(c.id): c.name for c in db.scalars(select(Channel).where(Channel.team_id == team_id))}
    breakdown = [
        {"channel": channel_names.get(k, k), "revenue": v["revenue"], "quantity": v["quantity"]}
        for k, v in by_channel.items()
    ]

    return {
        "sale_count": len(sales),
        "total_revenue": total_revenue,
        "total_quantity": total_quantity,
        "breakdown": breakdown,
    }
