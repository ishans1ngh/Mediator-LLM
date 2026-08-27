from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.criteria import TrialCriterion
from app.models.trial import Trial
from app.repositories.trial_repository import TrialRepository
from app.services.clinicaltrials_service import ClinicalTrialsService


class TrialService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TrialRepository(db)
        self.ct_service = ClinicalTrialsService()

    async def search_trials(
        self,
        search: str | None = None,
        condition: str | None = None,
        phase: str | None = None,
        status: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Trial], int]:
        return self.repo.list(
            search=search,
            condition=condition,
            phase=phase,
            status=status,
            page=page,
            page_size=page_size,
        )

    def get_trial(self, trial_id: uuid.UUID) -> Trial:
        trial = self.repo.get_by_id(trial_id)
        if not trial:
            raise NotFoundError("TRIAL_NOT_FOUND", "Trial does not exist.")
        return trial

    def get_trial_by_nct(self, nct_id: str) -> Trial:
        trial = self.repo.get_by_nct_id(nct_id)
        if not trial:
            raise NotFoundError("TRIAL_NOT_FOUND", "Trial does not exist.")
        return trial

    async def sync_trials(self, condition: str, max_results: int = 20) -> dict:
        external_trials = await self.ct_service.search_trials(condition, max_results)
        
        created = 0
        updated = 0
        
        for trial_data in external_trials:
            existing = self.repo.get_by_nct_id(trial_data["nct_id"])
            
            if existing:
                existing.title = trial_data["title"]
                existing.brief_summary = trial_data["brief_summary"]
                existing.official_title = trial_data["official_title"]
                existing.phases = trial_data["phases"]
                existing.study_type = trial_data["study_type"]
                existing.status = trial_data["status"]
                existing.conditions = trial_data["conditions"]
                existing.intervention = ", ".join(trial_data["interventions"]) if trial_data["interventions"] else None
                existing.locations = trial_data["locations"]
                existing.eligibility_text = trial_data["eligibility_text"]
                existing.last_updated = datetime.now(timezone.utc)
                existing.source = "clinicaltrials.gov"
                updated += 1
            else:
                trial = Trial(
                    nct_id=trial_data["nct_id"],
                    title=trial_data["title"],
                    brief_summary=trial_data["brief_summary"],
                    official_title=trial_data["official_title"],
                    phases=trial_data["phases"],
                    study_type=trial_data["study_type"],
                    status=trial_data["status"],
                    conditions=trial_data["conditions"],
                    intervention=", ".join(trial_data["interventions"]) if trial_data["interventions"] else None,
                    locations=trial_data["locations"],
                    eligibility_text=trial_data["eligibility_text"],
                    source="clinicaltrials.gov",
                    last_updated=datetime.now(timezone.utc),
                )
                self.db.add(trial)
                created += 1
        
        self.db.flush()
        return {"condition": condition, "retrieved": len(external_trials), "created": created, "updated": updated}
