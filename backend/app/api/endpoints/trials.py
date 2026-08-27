from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.database import get_db
from app.core.exceptions import AppError
from app.models.trial import Trial
from app.repositories.trial_repository import TrialRepository
from app.schemas.criteria import CriteriaParseResponse, CriteriaResponse, TrialCriterionOut
from app.schemas.trial import TrialDetail, TrialListItem, TrialSyncResponse
from app.services.criteria_service import CriteriaService
from app.services.trial_service import TrialService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/trials", tags=["Trials"])


def handle_app_error(exc: AppError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=exc.to_detail())


@router.get("", response_model=list[TrialListItem], summary="List trials")
async def list_trials(
    search: str | None = Query(None),
    condition: str | None = Query(None),
    phase: str | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[TrialListItem]:
    service = TrialService(db)
    trials, _ = await service.search_trials(search, condition, phase, status, page, page_size)
    return [TrialListItem.model_validate(trial) for trial in trials]


@router.get("/search", response_model=list[TrialListItem], summary="Search ClinicalTrials.gov and sync")
async def search_trials(
    condition: str = Query(..., description="Disease/condition to search for"),
    max_results: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[TrialListItem]:
    service = TrialService(db)
    await service.sync_trials(condition, max_results)
    trials, _ = await service.search_trials(condition=condition, page=1, page_size=max_results)
    return [TrialListItem.model_validate(trial) for trial in trials]


@router.get("/{trial_id}", response_model=TrialDetail, summary="Get trial details")
async def get_trial(trial_id: uuid.UUID, db: Session = Depends(get_db)) -> TrialDetail:
    service = TrialService(db)
    try:
        trial = service.get_trial(trial_id)
        repo = TrialRepository(db)
        trial = repo.get_with_criteria(trial)
        return TrialDetail.model_validate(trial)
    except AppError as exc:
        raise handle_app_error(exc)


@router.get("/nct/{nct_id}", response_model=TrialDetail, summary="Get trial by NCT ID")
async def get_trial_by_nct(nct_id: str, db: Session = Depends(get_db)) -> TrialDetail:
    service = TrialService(db)
    try:
        trial = service.get_trial_by_nct(nct_id)
        repo = TrialRepository(db)
        trial = repo.get_with_criteria(trial)
        return TrialDetail.model_validate(trial)
    except AppError as exc:
        raise handle_app_error(exc)


@router.post("/sync", response_model=TrialSyncResponse, summary="Sync trials from ClinicalTrials.gov")
async def sync_trials(
    condition: str = Query(..., description="Disease/condition to search for"),
    max_results: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> TrialSyncResponse:
    service = TrialService(db)
    try:
        result = await service.sync_trials(condition, max_results)
        return TrialSyncResponse(**result)
    except AppError as exc:
        raise handle_app_error(exc)


@router.get("/{trial_id}/criteria", response_model=CriteriaResponse, summary="Get trial criteria")
async def get_trial_criteria(trial_id: uuid.UUID, db: Session = Depends(get_db)) -> CriteriaResponse:
    service = TrialService(db)
    try:
        trial = service.get_trial(trial_id)
        criteria_service = CriteriaService(db)
        criteria = criteria_service.get_trial_criteria(trial.id)
        
        inclusion = [c for c in criteria if c.criterion_type == "INCLUSION"]
        exclusion = [c for c in criteria if c.criterion_type == "EXCLUSION"]
        
        return CriteriaResponse(
            trial_id=str(trial.id),
            inclusion=[TrialCriterionOut.model_validate(c) for c in inclusion],
            exclusion=[TrialCriterionOut.model_validate(c) for c in exclusion],
        )
    except AppError as exc:
        raise handle_app_error(exc)


@router.post("/{trial_id}/criteria/parse", response_model=CriteriaParseResponse, summary="Parse trial eligibility criteria")
async def parse_trial_criteria(trial_id: uuid.UUID, db: Session = Depends(get_db)) -> CriteriaParseResponse:
    service = TrialService(db)
    try:
        trial = service.get_trial(trial_id)
        criteria_service = CriteriaService(db)
        
        if not trial.eligibility_text:
            raise AppError("NO_ELIGIBILITY_TEXT", "Trial has no eligibility text to parse.")
        
        criteria = await criteria_service.parse_trial_criteria(trial.id, trial.eligibility_text)
        
        structured = sum(1 for c in criteria if c.parser_status == "STRUCTURED")
        unstructured = sum(1 for c in criteria if c.parser_status == "UNSTRUCTURED")
        
        return CriteriaParseResponse(
            trial_id=str(trial.id),
            total_criteria=len(criteria),
            structured=structured,
            unstructured=unstructured,
            criteria=[TrialCriterionOut.model_validate(c) for c in criteria],
        )
    except AppError as exc:
        raise handle_app_error(exc)
