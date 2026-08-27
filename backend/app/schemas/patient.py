from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PatientCreate(BaseModel):
    patient_code: str = Field(..., examples=["PT-001"])
    name: str = Field(..., min_length=1, examples=["Demo Patient"])
    age: int = Field(..., ge=0, le=120)
    gender: str | None = None
    diagnosis: str = Field(..., min_length=1)
    disease_stage: str | None = None
    clinical_notes: str | None = None
    medical_history: str | None = None
    performance_status: str | None = None
    status: str | None = "ACTIVE"


class PatientUpdate(BaseModel):
    name: str | None = None
    age: int | None = Field(default=None, ge=0, le=120)
    gender: str | None = None
    diagnosis: str | None = None
    disease_stage: str | None = None
    clinical_notes: str | None = None
    medical_history: str | None = None
    performance_status: str | None = None
    status: str | None = None


class PatientCreated(BaseModel):
    id: UUID
    patient_code: str
    status: str


class LabCreate(BaseModel):
    test_name: str
    value: str
    unit: str | None = None
    reference_range: str | None = None
    status: str | None = "UNKNOWN"
    measured_at: datetime | None = None


class LabOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    test_name: str
    value: str
    unit: str | None
    reference_range: str | None
    status: str
    measured_at: datetime | None = None


class TreatmentCreate(BaseModel):
    treatment_name: str
    treatment_type: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: str | None = None
    notes: str | None = None


class TreatmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    treatment_name: str
    treatment_type: str | None
    start_date: datetime | None
    end_date: datetime | None
    status: str | None
    notes: str | None


class MriScanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    modality: str
    filename: str
    mime_type: str | None
    file_size: int
    upload_status: str
    created_at: datetime


class AnalysisSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    analysis_code: str
    status: str
    progress: int
    created_at: datetime
    completed_at: datetime | None = None


class PatientListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    patient_code: str
    name: str
    age: int
    gender: str | None
    diagnosis: str
    disease_stage: str | None
    status: str
    last_analysis: datetime | None = None
    eligible_trials: int = 0
    display_status: str | None = None
    created_at: datetime


class PatientDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    patient_code: str
    name: str
    age: int
    gender: str | None
    diagnosis: str
    disease_stage: str | None
    clinical_notes: str | None
    medical_history: str | None
    performance_status: str | None
    status: str
    created_at: datetime
    labs: list[LabOut] = []
    treatments: list[TreatmentOut] = []
    mri_scans: list[MriScanOut] = []
    analyses: list[AnalysisSummaryOut] = []


class PaginatedPatients(BaseModel):
    items: list[PatientListItem]
    page: int
    page_size: int
    total: int


class PatientAttributeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    attribute_name: str
    attribute_value: str | None
    normalized_value: str | None
    unit: str | None
    source: str | None
    source_text: str | None
    status: str
    confidence: float | None
    agent_version: str | None
    prompt_version: str | None
    model_name: str | None


class PatientProfileOut(BaseModel):
    patient_id: str
    attributes: list[PatientAttributeOut]
    overall_status: str


class PatientExtractResponse(BaseModel):
    patient_id: str
    status: str
    attributes: list[PatientAttributeOut]
