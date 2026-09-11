"""Upload and preview routes."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from dietaryindex.service.files import preview_file
from dietaryindex_api.settings import settings
from dietaryindex_api.storage import resolve_upload_path, save_upload_bytes


router = APIRouter(tags=["uploads"])


@router.post("/uploads")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename or "upload.bin"
    suffix = Path(filename).suffix.lower()
    if suffix not in settings.allowed_extensions:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{suffix or 'none'}'. Allowed: {', '.join(settings.allowed_extensions)}",
        )

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="Uploaded file exceeds the configured size limit")

    saved = save_upload_bytes(filename, data)
    try:
        preview = preview_file(saved["path"], rows=5)
    except Exception as exc:
        preview = {"error": {"type": type(exc).__name__, "message": str(exc)}}
    return {
        "upload_id": saved["upload_id"],
        "filename": saved["filename"],
        "size": len(data),
        "preview": preview,
    }


@router.get("/uploads/{upload_id}/preview")
def preview_uploaded_file(upload_id: str):
    try:
        path = resolve_upload_path(upload_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Upload not found")
    return preview_file(path, rows=10)
