from typing import Any

from app.agents.base import BaseAgent


class PatientReaderAgent(BaseAgent[dict[str, Any], dict[str, Any]]):
    """Deterministic mock extraction. Replace `_run` with LLM reasoning later."""

    name = "patient_reader"

    async def extract_attributes(self, patient: dict[str, Any]) -> dict[str, Any]:
        return await self.run(patient)

    async def _run(self, patient: dict[str, Any]) -> dict[str, Any]:
        treatments = [t.get("treatment_name") for t in patient.get("treatments", []) if t.get("treatment_name")]
        labs = {
            lab.get("test_name"): {"value": lab.get("value"), "unit": lab.get("unit")}
            for lab in patient.get("labs", [])
        }
        return {
            "age": patient.get("age"),
            "diagnosis": patient.get("diagnosis"),
            "disease_stage": patient.get("disease_stage"),
            "performance_status": patient.get("performance_status"),
            "gender": patient.get("gender"),
            "previous_treatments": treatments,
            "labs": labs,
            "clinical_notes": patient.get("clinical_notes"),
            "medical_history": patient.get("medical_history"),
        }
