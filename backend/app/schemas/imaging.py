from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MriUploadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    patient_id: UUID
    modality: str
    filename: str
    mime_type: str | None
    file_size: int
    upload_status: str
    created_at: datetime


class ImagingStubResult(BaseModel):
    segmentation_status: str
    tumor_volume: float
    features_extracted: bool
    prototype: bool = True
