from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CriterionEvaluationOut(BaseModel):
    criterion: str
    criterion_type: str | None = None
    result: str
    patient_value: str | None = None
    required_value: str | None = None
    patient_evidence: str | None = None
    explanation: str | None = None


class MatchingResultListItem(BaseModel):
    id: UUID
    trial_id: UUID
    nct_id: str
    title: str
    match_score: float
    eligibility_status: str
    criteria_passed: int
    criteria_failed: int
    criteria_unknown: int
    criteria: list[CriterionEvaluationOut] = []


class MatchingSummary(BaseModel):
    total: int
    eligible: int
    uncertain: int
    not_eligible: int


class AnalysisResultsOut(BaseModel):
    analysis_id: UUID
    patient_id: UUID
    summary: MatchingSummary
    results: list[MatchingResultListItem]


class MatchingResultDetail(BaseModel):
    id: UUID
    analysis_id: UUID
    match_score: float
    eligibility_status: str
    trial: dict
    criteria: list[CriterionEvaluationOut]


class ReportsOut(BaseModel):
    totalAnalyses: int
    averageMatchScore: float
    eligibleRate: float
    unknownRate: float
    eligibilityDistribution: dict
    matchingPerformance: dict
    segmentationMetrics: dict
