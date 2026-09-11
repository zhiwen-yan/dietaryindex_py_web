"""Automatic column mapping helpers."""

from __future__ import annotations

from difflib import SequenceMatcher

from dietaryindex.service.registry import get_index_detail


COMMON_SYNONYMS = {
    "respondent_id": ["id", "seqn", "participant_id", "subject_id"],
    "gender": ["sex", "riagendr"],
    "age": ["ridageyr"],
    "total_kcal": ["kcal", "energy", "totalenergy", "totalkcal", "dr1tkcal", "drxtkcal"],
    "kcal": ["energy", "totalenergy", "totalkcal"],
    "total_fruit": ["fruit_total", "totalfruit", "totalfruits"],
    "whole_fruit": ["wholefruit", "wholefruits"],
    "total_vegetable": ["vegetable_total", "totalvegetable", "totalvegetables", "veg_total"],
    "green_and_bean": ["greensandbeans", "greenbean", "greenbeans"],
    "total_protein": ["totalprotein"],
    "seafood_plant_protein": ["seafoodplantprotein", "seafoodplantproteins"],
    "whole_grain": ["wholegrain", "wholegrains"],
    "refined_grain": ["refinedgrain", "refinedgrains"],
    "fatty_acid": ["fattyacidratio"],
    "sodium": ["na", "sodi", "dr1tsodi", "drxtsodi"],
    "fiber": ["fibre", "dietaryfiber", "tfibe", "dr1tfibe", "drxtfibe"],
    "alcohol": ["alco", "dr1talco", "drxtalco"],
    "protein": ["prot", "dr1tprot", "drxtprot"],
    "carb": ["carbohydrate", "carbo", "dr1tcarb", "drxttcarb", "drxtcarb"],
    "totalfat": ["total_fat", "fat", "tfat", "dr1ttfat", "drxttfat"],
    "satfat": ["saturatedfat", "sat_fat", "sfa", "dr1tsfat", "drxtsfat"],
    "pufa": ["poly_fat", "polyunsaturated"],
    "mufa": ["mono_fat", "monounsaturated"],
    "trans_fat": ["transfat", "transfattyacids"],
    "n3_fat": ["n3fat", "omega3", "omega_3"],
    "added_sugar": ["addedsugars", "sugar"],
    "fruit": ["totalfruit", "fruit_total"],
    "vegetable": ["veg", "totalvegetable", "vegetable_total"],
}


def _normalize(text: str) -> str:
    return "".join(ch.lower() for ch in str(text).strip() if ch.isalnum() or ch == "_")


def _candidate_names(field_name: str, label_en: str) -> list[str]:
    names = [field_name, label_en]
    names.extend(COMMON_SYNONYMS.get(field_name.lower(), []))
    return [_normalize(name) for name in names if name]


def _best_match(field_name: str, label_en: str, columns: list[str]) -> tuple[str | None, float]:
    normalized_columns = {column: _normalize(column) for column in columns}
    candidates = _candidate_names(field_name, label_en)
    best_col = None
    best_score = 0.0

    for column, normalized in normalized_columns.items():
        for candidate in candidates:
            if not candidate:
                continue
            if normalized == candidate:
                return column, 1.0
            score = SequenceMatcher(None, normalized, candidate).ratio()
            if candidate in normalized or normalized in candidate:
                score = max(score, 0.86)
            if score > best_score:
                best_col, best_score = column, score
    return (best_col, best_score) if best_score >= 0.72 else (None, 0.0)


def suggest_mapping(index_key: str, columns: list[str]) -> dict:
    detail = get_index_detail(index_key)
    suggestions = {}
    missing_required = []

    for field in detail["fields"]:
        column, score = _best_match(field["name"], field["label_en"], columns)
        suggestions[field["name"]] = {
            "column": column,
            "confidence": round(score, 3),
            "required": field["required"],
            "label_en": field["label_en"],
            "label_zh": field["label_zh"],
        }
        if field["required"] and not column:
            missing_required.append(field["name"])

    return {
        "index_key": index_key,
        "suggestions": suggestions,
        "missing_required": missing_required,
    }


def validate_mapping(index_key: str, mapping: dict[str, str | int | float | None], columns: list[str]) -> dict:
    detail = get_index_detail(index_key)
    field_lookup = {field["name"]: field for field in detail["fields"]}
    missing_required = []
    unknown_columns = []

    for field_name, mapped in mapping.items():
        if isinstance(mapped, str) and mapped and mapped not in columns:
            unknown_columns.append({"field": field_name, "column": mapped})

    for field in detail["fields"]:
        mapped = mapping.get(field["name"])
        if field["required"] and mapped in (None, "", []):
            missing_required.append(field["name"])

    return {
        "index_key": index_key,
        "valid": not missing_required and not unknown_columns,
        "missing_required": missing_required,
        "unknown_columns": unknown_columns,
        "known_fields": list(field_lookup.keys()),
    }
