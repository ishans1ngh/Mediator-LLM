from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.database import get_db
from app.core.exceptions import AppError
from app.models.trial import Trial
from app.repositories.trial_repository import TrialRepository
from app.schemas.trial import TrialCreate, TrialDetail, TrialListItem, TrialSyncResponse
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
