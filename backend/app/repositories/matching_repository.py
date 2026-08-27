from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.matching import CriterionEvaluation, MatchingResult


class MatchingRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_result(self, result: MatchingResult) -> MatchingResult:
        self.db.add(result)
        self.db.flush()
        return result

    def add_evaluation(self, evaluation: CriterionEvaluation) -> CriterionEvaluation:
        self.db.add(evaluation)
        self.db.flush()
        return evaluation

    def list_for_analysis(self, analysis_id: uuid.UUID) -> list[MatchingResult]:
        stmt = (
            select(MatchingResult)
            .options(
                selectinload(MatchingResult.trial),
                selectinload(MatchingResult.evaluations).selectinload(CriterionEvaluation.criterion),
            )
            .where(MatchingResult.analysis_id == analysis_id)
            .order_by(MatchingResult.match_score.desc())
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_by_id(self, matching_result_id: uuid.UUID) -> MatchingResult | None:
        stmt = (
            select(MatchingResult)
            .options(
                selectinload(MatchingResult.trial),
                selectinload(MatchingResult.evaluations).selectinload(CriterionEvaluation.criterion),
            )
            .where(MatchingResult.id == matching_result_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def summary_counts(self) -> dict:
        total_analyses = self.db.execute(select(func.count()).select_from(MatchingResult)).scalar_one()
        return {"matching_rows": int(total_analyses)}
