from uuid import UUID

from pydantic import BaseModel, ConfigDict


class StructuredCriterion(BaseModel):
    criterion_type: str
    criterion_text: str
    structured_field: str | None = None
    operator: str | None = None
    value: str | None = None
    unit: str | None = None
    parser_status: str = "UNSTRUCTURED"
    parser_version: str = "v1-deterministic"
    confidence: float | None = None


class TrialCriterionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    criterion_type: str
    criterion_text: str
    structured_field: str | None = None
    operator: str | None = None
    value: str | None = None
    unit: str | None = None
    parser_status: str
    parser_version: str
    confidence: float | None = None


class CriteriaResponse(BaseModel):
    trial_id: str
    inclusion: list[TrialCriterionOut]
    exclusion: list[TrialCriterionOut]


class CriteriaParseResponse(BaseModel):
    trial_id: str
    total_criteria: int
    structured: int
    unstructured: int
    criteria: list[TrialCriterionOut]
