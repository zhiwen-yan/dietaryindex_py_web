"""Simple filesystem storage for API uploads and results."""

from __future__ import annotations

from pathlib import Path
import re
from uuid import uuid4

from dietaryindex_api.settings import settings

ROOT = Path(settings.runtime_dir)
UPLOAD_DIR = ROOT / "uploads"
RESULT_DIR = ROOT / "results"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)


def _safe_filename(filename: str, upload_id: str) -> str:
    basename = Path(filename or "").name.strip()
    if not basename:
        return f"{upload_id}.bin"
    cleaned = re.sub(r"[^A-Za-z0-9._\-\u4e00-\u9fff]+", "_", basename)
    return cleaned[:180] or f"{upload_id}.bin"


def save_upload_bytes(filename: str, data: bytes) -> dict:
    upload_id = uuid4().hex
    safe_name = _safe_filename(filename, upload_id)
    path = UPLOAD_DIR / f"{upload_id}_{safe_name}"
    path.write_bytes(data)
    return {"upload_id": upload_id, "filename": safe_name, "path": str(path)}


def resolve_upload_path(upload_id: str) -> str:
    matches = list(UPLOAD_DIR.glob(f"{upload_id}_*"))
    if not matches:
        raise FileNotFoundError(upload_id)
    return str(matches[0])


def create_result_dir(job_id: str) -> str:
    output_dir = RESULT_DIR / job_id
    output_dir.mkdir(parents=True, exist_ok=True)
    return str(output_dir)
