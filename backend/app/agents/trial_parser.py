from typing import Any

from app.agents.base import BaseAgent


class TrialParserAgent(BaseAgent[dict[str, Any], list[dict[str, Any]]]):
    """Deterministic mock criteria extraction. Replace `_run` with LLM reasoning later."""

    name = "trial_parser"

    async def parse(self, trial: dict[str, Any]) -> list[dict[str, Any]]:
        return await self.run(trial)

    async def _run(self, trial: dict[str, Any]) -> list[dict[str, Any]]:
        eligibility_text = trial.get("eligibility_text", "")
        criteria = []
        
        if "age" in eligibility_text.lower() or "18" in eligibility_text:
            criteria.append({
                "criterion_type": "INCLUSION",
                "criterion_text": "Age ≥ 18 years",
                "structured_field": "age",
                "operator": ">=",
                "value": "18",
                "unit": "years",
            })
        
        if "glioblastoma" in eligibility_text.lower() or "gbm" in eligibility_text.lower():
            criteria.append({
                "criterion_type": "INCLUSION",
                "criterion_text": "Histologically confirmed glioblastoma",
                "structured_field": "diagnosis",
                "operator": "==",
                "value": "Glioblastoma",
                "unit": None,
            })
        
        if "ecog" in eligibility_text.lower():
            criteria.append({
                "criterion_type": "INCLUSION",
                "criterion_text": "ECOG performance status 0-2",
                "structured_field": "performance_status",
                "operator": "in",
                "value": "ECOG 0, ECOG 1, ECOG 2",
                "unit": None,
            })
        
        if "pregnant" in eligibility_text.lower():
            criteria.append({
                "criterion_type": "EXCLUSION",
                "criterion_text": "Pregnant or breastfeeding",
                "structured_field": "pregnancy_status",
                "operator": "==",
                "value": "Not pregnant",
                "unit": None,
            })
        
        if "prior" in eligibility_text.lower() and "therapy" in eligibility_text.lower():
            criteria.append({
                "criterion_type": "EXCLUSION",
                "criterion_text": "Prior therapy with similar agent",
                "structured_field": "previous_treatments",
                "operator": "not_contains",
                "value": "similar_agent",
                "unit": None,
            })
        
        return criteria
