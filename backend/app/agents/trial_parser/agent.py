from __future__ import annotations

from app.ai.client import LLMClient
from app.agents.base import BaseAgent
from app.agents.trial_parser.prompts import TRIAL_PARSER_PROMPT_VERSION, TRIAL_PARSER_SYSTEM_PROMPT
from app.agents.trial_parser.schemas import ParsedEligibility
from app.core.logging import get_logger

logger = get_logger(__name__)


class TrialParserAgent(BaseAgent[dict, ParsedEligibility]):
    name = "trial_parser"

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.prompt_version = TRIAL_PARSER_PROMPT_VERSION

    async def _run(self, payload: dict) -> ParsedEligibility:
        """
        Parse trial eligibility criteria into structured format.

        Args:
            payload: Dictionary containing trial information

        Returns:
            ParsedEligibility with structured criteria
        """
        trial_id = payload.get("trial_id", "unknown")
        
        # Build user prompt from trial data
        user_prompt = self._build_user_prompt(payload)
        
        try:
            eligibility = await self.llm_client.generate_structured(
                system_prompt=TRIAL_PARSER_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_schema=ParsedEligibility,
            )
            eligibility.trial_id = trial_id
            logger.info(
                "trial_eligibility_parsed",
                extra={
                    "trial_id": trial_id,
                    "criterion_count": len(eligibility.criteria),
                    "prompt_version": self.prompt_version,
                },
            )
            return eligibility
        except Exception as exc:
            logger.exception("trial_parser_failed", extra={"trial_id": trial_id})
            raise

    def _build_user_prompt(self, trial_data: dict) -> str:
        """Build user prompt from trial data."""
        prompt_parts = []
        
        if "title" in trial_data:
            prompt_parts.append(f"Trial Title: {trial_data['title']}")
        
        if "official_title" in trial_data:
            prompt_parts.append(f"Official Title: {trial_data['official_title']}")
        
        if "conditions" in trial_data and trial_data["conditions"]:
            conditions = ", ".join(trial_data["conditions"]) if isinstance(trial_data["conditions"], list) else trial_data["conditions"]
            prompt_parts.append(f"Conditions: {conditions}")
        
        if "eligibility_text" in trial_data:
            prompt_parts.append("Eligibility Criteria:")
            prompt_parts.append(trial_data["eligibility_text"])
        
        return "\n\n".join(prompt_parts)
