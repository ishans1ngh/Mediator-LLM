from __future__ import annotations

import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.analysis import Analysis
from app.models.matching import MatchingResult
from app.models.patient import Patient, PatientLab, PatientProfileAttribute, PatientTreatment


class PatientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, patient_id: uuid.UUID) -> Patient | None:
        return self.db.get(Patient, patient_id)

    def get_by_code(self, patient_code: str) -> Patient | None:
        stmt = select(Patient).where(func.upper(Patient.patient_code) == patient_code.upper())
        return self.db.execute(stmt).scalar_one_or_none()

    def get_with_relations(self, patient: Patient) -> Patient:
        stmt = (
            select(Patient)
            .options(
                selectinload(Patient.labs),
                selectinload(Patient.treatments),
                selectinload(Patient.mri_scans),
                selectinload(Patient.analyses),
                selectinload(Patient.profile_attributes),
            )
            .where(Patient.id == patient.id)
        )
        return self.db.execute(stmt).scalar_one()

    def next_patient_sequence(self) -> int:
        count = self.db.execute(select(func.count()).select_from(Patient)).scalar_one()
        return int(count) + 1

    def list(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        diagnosis: str | None = None,
        status: str | None = None,
    ) -> tuple[list[Patient], int]:
        stmt = select(Patient)
        count_stmt = select(func.count()).select_from(Patient)
        if search:
            like = f"%{search}%"
            filter_clause = or_(
                Patient.name.ilike(like),
                Patient.patient_code.ilike(like),
                Patient.diagnosis.ilike(like),
            )
            stmt = stmt.where(filter_clause)
            count_stmt = count_stmt.where(filter_clause)
        if diagnosis:
            stmt = stmt.where(Patient.diagnosis.ilike(diagnosis))
            count_stmt = count_stmt.where(Patient.diagnosis.ilike(diagnosis))
        if status:
            stmt = stmt.where(Patient.status.ilike(status))
            count_stmt = count_stmt.where(Patient.status.ilike(status))
        total = self.db.execute(count_stmt).scalar_one()
        rows = (
            self.db.execute(
                stmt.order_by(Patient.created_at.desc())
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            .scalars()
            .all()
        )
        return list(rows), int(total)

    def add(self, patient: Patient) -> Patient:
        self.db.add(patient)
        self.db.flush()
        return patient

    def delete(self, patient: Patient) -> None:
        self.db.delete(patient)

    def latest_analysis(self, patient_id: uuid.UUID) -> Analysis | None:
        stmt = (
            select(Analysis)
            .where(Analysis.patient_id == patient_id)
            .order_by(Analysis.created_at.desc())
            .limit(1)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def eligible_count_for_latest(self, patient_id: uuid.UUID) -> int:
        latest = self.latest_analysis(patient_id)
        if not latest:
            return 0
        stmt = select(func.count()).where(
            MatchingResult.analysis_id == latest.id,
            MatchingResult.eligibility_status == "ELIGIBLE",
        )
        return int(self.db.execute(stmt).scalar_one())

    def add_lab(self, lab: PatientLab) -> PatientLab:
        self.db.add(lab)
        self.db.flush()
        return lab

    def get_lab(self, lab_id: uuid.UUID) -> PatientLab | None:
        return self.db.get(PatientLab, lab_id)

    def list_labs(self, patient_id: uuid.UUID) -> list[PatientLab]:
        stmt = select(PatientLab).where(PatientLab.patient_id == patient_id)
        return list(self.db.execute(stmt).scalars().all())

    def delete_lab(self, lab: PatientLab) -> None:
        self.db.delete(lab)

    def add_treatment(self, treatment: PatientTreatment) -> PatientTreatment:
        self.db.add(treatment)
        self.db.flush()
        return treatment

    def get_treatment(self, treatment_id: uuid.UUID) -> PatientTreatment | None:
        return self.db.get(PatientTreatment, treatment_id)

    def list_treatments(self, patient_id: uuid.UUID) -> list[PatientTreatment]:
        stmt = select(PatientTreatment).where(PatientTreatment.patient_id == patient_id)
        return list(self.db.execute(stmt).scalars().all())

    def delete_treatment(self, treatment: PatientTreatment) -> None:
        self.db.delete(treatment)

    def replace_attributes(self, patient_id: uuid.UUID, attributes: list[PatientProfileAttribute]) -> None:
        existing = self.db.execute(
            select(PatientProfileAttribute).where(PatientProfileAttribute.patient_id == patient_id)
        ).scalars().all()
        for row in existing:
            self.db.delete(row)
        for attr in attributes:
            self.db.add(attr)
        self.db.flush()
