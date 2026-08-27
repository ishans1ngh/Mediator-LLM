from __future__ import annotations

import httpx

from app.core.config import settings
from app.core.exceptions import AppError
from app.core.logging import get_logger

logger = get_logger(__name__)


class ClinicalTrialsService:
    def __init__(self):
        self.base_url = settings.clinicaltrials_api_url
        self.timeout = settings.http_timeout_seconds

    async def search_trials(self, condition: str, max_results: int = 20) -> list[dict]:
        params = {
            "query.term": condition,
            "pageSize": max_results,
            "fields": "NCTId,OfficialTitle,BriefTitle,BriefSummary,Phase,StudyType,OverallStatus,Condition,InterventionName,Location,EligibilityModule",
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/studies", params=params)
                response.raise_for_status()
                data = response.json()
                return self._normalize_trials(data)
        except httpx.TimeoutException:
            logger.error("clinicaltrials_timeout", extra={"condition": condition})
            raise AppError("CLINICALTRIALS_TIMEOUT", "ClinicalTrials.gov API timed out.")
        except httpx.HTTPStatusError as e:
            logger.error("clinicaltrials_http_error", extra={"status": e.response.status_code})
            raise AppError("CLINICALTRIALS_ERROR", f"External API error: {e.response.status_code}")
        except Exception as e:
            logger.exception("clinicaltrials_error")
            raise AppError("CLINICALTRIALS_ERROR", "Failed to fetch trials from ClinicalTrials.gov.")

    def _normalize_trials(self, data: dict) -> list[dict]:
        normalized = []
        studies = data.get("studies", [])
        
        for study in studies:
            protocol = study.get("protocolSection", {})
            identification = protocol.get("identificationModule", {})
            status_module = protocol.get("statusModule", {})
            design = protocol.get("designModule", {})
            arms_interventions = protocol.get("armsInterventionsModule", {})
            contacts_locations = protocol.get("contactsLocationsModule", {})
            eligibility = protocol.get("eligibilityModule", {})
            
            nct_id = identification.get("nctId")
            title = identification.get("briefTitle") or identification.get("officialTitle", "")
            brief_summary = protocol.get("descriptionModule", {}).get("briefSummary", {}).get("textblock", "")
            official_title = identification.get("officialTitle")
            
            phases = []
            if "phases" in design:
                phases = [p for p in design["phases"] if p]
            
            conditions = []
            if "conditionsModule" in protocol:
                conditions = protocol["conditionsModule"].get("conditions", [])
                conditions = [c.get("name") if isinstance(c, dict) else c for c in conditions]
            
            interventions = []
            if "armsInterventionsModule" in protocol:
                for arm in arms_interventions.get("arms", []):
                    for intervention in arm.get("interventions", []):
                        name = intervention.get("name") or intervention.get("type", "")
                        if name:
                            interventions.append(name)
            
            locations = []
            if "locationsModule" in contacts_locations:
                for loc in contacts_locations["locationsModule"].get("locations", []):
                    loc_dict = loc.get("location", {})
                    city = loc_dict.get("city", "")
                    state = loc_dict.get("state", "")
                    country = loc_dict.get("country", "")
                    if city or state or country:
                        locations.append(f"{city}, {state}, {country}".strip(", "))
            
            eligibility_text = ""
            if "eligibilityModule" in eligibility:
                eligibility_text = eligibility["eligibilityModule"].get("eligibilityCriteria", "")
            
            normalized.append({
                "nct_id": nct_id,
                "title": title,
                "brief_summary": brief_summary,
                "official_title": official_title,
                "phase": ", ".join(phases) if phases else None,
                "study_type": design.get("studyType"),
                "status": status_module.get("overallStatus"),
                "condition": ", ".join(conditions) if conditions else None,
                "intervention": ", ".join(interventions) if interventions else None,
                "locations": locations,
                "eligibility_text": eligibility_text,
            })
        
        return normalized
