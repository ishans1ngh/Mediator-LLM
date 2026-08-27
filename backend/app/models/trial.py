import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, String, Text, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Trial(Base):
    __tablename__ = "trials"
    __table_args__ = (UniqueConstraint("nct_id", name="uq_trials_nct_id"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nct_id: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    brief_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    official_title: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    phase: Mapped[str | None] = mapped_column(String(64), nullable=True)
    study_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    condition: Mapped[str | None] = mapped_column(String(512), nullable=True)
    intervention: Mapped[str | None] = mapped_column(Text, nullable=True)
    locations: Mapped[list | None] = mapped_column(JSON, nullable=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False, default="seed")
    eligibility_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    criteria: Mapped[list["TrialCriterion"]] = relationship(
        back_populates="trial", cascade="all, delete-orphan"
    )
    matching_results: Mapped[list["MatchingResult"]] = relationship(back_populates="trial")
