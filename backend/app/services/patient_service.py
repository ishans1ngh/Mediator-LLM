from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.patient import Patient, PatientLab, PatientTreatment
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import LabCreate, PatientCreate, PatientUpdate, TreatmentCreate
from app.utils.validators import validate_age, validate_diagnosis, validate_lab_status, validate_patient_code


class PatientService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PatientRepository(db)

    def create_patient(self, data: PatientCreate) -> Patient:
        validated_code = validate_patient_code(data.patient_code)
        if self.repo.get_by_code(validated_code):
            raise ConflictError("PATIENT_CODE_EXISTS", "Patient code already exists.")
        
        validate_age(data.age)
        validate_diagnosis(data.diagnosis)
        
        patient = Patient(
            patient_code=validated_code,
            name=data.name,
            age=data.age,
            gender=data.gender,
            diagnosis=data.diagnosis,
            disease_stage=data.disease_stage,
            clinical_notes=data.clinical_notes,
            medical_history=data.medical_history,
            performance_status=data.performance_status,
            status=data.status or "created",
        )
        return self.repo.add(patient)

    def get_patient(self, patient_id: uuid.UUID) -> Patient:
        patient = self.repo.get_by_id(patient_id)
        if not patient:
            raise NotFoundError("PATIENT_NOT_FOUND", "Patient does not exist.")
        return self.repo.get_with_relations(patient)

    def list_patients(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        diagnosis: str | None = None,
        status: str | None = None,
    ) -> tuple[list[Patient], int]:
        return self.repo.list(page=page, page_size=page_size, search=search, diagnosis=diagnosis, status=status)

    def update_patient(self, patient_id: uuid.UUID, data: PatientUpdate) -> Patient:
        patient = self.get_patient(patient_id)
        
        if data.name is not None:
            patient.name = data.name
        if data.age is not None:
            validate_age(data.age)
            patient.age = data.age
        if data.gender is not None:
            patient.gender = data.gender
        if data.diagnosis is not None:
            validate_diagnosis(data.diagnosis)
            patient.diagnosis = data.diagnosis
        if data.disease_stage is not None:
            patient.disease_stage = data.disease_stage
        if data.clinical_notes is not None:
            patient.clinical_notes = data.clinical_notes
        if data.medical_history is not None:
            patient.medical_history = data.medical_history
        if data.performance_status is not None:
            patient.performance_status = data.performance_status
        if data.status is not None:
            patient.status = data.status
        
        self.db.flush()
        return patient

    def delete_patient(self, patient_id: uuid.UUID) -> None:
        patient = self.get_patient(patient_id)
        self.repo.delete(patient)

    def add_lab(self, patient_id: uuid.UUID, data: LabCreate) -> PatientLab:
        patient = self.get_patient(patient_id)
        validated_status = validate_lab_status(data.status)
        
        lab = PatientLab(
            patient_id=patient.id,
            test_name=data.test_name,
            value=data.value,
            unit=data.unit,
            reference_range=data.reference_range,
            status=validated_status,
            measured_at=data.measured_at,
        )
        return self.repo.add_lab(lab)

    def list_labs(self, patient_id: uuid.UUID) -> list[PatientLab]:
        self.get_patient(patient_id)
        return self.repo.list_labs(patient_id)

    def delete_lab(self, patient_id: uuid.UUID, lab_id: uuid.UUID) -> None:
        self.get_patient(patient_id)
        lab = self.repo.get_lab(lab_id)
        if not lab:
            raise NotFoundError("LAB_NOT_FOUND", "Lab record does not exist.")
        self.repo.delete_lab(lab)

    def add_treatment(self, patient_id: uuid.UUID, data: TreatmentCreate) -> PatientTreatment:
        patient = self.get_patient(patient_id)
        
        treatment = PatientTreatment(
            patient_id=patient.id,
            treatment_name=data.treatment_name,
            treatment_type=data.treatment_type,
            start_date=data.start_date,
            end_date=data.end_date,
            status=data.status,
            notes=data.notes,
        )
        return self.repo.add_treatment(treatment)

    def list_treatments(self, patient_id: uuid.UUID) -> list[PatientTreatment]:
        self.get_patient(patient_id)
        return self.repo.list_treatments(patient_id)

    def delete_treatment(self, patient_id: uuid.UUID, treatment_id: uuid.UUID) -> None:
        self.get_patient(patient_id)
        treatment = self.repo.get_treatment(treatment_id)
        if not treatment:
            raise NotFoundError("TREATMENT_NOT_FOUND", "Treatment record does not exist.")
        self.repo.delete_treatment(treatment)
