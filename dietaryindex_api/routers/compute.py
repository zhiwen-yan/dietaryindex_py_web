"""Computation submission routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from dietaryindex_api.jobs import submit_compute_job
from dietaryindex_api.storage import resolve_upload_path


router = APIRouter(tags=["compute"])


class ComputeRequest(BaseModel):
    index_key: str
    mode: str = "general"
    upload_id: str | None = None
    upload_ids: dict[str, str] | None = None
    mapping: dict[str, str | int | float | None] = Field(default_factory=dict)
    options: dict[str, str | int | float | None] = Field(default_factory=dict)
    cycles: list[dict] = Field(default_factory=list, description="Independent NHANES cycles, each with label and upload_ids.")


@router.post("/compute")
def compute(req: ComputeRequest):
    try:
        file_path = resolve_upload_path(req.upload_id) if req.upload_id else None
        file_paths = (
            {role: resolve_upload_path(upload_id) for role, upload_id in (req.upload_ids or {}).items()}
            if req.upload_ids
            else None
        )
        cycles = [
            {
                "label": str(cycle.get("label") or "").strip(),
                "file_paths": {role: resolve_upload_path(upload_id) for role, upload_id in (cycle.get("upload_ids") or {}).items()},
            }
            for cycle in req.cycles
        ]
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Upload not found: {exc}") from exc

    if not file_path and not file_paths and not cycles:
        raise HTTPException(status_code=400, detail="Provide upload_id, upload_ids, or cycles.")

    try:
        job = submit_compute_job(
            index_key=req.index_key,
            mode=req.mode,
            file_path=file_path,
            file_paths=file_paths,
            mapping=req.mapping,
            options=req.options,
            cycles=cycles,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"{type(exc).__name__}: {exc}") from exc
    return job
