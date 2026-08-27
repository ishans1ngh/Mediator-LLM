from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models.criteria import TrialCriterion
from app.parsers.eligibility_parser import DeterministicEligibilityParser, EligibilityParser, StructuredCriterion
from app.repositories.criteria_repository import CriteriaRepository
from app.core.logging import get_logger

logger = get_logger(__name__)


class CriteriaService:
    def __init__(self, db: Session, parser: EligibilityParser | None = None):
        self.db = db
        self.repo = CriteriaRepository(db)
        self.parser = parser or DeterministicEligibilityParser()

    async def parse_trial_criteria(self, trial_id: uuid.UUID, eligibility_text: str) -> list[TrialCriterion]:
        structured_criteria = await self.parser.parse(eligibility_text)
        
        self.repo.delete_by_trial_id(trial_id)
        
        trial_criteria = []
        for criterion in structured_criteria:
            trial_criterion = TrialCriterion(
                trial_id=trial_id,
                criterion_type=criterion.criterion_type,
                criterion_text=criterion.criterion_text,
                structured_field=criterion.structured_field,
                operator=criterion.operator,
                value=criterion.value,
                unit=criterion.unit,
                parser_status=criterion.parser_status,
                parser_version=criterion.parser_version,
                confidence=criterion.confidence,
            )
            trial_criteria.append(trial_criterion)
        
        self.repo.bulk_create(trial_criteria)
        
        logger.info(
            "trial_criteria_parsed",
            extra={
                "trial_id": str(trial_id),
                "total_criteria": len(trial_criteria),
                "structured": sum(1 for c in trial_criteria if c.parser_status == "STRUCTURED"),
                "unstructured": sum(1 for c in trial_criteria if c.parser_status == "UNSTRUCTURED"),
            },
        )
        
        return trial_criteria

    def get_trial_criteria(self, trial_id: uuid.UUID) -> list[TrialCriterion]:
        return self.repo.get_by_trial_id(trial_id)
