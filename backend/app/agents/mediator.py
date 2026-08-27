from typing import Any

from app.agents.base import BaseAgent


class MediatorAgent(BaseAgent[dict[str, Any], dict[str, Any]]):
    """Deterministic mock evaluation. Replace `_run` with LLM reasoning later."""

    name = "mediator"

    async def evaluate(self, patient_attributes: dict[str, Any], criteria: dict[str, Any]) -> dict[str, Any]:
        payload = {"patient": patient_attributes, "criterion": criteria}
        return await self.run(payload)

    async def _run(self, payload: dict[str, Any]) -> dict[str, Any]:
        patient = payload.get("patient", {})
        criterion = payload.get("criterion", {})
        
        field = criterion.get("structured_field")
        operator = criterion.get("operator")
        required_value = criterion.get("value")
        criterion_text = criterion.get("criterion_text", "")
        
        patient_value = patient.get(field)
        
        if patient_value is None:
            return {
                "result": "UNKNOWN",
                "patient_evidence": f"No data available for {field}",
                "patient_value": str(patient_value) if patient_value is not None else None,
                "required_value": required_value,
                "explanation": f"Patient data missing for {field}.",
            }
        
        result = "UNKNOWN"
        explanation = ""
        
        if field == "age":
            try:
                age_val = int(patient_value)
                req_val = int(required_value) if required_value else 0
                if operator == ">=":
                    result = "PASS" if age_val >= req_val else "FAIL"
                    explanation = f"Patient age {age_val} {'satisfies' if result == 'PASS' else 'does not satisfy'} requirement {operator}{req_val}."
                elif operator == "<=":
                    result = "PASS" if age_val <= req_val else "FAIL"
                    explanation = f"Patient age {age_val} {'satisfies' if result == 'PASS' else 'does not satisfy'} requirement {operator}{req_val}."
            except (ValueError, TypeError):
                result = "UNKNOWN"
                explanation = f"Unable to parse age value: {patient_value}"
        
        elif field == "diagnosis":
            diagnosis_str = str(patient_value).lower()
            req_str = str(required_value).lower()
            if operator == "==":
                result = "PASS" if req_str in diagnosis_str else "FAIL"
                explanation = f"Patient diagnosis '{patient_value}' {'matches' if result == 'PASS' else 'does not match'} required '{required_value}'."
        
        elif field == "performance_status":
            ps_str = str(patient_value).lower()
            if operator == "in":
                allowed = [v.strip().lower() for v in str(required_value).split(",")]
                result = "PASS" if any(a in ps_str for a in allowed) else "FAIL"
                explanation = f"Patient performance status '{patient_value}' {'is within' if result == 'PASS' else 'is not within'} allowed range {required_value}."
        
        elif field == "previous_treatments":
            treatments = patient.get("previous_treatments", [])
            if operator == "not_contains":
                result = "FAIL" if any(req_val.lower() in str(t).lower() for t in treatments) else "PASS"
                explanation = f"Patient treatment history {'conflicts' if result == 'FAIL' else 'does not conflict'} with exclusion criterion."
        
        else:
            result = "UNKNOWN"
            explanation = f"Unable to evaluate field {field} with operator {operator}."
        
        return {
            "result": result,
            "patient_evidence": f"{field} = {patient_value}",
            "patient_value": str(patient_value),
            "required_value": str(required_value) if required_value else None,
            "explanation": explanation,
        }
