from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AttributeStatus(str, Enum):
    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"


class PatientAttribute(BaseModel):
    field: str = Field(..., description="Name of the attribute (e.g., age, sex, diagnosis)")
    value: Any = Field(None, description="Raw extracted value")
    normalized_value: Any = Field(None, description="Normalized value (e.g., MALE for male)")
    unit: str | None = Field(None, description="Unit of measurement (e.g., years, ECOG)")
    source: str | None = Field(None, description="Source of the information (e.g., patient_record, clinical_notes)")
    source_text: str | None = Field(None, description="Exact text excerpt from source")
    confidence: float | None = Field(None, ge=0, le=1, description="Extraction confidence")
    status: AttributeStatus = Field(..., description="Whether the attribute is KNOWN or UNKNOWN")


class PatientProfile(BaseModel):
    patient_id: str = Field(..., description="Patient identifier")
    attributes: list[PatientAttribute] = Field(default_factory=list, description="Extracted patient attributes")
    overall_status: str = Field(..., description="Overall extraction status (COMPLETED, FAILED)")
