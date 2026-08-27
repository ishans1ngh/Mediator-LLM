from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.core.database import get_db
from app.core.exceptions import AppError
from app.models.analysis import Analysis
from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.analysis import (
    AnalysisCreate,
    AnalysisResponse,
    AnalysisStatusResponse,
    AnalysisStepOut,
    MatchingResultDetail,
    MatchingResultOut,
    MatchingResultsSummary,
)
from app.services.analysis_service import AnalysisService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/analyses", tags=["Analysis"])


def handle_app_error(exc: AppError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=exc.to_detail())


@router.post("", response_model=AnalysisResponse, summary="Create analysis")
async def create_analysis(
    data: AnalysisCreate, db: Session = Depends(get_db)
) -> AnalysisResponse:
    service = AnalysisService(db)
    try:
        analysis = await service.create_analysis(data.patient_id)
        return AnalysisResponse(
            analysis_id=str(analysis.id),
            analysis_code=analysis.analysis_code,
            status=analysis.status,
        )
    except AppError as exc:
        raise handle_app_error(exc)


@router.get("/{analysis_id}", response_model=AnalysisResponse, summary="Get analysis")
async def get_analysis(analysis_id: uuid.UUID, db: Session = Depends(get_db)) -> AnalysisResponse:
    repo = AnalysisRepository(db)
    analysis = repo.get_by_id(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return AnalysisResponse(
        analysis_id=str(analysis.id),
        analysis_code=analysis.analysis_code,
        status=analysis.status,
    )


@router.get("/{analysis_id}/status", response_model=AnalysisStatusResponse, summary="Get analysis status")
async def get_analysis_status(
    analysis_id: uuid.UUID, db: Session = Depends(get_db)
) -> AnalysisStatusResponse:
    repo = AnalysisRepository(db)
    analysis = repo.get_by_id(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    steps = [
        AnalysisStepOut(
            name=step.step_name,
            status=step.status,
            message=step.message,
        )
        for step in analysis.steps
    ]
    
    return AnalysisStatusResponse(
        analysis_id=str(analysis.id),
        status=analysis.status,
        progress=analysis.progress,
        current_step=analysis.current_step,
        steps=steps,
    )


@router.get("/{analysis_id}/results", response_model=MatchingResultsSummary, summary="Get matching results")
async def get_matching_results(
    analysis_id: uuid.UUID, db: Session = Depends(get_db)
) -> MatchingResultsSummary:
    repo = AnalysisRepository(db)
    analysis = repo.get_by_id(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    results = repo.get_matching_results(analysis_id)
    
    eligible = sum(1 for r in results if r.eligibility_status == "ELIGIBLE")
    uncertain = sum(1 for r in results if r.eligibility_status == "UNCERTAIN")
    not_eligible = sum(1 for r in results if r.eligibility_status == "NOT_ELIGIBLE")
    
    result_items = [
        MatchingResultOut(
            trial_id=str(r.trial_id),
            nct_id=r.trial.nct_id,
            title=r.trial.title,
            match_score=float(r.match_score),
            eligibility_status=r.eligibility_status,
            criteria_passed=r.criteria_passed,
            criteria_failed=r.criteria_failed,
            criteria_unknown=r.criteria_unknown,
        )
        for r in results
    ]
    
    return MatchingResultsSummary(
        analysis_id=str(analysis.id),
        patient_id=str(analysis.patient_id),
        summary={
            "total": len(results),
            "eligible": eligible,
            "uncertain": uncertain,
            "not_eligible": not_eligible,
        },
        results=result_items,
    )


@router.get("/matching-results/{result_id}", response_model=MatchingResultDetail, summary="Get matching result details")
async def get_matching_result_detail(
    result_id: uuid.UUID, db: Session = Depends(get_db)
) -> MatchingResultDetail:
    repo = AnalysisRepository(db)
    result = repo.get_matching_result_by_id(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Matching result not found")
    
    trial = result.trial
    
    criteria = [
        {
            "criterion": eval.criterion.criterion_text,
            "result": eval.result,
            "patient_value": eval.patient_value,
            "required_value": eval.required_value,
            "patient_evidence": eval.patient_evidence,
            "explanation": eval.explanation,
        }
        for eval in result.evaluations
    ]
    
    return MatchingResultDetail(
        trial={
            "nct_id": trial.nct_id,
            "title": trial.title,
            "brief_summary": trial.brief_summary,
            "phase": trial.phase,
            "status": trial.status,
            "condition": trial.condition,
        },
        match_score=float(result.match_score),
        eligibility_status=result.eligibility_status,
        criteria=criteria,
    )
