from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.ai.client import LLMClient
from app.ai.mock_client import MockLLMClient
from app.agents.patient_reader.agent import PatientReaderAgent
from app.agents.patient_reader.schemas import PatientAttribute, PatientProfile
from app.core.config import settings
from app.core.logging import get_logger
from app.models.patient import Patient, PatientProfileAttribute
from app.repositories.patient_repository import PatientRepository

logger = get_logger(__name__)


class PatientReaderService:
    def __init__(self, db: Session, llm_client: LLMClient | None = None):
        self.db = db
        self.repo = PatientRepository(db)
        
        # Use MockLLMClient if no client provided or configured
        if llm_client is None:
            llm_client = MockLLMClient(
                model=getattr(settings, 'llm_model', 'mock-model'),
                temperature=getattr(settings, 'llm_temperature', 0),
                max_tokens=getattr(settings, 'llm_max_tokens', 4000),
                timeout=getattr(settings, 'http_timeout_seconds', 30),
            )
        
        self.agent = PatientReaderAgent(llm_client)
        self.agent_version = "patient-reader-v1"

    async def extract_patient_profile(self, patient_id: uuid.UUID) -> PatientProfile:
        """
        Extract structured patient attributes using Patient Reader Agent.

        Args:
            patient_id: Patient UUID

        Returns:
            PatientProfile with extracted attributes
        """
        patient = self.repo.get_by_id(patient_id)
        if not patient:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("PATIENT_NOT_FOUND", "Patient does not exist.")

        # Build patient data payload for the agent
        patient_data = {
            "patient_id": str(patient.id),
            "patient_code": patient.patient_code,
            "age": patient.age,
            "gender": patient.gender,
            "diagnosis": patient.diagnosis,
            "disease_stage": patient.disease_stage,
            "clinical_notes": patient.clinical_notes,
            "medical_history": patient.medical_history,
            "performance_status": patient.performance_status,
            "labs": [
                {"test_name": lab.test_name, "value": lab.value, "unit": lab.unit}
                for lab in patient.labs
            ],
            "treatments": [
                {"treatment_name": t.treatment_name, "status": t.status}
                for t in patient.treatments
            ],
        }

        # Run the agent
        profile = await self.agent.run(patient_data)

        # Store extracted attributes in database
        self._store_attributes(patient_id, profile)

        logger.info(
            "patient_profile_extracted_and_stored",
            extra={
                "patient_id": str(patient_id),
                "attribute_count": len(profile.attributes),
                "agent_version": self.agent_version,
            },
        )

        return profile

    def _store_attributes(self, patient_id: uuid.UUID, profile: PatientProfile) -> None:
        """
        Store extracted patient attributes in database.

        Args:
            patient_id: Patient UUID
            profile: Extracted patient profile
        """
        # Delete existing AI-generated attributes
        self.db.query(PatientProfileAttribute).filter(
            PatientProfileAttribute.patient_id == patient_id,
            PatientProfileAttribute.agent_version.isnot(None)
        ).delete()

        # Insert new attributes
        for attr in profile.attributes:
            db_attr = PatientProfileAttribute(
                patient_id=patient_id,
                attribute_name=attr.field,
                attribute_value=str(attr.value) if attr.value is not None else None,
                normalized_value=str(attr.normalized_value) if attr.normalized_value is not None else None,
                unit=attr.unit,
                source=attr.source,
                source_text=attr.source_text,
                status=attr.status.value,
                confidence=attr.confidence,
                agent_version=self.agent_version,
                prompt_version=self.agent.prompt_version,
                model_name=self.agent.llm_client.model,
            )
            self.db.add(db_attr)

        self.db.flush()

    def get_patient_profile(self, patient_id: uuid.UUID) -> list[PatientProfileAttribute]:
        """
        Get stored patient profile attributes.

        Args:
            patient_id: Patient UUID

        Returns:
            List of patient profile attributes
        """
        patient = self.repo.get_by_id(patient_id)
        if not patient:
            from app.core.exceptions import NotFoundError
            raise NotFoundError("PATIENT_NOT_FOUND", "Patient does not exist.")

        return patient.profile_attributes
