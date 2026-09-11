"""Mapping suggestion and validation routes."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from dietaryindex.service.mapping import suggest_mapping, validate_mapping


router = APIRouter(tags=["mapping"])


class MappingSuggestionRequest(BaseModel):
    index_key: str
    columns: list[str]


class MappingValidationRequest(BaseModel):
    index_key: str
    columns: list[str]
    mapping: dict[str, str | int | float | None]


@router.post("/mapping/suggest")
def suggest(req: MappingSuggestionRequest):
    return suggest_mapping(req.index_key, req.columns)


@router.post("/mapping/validate")
def validate(req: MappingValidationRequest):
    return validate_mapping(req.index_key, req.mapping, req.columns)
