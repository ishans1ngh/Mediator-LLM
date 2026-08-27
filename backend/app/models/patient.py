import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str | None] = mapped_column(String(32), nullable=True)
    diagnosis: Mapped[str] = mapped_column(String(255), nullable=False)
    disease_stage: Mapped[str | None] = mapped_column(String(128), nullable=True)
    clinical_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    medical_history: Mapped[str | None] = mapped_column(Text, nullable=True)
    performance_status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    profile_attributes: Mapped[list["PatientProfileAttribute"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    labs: Mapped[list["PatientLab"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    treatments: Mapped[list["PatientTreatment"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    mri_scans: Mapped[list["PatientMriScan"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
    analyses: Mapped[list["Analysis"]] = relationship(back_populates="patient", cascade="all, delete-orphan")


class PatientProfileAttribute(Base):
    __tablename__ = "patient_profile_attributes"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    attribute_name: Mapped[str] = mapped_column(String(128), nullable=False)
    attribute_value: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str | None] = mapped_column(String(128), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    patient: Mapped[Patient] = relationship(back_populates="profile_attributes")


class PatientLab(Base):
    __tablename__ = "patient_labs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    test_name: Mapped[str] = mapped_column(String(128), nullable=False)
    value: Mapped[str] = mapped_column(String(64), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reference_range: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="UNKNOWN")
    measured_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    patient: Mapped[Patient] = relationship(back_populates="labs")


class PatientTreatment(Base):
    __tablename__ = "patient_treatments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    treatment_name: Mapped[str] = mapped_column(String(255), nullable=False)
    treatment_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str | None] = mapped_column(String(64), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    patient: Mapped[Patient] = relationship(back_populates="treatments")
