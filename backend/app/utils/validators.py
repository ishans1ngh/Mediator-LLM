from app.core.exceptions import AppError
from app.utils.ids import NCT_ID_RE, PATIENT_CODE_RE


def validate_patient_code(patient_code: str) -> str:
    code = (patient_code or "").strip().upper()
    if not PATIENT_CODE_RE.match(code):
        raise AppError("INVALID_PATIENT_CODE", "Patient code must match PT-XXX (e.g. PT-001).")
    return code


def validate_age(age: int) -> int:
    if age < 0 or age > 120:
        raise AppError("INVALID_AGE", "Age must be between 0 and 120.")
    return age


def validate_diagnosis(diagnosis: str) -> str:
    value = (diagnosis or "").strip()
    if not value:
        raise AppError("INVALID_DIAGNOSIS", "Diagnosis is required.")
    return value


def validate_nct_id(nct_id: str) -> str:
    value = (nct_id or "").strip().upper()
    if not NCT_ID_RE.match(value):
        raise AppError("INVALID_NCT_ID", "NCT ID must match NCT########.")
    return value


def validate_lab_status(status: str | None) -> str:
    value = (status or "UNKNOWN").upper()
    if value not in {"NORMAL", "ABNORMAL", "UNKNOWN"}:
        raise AppError("INVALID_LAB_STATUS", "Lab status must be NORMAL, ABNORMAL, or UNKNOWN.")
    return value


def validate_mri_modality(modality: str) -> str:
    value = (modality or "").strip().upper()
    if value not in {"T1", "T2", "FLAIR"}:
        raise AppError("INVALID_MODALITY", "MRI modality must be T1, T2, or FLAIR.")
    return value
