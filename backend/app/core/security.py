import re
import uuid
from pathlib import Path

SAFE_FILENAME_RE = re.compile(r"[^A-Za-z0-9._-]+")
ALLOWED_MRI_EXTENSIONS = {".dcm", ".nii", ".nii.gz", ".png", ".jpg", ".jpeg"}


def sanitize_filename(original_name: str) -> str:
    """Return a safe stored filename. Never trust the client path."""
    name = Path(original_name.replace("\\", "/")).name
    if name.lower().endswith(".nii.gz"):
        stem = name[: -len(".nii.gz")]
        ext = ".nii.gz"
    else:
        stem = Path(name).stem
        ext = Path(name).suffix.lower()
    stem = SAFE_FILENAME_RE.sub("_", stem).strip("._") or "scan"
    stem = stem[:80]
    return f"{uuid.uuid4().hex}_{stem}{ext}"


def extract_extension(original_name: str) -> str:
    name = Path(original_name.replace("\\", "/")).name.lower()
    if name.endswith(".nii.gz"):
        return ".nii.gz"
    return Path(name).suffix.lower()


def is_allowed_mri_file(original_name: str) -> bool:
    return extract_extension(original_name) in ALLOWED_MRI_EXTENSIONS


def resolve_under_base(base: Path, *parts: str) -> Path:
    """Join path parts under base and reject traversal outside it."""
    candidate = (base.joinpath(*parts)).resolve()
    base_resolved = base.resolve()
    if not str(candidate).startswith(str(base_resolved)):
        raise ValueError("Invalid storage path.")
    return candidate
