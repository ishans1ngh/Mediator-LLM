from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TrialSyncRequest(BaseModel):
    condition: str = Field(..., min_length=1, examples=["Glioblastoma"])


class TrialSyncResponse(BaseModel):
    condition: str
    retrieved: int
    created: int
    updated: int


class TrialCriterionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    criterion_type: str
    criterion_text: str
    structured_field: str | None = None
    operator: str | None = None
    value: str | None = None
    unit: str | None = None


class TrialListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nct_id: str
    title: str
    brief_summary: str | None = None
    phase: str | None = None
    status: str | None = None
    condition: str | None = None
    intervention: str | None = None
    locations: list | None = None
    extra: dict | None = None


class TrialDetail(TrialListItem):
    official_title: str | None = None
    study_type: str | None = None
    source: str
    eligibility_text: str | None = None
    last_updated: datetime | None = None
    created_at: datetime
    criteria: list[TrialCriterionOut] = []


class PaginatedTrials(BaseModel):
    items: list[TrialListItem]
    page: int
    page_size: int
    total: int


class NormalizedTrial(BaseModel):
    nct_id: str
    title: str
    brief_summary: str | None = None
    official_title: str | None = None
    phase: list[str] = []
    status: str | None = None
    conditions: list[str] = []
    interventions: list[str] = []
    study_type: str | None = None
    locations: list[str] = []
    eligibility_text: str | None = None
    extra: dict | None = None
