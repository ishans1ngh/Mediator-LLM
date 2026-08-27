from __future__ import annotations

import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.criteria import TrialCriterion


class CriteriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_trial_id(self, trial_id: uuid.UUID) -> list[TrialCriterion]:
        stmt = select(TrialCriterion).where(TrialCriterion.trial_id == trial_id)
        return list(self.db.execute(stmt).scalars().all())

    def delete_by_trial_id(self, trial_id: uuid.UUID) -> None:
        stmt = delete(TrialCriterion).where(TrialCriterion.trial_id == trial_id)
        self.db.execute(stmt)

    def bulk_create(self, criteria: list[TrialCriterion]) -> list[TrialCriterion]:
        for criterion in criteria:
            self.db.add(criterion)
        self.db.flush()
        return criteria

    def create(self, criterion: TrialCriterion) -> TrialCriterion:
        self.db.add(criterion)
        self.db.flush()
        return criterion
