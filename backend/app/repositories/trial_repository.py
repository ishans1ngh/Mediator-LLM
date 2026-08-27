from __future__ import annotations

import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.criteria import TrialCriterion
from app.models.trial import Trial


class TrialRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, trial_id: uuid.UUID) -> Trial | None:
        return self.db.get(Trial, trial_id)

    def get_by_nct(self, nct_id: str) -> Trial | None:
        stmt = select(Trial).where(func.upper(Trial.nct_id) == nct_id.upper())
        return self.db.execute(stmt).scalar_one_or_none()

    def get_with_criteria(self, trial: Trial) -> Trial:
        stmt = select(Trial).options(selectinload(Trial.criteria)).where(Trial.id == trial.id)
        return self.db.execute(stmt).scalar_one()

    def list(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        condition: str | None = None,
        phase: str | None = None,
        status: str | None = None,
    ) -> tuple[list[Trial], int]:
        stmt = select(Trial)
        count_stmt = select(func.count()).select_from(Trial)
        if search:
            like = f"%{search}%"
            clause = or_(
                Trial.title.ilike(like),
                Trial.nct_id.ilike(like),
                Trial.condition.ilike(like),
                Trial.brief_summary.ilike(like),
            )
            stmt = stmt.where(clause)
            count_stmt = count_stmt.where(clause)
        if condition:
            stmt = stmt.where(Trial.condition.ilike(f"%{condition}%"))
            count_stmt = count_stmt.where(Trial.condition.ilike(f"%{condition}%"))
        if phase:
            stmt = stmt.where(Trial.phase.ilike(f"%{phase}%"))
            count_stmt = count_stmt.where(Trial.phase.ilike(f"%{phase}%"))
        if status:
            stmt = stmt.where(Trial.status.ilike(status))
            count_stmt = count_stmt.where(Trial.status.ilike(status))
        total = self.db.execute(count_stmt).scalar_one()
        rows = (
            self.db.execute(
                stmt.order_by(Trial.nct_id.asc()).offset((page - 1) * page_size).limit(page_size)
            )
            .scalars()
            .all()
        )
        return list(rows), int(total)

    def list_by_condition(self, condition: str, limit: int) -> list[Trial]:
        stmt = (
            select(Trial)
            .options(selectinload(Trial.criteria))
            .where(Trial.condition.ilike(f"%{condition}%"))
            .order_by(Trial.nct_id.asc())
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def add(self, trial: Trial) -> Trial:
        self.db.add(trial)
        self.db.flush()
        return trial

    def replace_criteria(self, trial: Trial, criteria: list[TrialCriterion]) -> None:
        for existing in list(trial.criteria):
            self.db.delete(existing)
        self.db.flush()
        for criterion in criteria:
            criterion.trial_id = trial.id
            self.db.add(criterion)
        self.db.flush()

    def add_criteria_if_empty(self, trial: Trial, criteria: list[TrialCriterion]) -> None:
        if trial.criteria:
            return
        for criterion in criteria:
            criterion.trial_id = trial.id
            self.db.add(criterion)
        self.db.flush()
