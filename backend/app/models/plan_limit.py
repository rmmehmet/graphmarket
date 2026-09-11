from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PlanLimit(Base):
    __tablename__ = "plan_limits"

    plan: Mapped[str] = mapped_column(String, primary_key=True)
    monthly_trend_research: Mapped[int | None] = mapped_column(Integer, nullable=True)
    monthly_agent_ask_deep: Mapped[int | None] = mapped_column(Integer, nullable=True)
    monthly_messenger_sync: Mapped[int | None] = mapped_column(Integer, nullable=True)
