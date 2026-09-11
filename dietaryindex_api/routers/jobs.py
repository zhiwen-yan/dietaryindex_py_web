"""Job status routes."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from dietaryindex_api.jobs import get_job, get_job_view
from dietaryindex_api.settings import settings


router = APIRouter(tags=["jobs"])


@router.get("/jobs/{job_id}")
def job_status(job_id: str):
    try:
        return get_job_view(job_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Job not found") from exc


@router.get("/jobs/{job_id}/download")
def download_job_result(job_id: str, format: str = Query("csv", pattern="^(csv|xlsx)$")):
    try:
        job = get_job(job_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Job not found") from exc

    if job.get("status") != "succeeded":
        raise HTTPException(status_code=409, detail="Job has not completed successfully")

    result = job.get("result") or {}
    path_value = (result.get("files") or {}).get(f"{format}_path")
    if not path_value:
        raise HTTPException(status_code=404, detail=f"{format.upper()} result is unavailable")

    path = Path(path_value).resolve()
    result_root = (Path(settings.runtime_dir) / "results").resolve()
    if not path.is_relative_to(result_root) or not path.is_file():
        raise HTTPException(status_code=404, detail="Result file not found")

    media_type = "text/csv; charset=utf-8" if format == "csv" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return FileResponse(path, media_type=media_type, filename=path.name)
