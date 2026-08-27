from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.ai.client import LLMClient
from app.ai.mock_client import MockLLMClient
from app.agents.trial_parser.agent import TrialParserAgent
from app.agents.trial_parser.schemas import ParsedCriterion, ParsedEligibility
from app.core.config import settings
from app.core.logging import get_logger
from app.models.criteria import TrialCriterion
from app.models.trial import Trial
from app.repositories.trial_repository import TrialRepository

logger = get_logger(__name__)


class TrialParserService:
    def __init__(self, db: Session, llm_client: LLMClient | None = None):
        self.db = db
        self.repo = TrialRepository(db)
        
        # Use MockLLMClient if no client provided or configured
        if llm_client is None:
            llm_client = MockLLMClient(
                model=getattr(settings, 'llm_model', 'mock-model'),
                temperature=getattr(settings, 'llm_temperature', 0),
                max_tokens=getattr(settings, 'llm_max_tokens', 4000),
                timeout=getattr(settings, 'http_timeout_seconds', 30),
            )
        
        self.agent = TrialParserAgent(llm_client)
        self.agent_version = "trial-parser-v1"

    async def parse_trial_eligibility(self, trial_id: uuid.UUID) -> ParsedEligibility:
        """
        Parse trial eligibility criteria using Trial Parser Agent.

        Args:
            trial_id: Trial UUID

        Returns:
            ParsedEligibility with structured criteria
        """
        trial = self.repo.get_by_id(trial_id)
        if not trial:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("TRIAL_NOT_FOUND", "Trial does not exist.")

        # Build trial data payload for the agent
        trial_data = {
            "trial_id": str(trial.id),
            "title": trial.title,
            "official_title": trial.official_title,
            "conditions": trial.conditions,
            "eligibility_text": trial.eligibility_text,
        }

        # Run the agent
        eligibility = await self.agent.run(trial_data)

        # Store parsed criteria in database
        self._store_criteria(trial_id, eligibility)

        logger.info(
            "trial_eligibility_parsed_and_stored",
            extra={
                "trial_id": str(trial_id),
                "criterion_count": len(eligibility.criteria),
                "agent_version": self.agent_version,
            },
        )

        return eligibility

    def _store_criteria(self, trial_id: uuid.UUID, eligibility: ParsedEligibility) -> None:
        """
        Store parsed trial criteria in database.

        Args:
            trial_id: Trial UUID
            eligibility: Parsed eligibility criteria
        """
        # Delete existing AI-generated criteria
        self.db.query(TrialCriterion).filter(
            TrialCriterion.trial_id == trial_id,
            TrialCriterion.agent_version.isnot(None)
        ).delete()

        # Insert new criteria
        for criterion in eligibility.criteria:
            # Convert value to string for storage (can be dict, list, etc.)
            value_str = str(criterion.value) if criterion.value is not None else None
            normalized_value_str = str(criterion.normalized_value) if criterion.normalized_value is not None else None

            db_criterion = TrialCriterion(
                trial_id=trial_id,
                criterion_type=criterion.criterion_type.value,
                criterion_text=criterion.criterion_text,
                structured_field=criterion.structured_field,
                operator=criterion.operator,
                value=value_str,
                unit=criterion.unit,
                normalized_value=normalized_value_str,
                source_text=criterion.source_text,
                parser_status=criterion.parser_status.value,
                parser_version=self.agent_version,
                confidence=criterion.confidence,
                agent_version=self.agent_version,
                prompt_version=self.agent.prompt_version,
                model_name=self.agent.llm_client.model,
            )
            self.db.add(db_criterion)

        self.db.flush()

    def get_trial_criteria(self, trial_id: uuid.UUID) -> list[TrialCriterion]:
        """
        Get stored trial criteria.

        Args:
            trial_id: Trial UUID

        Returns:
            List of trial criteria
        """
        trial = self.repo.get_by_id(trial_id)
        if not trial:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("TRIAL_NOT_FOUND", "Trial does not exist.")

        return trial.criteria
