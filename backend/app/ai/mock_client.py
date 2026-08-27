from __future__ import annotations

import json
from typing import Any, Type

from app.ai.client import LLMClient
from app.ai.exceptions import StructuredOutputError


class MockLLMClient(LLMClient):
    """Mock LLM client for development and testing."""

    def __init__(
        self,
        model: str = "mock-model",
        temperature: float = 0,
        max_tokens: int = 4000,
        timeout: int = 30,
    ):
        super().__init__(model, temperature, max_tokens, timeout)

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Type,
    ) -> Any:
        """
        Generate deterministic mock structured output based on input content.
        """
        from app.agents.patient_reader.schemas import PatientProfile, PatientAttribute
        from app.agents.trial_parser.schemas import ParsedEligibility, ParsedCriterion

        # Check if this is a patient reader request
        if "patient" in system_prompt.lower() and "extract" in system_prompt.lower():
            return self._mock_patient_profile(user_prompt)
        
        # Check if this is a trial parser request
        if "trial" in system_prompt.lower() and "eligibility" in system_prompt.lower():
            return self._mock_trial_eligibility(user_prompt)

        # Fallback: try to create a minimal valid instance
        try:
            return response_schema()
        except Exception as e:
            raise StructuredOutputError(f"Cannot create mock instance of {response_schema.__name__}: {e}")

    def _mock_patient_profile(self, user_prompt: str) -> Any:
        """Generate mock patient profile based on input."""
        from app.agents.patient_reader.schemas import PatientProfile, PatientAttribute

        attributes = []
        prompt_lower = user_prompt.lower()

        # Age extraction
        if "age" in prompt_lower:
            import re
            age_match = re.search(r"age[:\s]*(\d+)", prompt_lower)
            if age_match:
                age = int(age_match.group(1))
                attributes.append(
                    PatientAttribute(
                        field="age",
                        value=age,
                        normalized_value=age,
                        unit="years",
                        source="patient_record",
                        source_text=f"Age: {age}",
                        confidence=1.0,
                        status="KNOWN",
                    )
                )

        # Sex extraction
        if "male" in prompt_lower:
            attributes.append(
                PatientAttribute(
                    field="sex",
                    value="Male",
                    normalized_value="MALE",
                    unit=None,
                    source="patient_record",
                    source_text="Male",
                    confidence=1.0,
                    status="KNOWN",
                )
            )
        elif "female" in prompt_lower:
            attributes.append(
                PatientAttribute(
                    field="sex",
                    value="Female",
                    normalized_value="FEMALE",
                    unit=None,
                    source="patient_record",
                    source_text="Female",
                    confidence=1.0,
                    status="KNOWN",
                )
            )

        # Diagnosis extraction
        if "glioblastoma" in prompt_lower:
            attributes.append(
                PatientAttribute(
                    field="diagnosis",
                    value="Glioblastoma",
                    normalized_value="Glioblastoma",
                    unit=None,
                    source="patient_record",
                    source_text="Diagnosis: Glioblastoma",
                    confidence=1.0,
                    status="KNOWN",
                )
            )
        elif "diagnosis" in prompt_lower:
            import re
            diag_match = re.search(r"diagnosis[:\s]*([^\n,]+)", prompt_lower)
            if diag_match:
                diagnosis = diag_match.group(1).strip()
                attributes.append(
                    PatientAttribute(
                        field="diagnosis",
                        value=diagnosis,
                        normalized_value=diagnosis,
                        unit=None,
                        source="patient_record",
                        source_text=f"Diagnosis: {diagnosis}",
                        confidence=1.0,
                        status="KNOWN",
                    )
                )

        # Performance status
        if "ecog" in prompt_lower:
            import re
            ecog_match = re.search(r"ecog[:\s]*(\d)", prompt_lower)
            if ecog_match:
                ecog = int(ecog_match.group(1))
                attributes.append(
                    PatientAttribute(
                        field="performance_status",
                        value=f"ECOG {ecog}",
                        normalized_value=ecog,
                        unit="ECOG",
                        source="patient_record",
                        source_text=f"ECOG {ecog}",
                        confidence=1.0,
                        status="KNOWN",
                    )
                )

        # Biomarkers - explicitly mark as UNKNOWN if not present
        if "mgmt" not in prompt_lower:
            attributes.append(
                PatientAttribute(
                    field="MGMT_status",
                    value=None,
                    normalized_value=None,
                    unit=None,
                    source=None,
                    source_text=None,
                    confidence=None,
                    status="UNKNOWN",
                )
            )
        if "idh" not in prompt_lower:
            attributes.append(
                PatientAttribute(
                    field="IDH_status",
                    value=None,
                    normalized_value=None,
                    unit=None,
                    source=None,
                    source_text=None,
                    confidence=None,
                    status="UNKNOWN",
                )
            )

        return PatientProfile(
            patient_id="mock-patient-id",
            attributes=attributes,
            overall_status="COMPLETED",
        )

    def _mock_trial_eligibility(self, user_prompt: str) -> Any:
        """Generate mock trial eligibility based on input."""
        from app.agents.trial_parser.schemas import ParsedEligibility, ParsedCriterion

        criteria = []
        prompt_lower = user_prompt.lower()

        # Age criteria
        if "age" in prompt_lower:
            import re
            age_match = re.search(r"age\s*([>=<]+)\s*(\d+)", prompt_lower)
            if age_match:
                operator = age_match.group(1)
                value = int(age_match.group(2))
                criteria.append(
                    ParsedCriterion(
                        criterion_type="INCLUSION",
                        criterion_text=f"Age {operator} {value} years.",
                        structured_field="age",
                        operator=operator,
                        value=value,
                        unit="years",
                        normalized_value=value,
                        source_text=f"Age {operator} {value}",
                        parser_status="STRUCTURED",
                        confidence=0.99,
                    )
                )

        # ECOG criteria
        if "ecog" in prompt_lower:
            import re
            ecog_match = re.search(r"ecog\s*([0-2])[-\s]*([0-2])?", prompt_lower)
            if ecog_match:
                ecog_min = int(ecog_match.group(1))
                ecog_max = int(ecog_match.group(2)) if ecog_match.group(2) else ecog_min
                criteria.append(
                    ParsedCriterion(
                        criterion_type="INCLUSION",
                        criterion_text=f"ECOG performance status {ecog_min}-{ecog_max}.",
                        structured_field="performance_status",
                        operator="BETWEEN",
                        value={"min": ecog_min, "max": ecog_max},
                        unit="ECOG",
                        normalized_value=f"{ecog_min}-{ecog_max}",
                        source_text=f"ECOG {ecog_min}-{ecog_max}",
                        parser_status="STRUCTURED",
                        confidence=0.90,
                    )
                )

        # Diagnosis criteria
        if "glioblastoma" in prompt_lower:
            criteria.append(
                ParsedCriterion(
                    criterion_type="INCLUSION",
                    criterion_text="Histologically confirmed glioblastoma.",
                    structured_field="diagnosis",
                    operator="CONTAINS",
                    value="glioblastoma",
                    unit=None,
                    normalized_value="glioblastoma",
                    source_text="glioblastoma",
                    parser_status="STRUCTURED",
                    confidence=0.95,
                )
            )

        # Unstructured criteria
        if "adequate organ function" in prompt_lower:
            criteria.append(
                ParsedCriterion(
                    criterion_type="INCLUSION",
                    criterion_text="Adequate organ function as determined by the investigator.",
                    structured_field=None,
                    operator=None,
                    value=None,
                    unit=None,
                    normalized_value=None,
                    source_text="Adequate organ function as determined by the investigator.",
                    parser_status="UNSTRUCTURED",
                    confidence=None,
                )
            )

        return ParsedEligibility(
            trial_id="mock-trial-id",
            criteria=criteria,
            overall_status="COMPLETED",
        )
