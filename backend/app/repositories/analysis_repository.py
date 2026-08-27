from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.analysis import Analysis, AnalysisStep
from app.models.matching import MatchingResult


class AnalysisRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, analysis_id: uuid.UUID) -> Analysis | None:
        stmt = (
            select(Analysis)
            .options(selectinload(Analysis.steps), selectinload(Analysis.patient))
            .where(Analysis.id == analysis_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def latest_for_patient(self, patient_id: uuid.UUID) -> Analysis | None:
        stmt = (
            select(Analysis)
            .options(selectinload(Analysis.steps), selectinload(Analysis.patient))
            .where(Analysis.patient_id == patient_id)
            .order_by(Analysis.created_at.desc())
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def next_sequence(self) -> int:
        count = self.db.execute(select(func.count()).select_from(Analysis)).scalar_one()
        return int(count) + 1

    def add(self, analysis: Analysis) -> Analysis:
        self.db.add(analysis)
        self.db.flush()
        return analysis

    def add_steps(self, steps: list[AnalysisStep]) -> None:
        for step in steps:
            self.db.add(step)
        self.db.flush()

    def get_step(self, analysis_id: uuid.UUID, step_name: str) -> AnalysisStep | None:
        stmt = select(AnalysisStep).where(
            AnalysisStep.analysis_id == analysis_id,
            AnalysisStep.step_name == step_name,
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def get_matching_results(self, analysis_id: uuid.UUID) -> list[MatchingResult]:
        stmt = (
            select(MatchingResult)
            .options(selectinload(MatchingResult.trial), selectinload(MatchingResult.evaluations))
            .where(MatchingResult.analysis_id == analysis_id)
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_matching_result_by_id(self, result_id: uuid.UUID) -> MatchingResult | None:
        stmt = (
            select(MatchingResult)
            .options(selectinload(MatchingResult.trial), selectinload(MatchingResult.evaluations))
            .where(MatchingResult.id == result_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()
