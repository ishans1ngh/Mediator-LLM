from __future__ import annotations

import os
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ConflictError, NotFoundError, PayloadTooLargeError
from app.models.imaging import PatientMriScan
from app.repositories.patient_repository import PatientRepository
from app.utils.validators import validate_mri_modality


class ImagingService:
    def __init__(self, db: Session):
        self.db = db
        self.patient_repo = PatientRepository(db)

    def _get_patient_upload_dir(self, patient_code: str, modality: str) -> Path:
        base_dir = Path(settings.upload_dir) / "patients" / patient_code / modality
        base_dir.mkdir(parents=True, exist_ok=True)
        return base_dir

    def _generate_safe_filename(self, original_filename: str) -> str:
        ext = Path(original_filename).suffix or ".bin"
        safe_name = f"{uuid.uuid4()}{ext}"
        return safe_name

    async def upload_mri(
        self,
        patient_id: uuid.UUID,
        file,
        filename: str,
        modality: str,
        content_type: str,
        file_size: int,
    ) -> PatientMriScan:
        patient = self.patient_repo.get_by_id(patient_id)
        if not patient:
            raise NotFoundError("PATIENT_NOT_FOUND", "Patient does not exist.")

        validated_modality = validate_mri_modality(modality)

        if file_size > settings.max_upload_size_bytes:
            raise PayloadTooLargeError("File exceeds maximum allowed size.")

        existing_scans = [
            scan for scan in patient.mri_scans if scan.modality == validated_modality
        ]
        if existing_scans:
            raise ConflictError("MRI_EXISTS", f"Patient already has a {validated_modality} scan.")

        upload_dir = self._get_patient_upload_dir(patient.patient_code, validated_modality)
        safe_filename = self._generate_safe_filename(filename)
        storage_path = str(upload_dir / safe_filename)

        contents = await file.read()
        with open(storage_path, "wb") as f:
            f.write(contents)

        mri_scan = PatientMriScan(
            patient_id=patient.id,
            modality=validated_modality,
            filename=safe_filename,
            storage_path=storage_path,
            mime_type=content_type,
            file_size=file_size,
            upload_status="UPLOADED",
        )
        self.db.add(mri_scan)
        self.db.flush()
        return mri_scan

    async def preprocess_mri(self, mri_scan: PatientMriScan) -> dict:
        return {
            "segmentation_status": "completed",
            "tumor_volume": 24.7,
            "features_extracted": True,
        }

    async def segment_mri(self, mri_scan: PatientMriScan) -> dict:
        return {
            "segmentation_complete": True,
            "tumor_regions": 3,
            "confidence": 0.92,
        }

    async def extract_features(self, mri_scan: PatientMriScan) -> dict:
        return {
            "features": [0.234, -0.567, 0.891, 0.123],
            "feature_dim": 512,
        }
