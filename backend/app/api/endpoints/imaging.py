from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.core.database import get_db
from app.core.exceptions import AppError
from app.schemas.imaging import MriScanOut
from app.services.imaging_service import ImagingService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/patients/{patient_id}/mri", tags=["Imaging"])


def handle_app_error(exc: AppError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=exc.to_detail())


@router.post("", response_model=MriScanOut, summary="Upload MRI scan")
async def upload_mri(
    patient_id: uuid.UUID,
    file: UploadFile = File(...),
    modality: str = Form(...),
    db: Session = Depends(get_db),
) -> MriScanOut:
    service = ImagingService(db)
    try:
        mri_scan = await service.upload_mri(
            patient_id=patient_id,
            file=file.file,
            filename=file.filename or "upload.bin",
            modality=modality,
            content_type=file.content_type,
            file_size=file.size or 0,
        )
        return MriScanOut.model_validate(mri_scan)
    except AppError as exc:
        raise handle_app_error(exc)
