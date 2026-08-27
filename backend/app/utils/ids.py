import re
from datetime import datetime, timezone

PATIENT_CODE_RE = re.compile(r"^PT-\d{3,}$", re.IGNORECASE)
NCT_ID_RE = re.compile(r"^NCT\d{8}$", re.IGNORECASE)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def generate_patient_code(sequence: int) -> str:
    return f"PT-{sequence:03d}"


def generate_analysis_code(year: int, sequence: int) -> str:
    return f"ANL-{year}-{sequence:03d}"


def is_uuid_like(value: str) -> bool:
    return bool(
        re.fullmatch(
            r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
            value,
        )
    )
