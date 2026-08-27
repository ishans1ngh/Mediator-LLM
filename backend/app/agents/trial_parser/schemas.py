from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class CriterionType(str, Enum):
    INCLUSION = "INCLUSION"
    EXCLUSION = "EXCLUSION"


class ParserStatus(str, Enum):
    STRUCTURED = "STRUCTURED"
    PARTIALLY_STRUCTURED = "PARTIALLY_STRUCTURED"
    UNSTRUCTURED = "UNSTRUCTURED"


class ParsedCriterion(BaseModel):
    criterion_type: CriterionType = Field(..., description="INCLUSION or EXCLUSION")
    criterion_text: str = Field(..., description="Original criterion text")
    structured_field: str | None = Field(None, description="Field name if structured (e.g., age, diagnosis)")
    operator: str | None = Field(None, description="Operator (e.g., >=, <=, CONTAINS)")
    value: Any = Field(None, description="Value for the criterion")
    unit: str | None = Field(None, description="Unit (e.g., years, ECOG)")
    normalized_value: Any = Field(None, description="Normalized value")
    source_text: str | None = Field(None, description="Excerpt from original text")
    parser_status: ParserStatus = Field(..., description="STRUCTURED, PARTIALLY_STRUCTURED, or UNSTRUCTURED")
    confidence: float | None = Field(None, ge=0, le=1, description="Extraction confidence")


class ParsedEligibility(BaseModel):
    trial_id: str = Field(..., description="Trial identifier")
    criteria: list[ParsedCriterion] = Field(default_factory=list, description="Parsed eligibility criteria")
    overall_status: str = Field(..., description="Overall parsing status (COMPLETED, FAILED)")
