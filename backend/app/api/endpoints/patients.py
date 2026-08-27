from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.database import get_db
from app.core.exceptions import AppError
from app.models.patient import Patient
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import (
    LabCreate,
    LabOut,
    PatientCreate,
    PatientCreated,
    PatientDetail,
    PatientListItem,
    PatientUpdate,
    PaginatedPatients,
    TreatmentCreate,
    TreatmentOut,
)
from app.services.patient_service import PatientService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/patients", tags=["Patients"])


def handle_app_error(exc: AppError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=exc.to_detail())


@router.post("", response_model=PatientCreated, summary="Create patient")
async def create_patient(data: PatientCreate, db: Session = Depends(get_db)) -> PatientCreated:
    service = PatientService(db)
    try:
        patient = service.create_patient(data)
        return PatientCreated(id=patient.id, patient_code=patient.patient_code, status="created")
    except AppError as exc:
        raise handle_app_error(exc)


@router.get("", response_model=PaginatedPatients, summary="List patients")
async def list_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    diagnosis: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
) -> PaginatedPatients:
    service = PatientService(db)
    patients, total = service.list_patients(page, page_size, search, diagnosis, status)
    
    repo = PatientRepository(db)
    items = []
    for patient in patients:
        latest_analysis = repo.latest_analysis(patient.id)
        eligible_count = repo.eligible_count_for_latest(patient.id)
        
        items.append(PatientListItem(
            id=patient.id,
            patient_code=patient.patient_code,
            name=patient.name,
            age=patient.age,
            gender=patient.gender,
            diagnosis=patient.diagnosis,
            disease_stage=patient.disease_stage,
            status=patient.status,
            last_analysis=latest_analysis.created_at if latest_analysis else None,
            eligible_trials=eligible_count,
            display_status=patient.status,
            created_at=patient.created_at,
        ))
    
    return PaginatedPatients(items=items, page=page, page_size=page_size, total=total)


@router.get("/{patient_id}", response_model=PatientDetail, summary="Get patient details")
async def get_patient(patient_id: uuid.UUID, db: Session = Depends(get_db)) -> PatientDetail:
    service = PatientService(db)
    try:
        patient = service.get_patient(patient_id)
        return PatientDetail.model_validate(patient)
    except AppError as exc:
        raise handle_app_error(exc)


@router.put("/{patient_id}", response_model=PatientDetail, summary="Update patient")
async def update_patient(
    patient_id: uuid.UUID, data: PatientUpdate, db: Session = Depends(get_db)
) -> PatientDetail:
    service = PatientService(db)
    try:
        patient = service.update_patient(patient_id, data)
        return PatientDetail.model_validate(patient)
    except AppError as exc:
        raise handle_app_error(exc)


@router.delete("/{patient_id}", summary="Delete patient")
async def delete_patient(patient_id: uuid.UUID, db: Session = Depends(get_db)) -> dict:
    service = PatientService(db)
    try:
        service.delete_patient(patient_id)
        return {"message": "Patient deleted successfully"}
    except AppError as exc:
        raise handle_app_error(exc)


@router.post("/{patient_id}/labs", response_model=LabOut, summary="Add lab result")
async def add_lab(
    patient_id: uuid.UUID, data: LabCreate, db: Session = Depends(get_db)
) -> LabOut:
    service = PatientService(db)
    try:
        lab = service.add_lab(patient_id, data)
        return LabOut.model_validate(lab)
    except AppError as exc:
        raise handle_app_error(exc)


@router.get("/{patient_id}/labs", response_model=list[LabOut], summary="List lab results")
async def list_labs(patient_id: uuid.UUID, db: Session = Depends(get_db)) -> list[LabOut]:
    service = PatientService(db)
    try:
        labs = service.list_labs(patient_id)
        return [LabOut.model_validate(lab) for lab in labs]
    except AppError as exc:
        raise handle_app_error(exc)


@router.delete("/{patient_id}/labs/{lab_id}", summary="Delete lab result")
async def delete_lab(patient_id: uuid.UUID, lab_id: uuid.UUID, db: Session = Depends(get_db)) -> dict:
    service = PatientService(db)
    try:
        service.delete_lab(patient_id, lab_id)
        return {"message": "Lab result deleted successfully"}
    except AppError as exc:
        raise handle_app_error(exc)


@router.post("/{patient_id}/treatments", response_model=TreatmentOut, summary="Add treatment")
async def add_treatment(
    patient_id: uuid.UUID, data: TreatmentCreate, db: Session = Depends(get_db)
) -> TreatmentOut:
    service = PatientService(db)
    try:
        treatment = service.add_treatment(patient_id, data)
        return TreatmentOut.model_validate(treatment)
    except AppError as exc:
        raise handle_app_error(exc)


@router.get("/{patient_id}/treatments", response_model=list[TreatmentOut], summary="List treatments")
async def list_treatments(patient_id: uuid.UUID, db: Session = Depends(get_db)) -> list[TreatmentOut]:
    service = PatientService(db)
    try:
        treatments = service.list_treatments(patient_id)
        return [TreatmentOut.model_validate(t) for t in treatments]
    except AppError as exc:
        raise handle_app_error(exc)


@router.delete("/{patient_id}/treatments/{treatment_id}", summary="Delete treatment")
async def delete_treatment(
    patient_id: uuid.UUID, treatment_id: uuid.UUID, db: Session = Depends(get_db)
) -> dict:
    service = PatientService(db)
    try:
        service.delete_treatment(patient_id, treatment_id)
        return {"message": "Treatment deleted successfully"}
    except AppError as exc:
        raise handle_app_error(exc)
