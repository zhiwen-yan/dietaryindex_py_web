"""FII database routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from fastapi.responses import FileResponse

from dietaryindex.service.fii_database import DATA_PATH, get_fii_detail, get_fii_peers, get_fii_summary, search_fii


router = APIRouter(tags=["fii"])


@router.get("/fii/summary")
def fii_summary():
    return get_fii_summary()


@router.get("/fii/search")
def fii_search(
    q: str = Query("", max_length=160),
    limit: int = Query(20, ge=1, le=200),
    group: str | None = Query(None),
    direction: str = Query("all", pattern="^(all|anti|pro|neutral)$"),
    sort_by: str = Query("best_match", pattern="^(best_match|fii_asc|fii_desc|score_desc|az)$"),
):
    return {
        "items": search_fii(
            q,
            limit=limit,
            group=group,
            direction=direction,
            sort_by=sort_by,
        )
    }


@router.get("/fii/foods/{fdcd}")
def fii_detail(fdcd: int):
    item = get_fii_detail(fdcd)
    if item is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return item


@router.get("/fii/foods/{fdcd}/peers")
def fii_peers(fdcd: int, limit: int = Query(5, ge=1, le=20)):
    result = get_fii_peers(fdcd, limit=limit)
    if result is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return result


@router.get("/fii/export")
def fii_export():
    return FileResponse(DATA_PATH, media_type="text/csv; charset=utf-8", filename="fii_food_usda.csv")
