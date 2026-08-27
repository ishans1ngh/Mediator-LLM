import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TrialCriterion(Base):
    __tablename__ = "trial_criteria"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trial_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("trials.id", ondelete="CASCADE"), nullable=False, index=True
    )
    criterion_type: Mapped[str] = mapped_column(String(32), nullable=False)
    criterion_text: Mapped[str] = mapped_column(Text, nullable=False)
    structured_field: Mapped[str | None] = mapped_column(String(128), nullable=True)
    operator: Mapped[str | None] = mapped_column(String(16), nullable=True)
    value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    trial: Mapped["Trial"] = relationship(back_populates="criteria")
    evaluations: Mapped[list["CriterionEvaluation"]] = relationship(back_populates="criterion")
