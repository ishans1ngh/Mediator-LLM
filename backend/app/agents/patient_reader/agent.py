from __future__ import annotations

from typing import Any

from app.ai.client import LLMClient
from app.agents.base import BaseAgent
from app.agents.patient_reader.prompts import PATIENT_READER_PROMPT_VERSION, PATIENT_READER_SYSTEM_PROMPT
from app.agents.patient_reader.schemas import PatientProfile
from app.core.logging import get_logger

logger = get_logger(__name__)


class PatientReaderAgent(BaseAgent[dict, PatientProfile]):
    name = "patient_reader"

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.prompt_version = PATIENT_READER_PROMPT_VERSION

    async def _run(self, payload: dict) -> PatientProfile:
        """
        Extract structured patient attributes from patient data.

        Args:
            payload: Dictionary containing patient information

        Returns:
            PatientProfile with extracted attributes
        """
        patient_id = payload.get("patient_id", "unknown")
        
        # Build user prompt from patient data
        user_prompt = self._build_user_prompt(payload)
        
        try:
            profile = await self.llm_client.generate_structured(
                system_prompt=PATIENT_READER_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_schema=PatientProfile,
            )
            profile.patient_id = patient_id
            logger.info(
                "patient_profile_extracted",
                extra={
                    "patient_id": patient_id,
                    "attribute_count": len(profile.attributes),
                    "prompt_version": self.prompt_version,
                },
            )
            return profile
        except Exception as exc:
            logger.exception("patient_reader_failed", extra={"patient_id": patient_id})
            raise

    def _build_user_prompt(self, patient_data: dict) -> str:
        """Build user prompt from patient data."""
        prompt_parts = []
        
        if "patient_code" in patient_data:
            prompt_parts.append(f"Patient Code: {patient_data['patient_code']}")
        
        if "age" in patient_data:
            prompt_parts.append(f"Age: {patient_data['age']}")
        
        if "gender" in patient_data:
            prompt_parts.append(f"Sex: {patient_data['gender']}")
        
        if "diagnosis" in patient_data:
            prompt_parts.append(f"Diagnosis: {patient_data['diagnosis']}")
        
        if "disease_stage" in patient_data:
            prompt_parts.append(f"Disease Stage: {patient_data['disease_stage']}")
        
        if "clinical_notes" in patient_data:
            prompt_parts.append(f"Clinical Notes: {patient_data['clinical_notes']}")
        
        if "medical_history" in patient_data:
            prompt_parts.append(f"Medical History: {patient_data['medical_history']}")
        
        if "performance_status" in patient_data:
            prompt_parts.append(f"Performance Status: {patient_data['performance_status']}")
        
        if "labs" in patient_data and patient_data["labs"]:
            prompt_parts.append("Lab Results:")
            for lab in patient_data["labs"]:
                prompt_parts.append(f"  - {lab.get('test_name')}: {lab.get('value')} {lab.get('unit', '')}")
        
        if "treatments" in patient_data and patient_data["treatments"]:
            prompt_parts.append("Treatments:")
            for treatment in patient_data["treatments"]:
                prompt_parts.append(f"  - {treatment.get('treatment_name')}: {treatment.get('status')}")
        
        return "\n".join(prompt_parts)
