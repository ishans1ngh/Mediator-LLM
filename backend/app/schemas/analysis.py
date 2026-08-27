from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AnalysisCreate(BaseModel):
    patient_id: str = Field(..., description="Patient UUID or patient_code (PT-001)")


class AnalysisCreated(BaseModel):
    analysis_id: UUID
    analysis_code: str
    status: str


class AnalysisStepOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    status: str
    step_order: int | None = None
    duration_ms: int | None = None
    message: str | None = None


class AnalysisStatusOut(BaseModel):
    analysis_id: UUID
    analysis_code: str
    patient_id: UUID
    patient_code: str | None = None
    status: str
    progress: int
    current_step: str | None
    steps: list[AnalysisStepOut]
    error_message: str | None = None


class AnalysisDetail(AnalysisStatusOut):
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
