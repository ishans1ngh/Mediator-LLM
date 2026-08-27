import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class PatientMriScan(Base):
    __tablename__ = "patient_mri_scans"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    modality: Mapped[str] = mapped_column(String(16), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    upload_status: Mapped[str] = mapped_column(String(32), nullable=False, default="UPLOADED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    patient: Mapped["Patient"] = relationship(back_populates="mri_scans")
