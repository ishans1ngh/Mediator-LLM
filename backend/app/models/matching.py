import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class MatchingResult(Base):
    __tablename__ = "matching_results"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    patient_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    trial_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("trials.id", ondelete="CASCADE"), nullable=False, index=True
    )
    match_score: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False, default=0)
    eligibility_status: Mapped[str] = mapped_column(String(32), nullable=False)
    criteria_passed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    criteria_failed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    criteria_unknown: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    analysis: Mapped["Analysis"] = relationship(back_populates="matching_results")
    trial: Mapped["Trial"] = relationship(back_populates="matching_results")
    evaluations: Mapped[list["CriterionEvaluation"]] = relationship(
        back_populates="matching_result", cascade="all, delete-orphan"
    )


class CriterionEvaluation(Base):
    __tablename__ = "criterion_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matching_result_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("matching_results.id", ondelete="CASCADE"), nullable=False, index=True
    )
    criterion_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("trial_criteria.id", ondelete="CASCADE"), nullable=False, index=True
    )
    result: Mapped[str] = mapped_column(String(16), nullable=False)
    patient_evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    patient_value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    required_value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    matching_result: Mapped[MatchingResult] = relationship(back_populates="evaluations")
    criterion: Mapped["TrialCriterion"] = relationship(back_populates="evaluations")
