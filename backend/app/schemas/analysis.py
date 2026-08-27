from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AnalysisCreate(BaseModel):
    patient_id: UUID


class AnalysisResponse(BaseModel):
    analysis_id: str
    analysis_code: str
    status: str


class AnalysisStepOut(BaseModel):
    name: str
    status: str
    message: str | None = None


class AnalysisStatusResponse(BaseModel):
    analysis_id: str
    status: str
    progress: int
    current_step: str | None
    steps: list[AnalysisStepOut]


class MatchingResultOut(BaseModel):
    trial_id: str
    nct_id: str
    title: str
    match_score: float
    eligibility_status: str
    criteria_passed: int
    criteria_failed: int
    criteria_unknown: int


class MatchingResultsSummary(BaseModel):
    analysis_id: str
    patient_id: str
    summary: dict
    results: list[MatchingResultOut]


class MatchingResultDetail(BaseModel):
    trial: dict
    match_score: float
    eligibility_status: str
    criteria: list[dict]
