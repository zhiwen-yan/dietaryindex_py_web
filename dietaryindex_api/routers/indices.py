"""Index metadata routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from dietaryindex.service.registry import get_index_catalog, get_index_detail, get_mode_definitions


router = APIRouter(tags=["indices"])


@router.get("/indices")
def list_indices():
    return {"items": get_index_catalog(), "modes": get_mode_definitions()}


@router.get("/indices/{index_key}")
def get_index(index_key: str):
    try:
        return get_index_detail(index_key)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
