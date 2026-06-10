from __future__ import annotations

from functools import lru_cache

import numpy as np
import pandas as pd

from config.params import INDEX_PARAMS


DII_POPULATED_COLUMNS = {
    "ALCOHOL",
    "BCAROTENE",
    "CARB",
    "CAFFEINE",
    "FIBER",
    "IRON",
    "KCAL",
    "MG",
    "N3FAT",
    "PROTEIN",
    "PUFA",
    "SE",
    "THIAMIN",
    "TOTALFAT",
    "TRANSFAT",
    "VITA",
    "VITB12",
    "VITB6",
    "VITC",
    "ZN",
}

CASE_LABELS = (
    "baseline_low",
    "baseline_mid",
    "baseline_high",
    "partial_missing",
    "boundary_high",
)

SAMPLE_PROFILES = {
    "demo": {
        "label": {"zh": "演示版（尽量填满）", "en": "Demo Sample (Mostly Populated)"},
        "file_suffix": "demo_50rows",
        "include_missing": False,
        "description": {
            "zh": "用于前端快速体验，默认尽量为各列提供示例值。",
            "en": "Designed for quick frontend exploration, with example values populated for most fields.",
        },
    },
    "consistency": {
        "label": {"zh": "一致性测试版（保留空列）", "en": "Consistency Test Sample (Missing Fields Preserved)"},
        "file_suffix": "consistency_50rows",
        "include_missing": True,
        "description": {
            "zh": "用于验证空列、缺失列时 Python 与 R 的处理一致性。",
            "en": "Designed to verify that Python and R handle empty or missing fields consistently.",
        },
    },
}


def _unit_meta(actual_key: str) -> dict[str, dict[str, object]]:
    cfg = INDEX_PARAMS[actual_key]
    meta: dict[str, dict[str, object]] = {}

    for extra in cfg.get("extra_params", []):
        meta[extra["name"]] = {
            "required": extra.get("required", False),
            "unit": extra.get("unit", ""),
        }

    for group in cfg.get("groups", []):
        for param in group["params"]:
            meta[param["name"]] = {
                "required": param.get("required", False),
                "unit": param.get("unit", ""),
            }

    return meta


def _service_like_sequence(name: str) -> list[float]:
    name = name.lower()
    if "items" in name:
        return [1.0, 4.0, 0.0, 2.0, 6.0]
    if any(token in name for token in ("ssb", "sweet", "red_processed_meat", "processed_meat", "red_meat")):
        return [0.0, 1.0, 2.5, 0.5, 3.5]
    if "coffee" in name:
        return [0.0, 1.5, 3.0, 0.5, 4.0]
    if "tea" in name:
        return [0.0, 1.0, 2.5, 0.5, 3.0]
    if "alcohol" in name:
        return [0.0, 0.5, 1.5, 0.25, 3.0]
    return [0.4, 1.8, 3.6, 0.9, 5.0]


def _gram_sequence(name: str) -> list[float]:
    name = name.lower()
    if "whole_grain" in name:
        return [20.0, 60.0, 110.0, 35.0, 130.0]
    if "fat" in name and "added" not in name:
        return [25.0, 50.0, 75.0, 35.0, 90.0]
    if "protein" in name:
        return [35.0, 60.0, 85.0, 45.0, 100.0]
    if "fiber" in name:
        return [12.0, 20.0, 35.0, 15.0, 45.0]
    if "alcohol" in name:
        return [0.0, 8.0, 18.0, 4.0, 28.0]
    if any(token in name for token in ("garlic", "onion", "pepper", "tea")):
        return [0.0, 1.5, 4.0, 0.5, 6.0]
    return [5.0, 15.0, 35.0, 10.0, 50.0]


def _milligram_sequence(name: str) -> list[float]:
    name = name.lower()
    if "sodium" in name:
        return [900.0, 1800.0, 2800.0, 1200.0, 4200.0]
    if "chol" in name:
        return [120.0, 220.0, 360.0, 150.0, 420.0]
    if "potassium" in name:
        return [1800.0, 2600.0, 3600.0, 2200.0, 4200.0]
    if "calcium" in name:
        return [500.0, 800.0, 1200.0, 650.0, 1400.0]
    if "magnesium" in name or name == "mg":
        return [180.0, 260.0, 360.0, 220.0, 420.0]
    if "iron" in name:
        return [6.0, 12.0, 18.0, 9.0, 24.0]
    if "fiber" in name:
        return [12.0, 20.0, 35.0, 15.0, 45.0]
    if "n3" in name or "omega" in name:
        return [120.0, 220.0, 320.0, 150.0, 380.0]
    return [40.0, 120.0, 280.0, 80.0, 420.0]


def _microgram_sequence(name: str) -> list[float]:
    name = name.lower()
    if "b12" in name:
        return [1.0, 2.5, 5.0, 1.5, 7.0]
    if "vitd" in name:
        return [5.0, 10.0, 15.0, 8.0, 20.0]
    if "bcarotene" in name:
        return [500.0, 1400.0, 2800.0, 900.0, 4200.0]
    if "fol" in name:
        return [180.0, 320.0, 480.0, 240.0, 650.0]
    return [80.0, 180.0, 360.0, 120.0, 520.0]


def _ratio_sequence(name: str) -> list[float]:
    name = name.lower()
    if "white_red_ratio" in name:
        return [0.8, 1.5, 2.5, 1.1, 3.5]
    if "poly_sat_ratio" in name:
        return [0.5, 1.0, 1.6, 0.8, 2.2]
    if "mufa_sfa_ratio" in name:
        return [1.0, 1.5, 2.2, 1.2, 2.8]
    return [0.7, 1.3, 2.2, 1.0, 3.0]


def _percent_sequence(name: str) -> list[float]:
    name = name.lower()
    if "trans" in name:
        return [0.5, 1.2, 2.4, 0.8, 3.8]
    if "pufa" in name:
        return [4.0, 7.0, 10.0, 5.5, 12.0]
    if "added_sugar" in name:
        return [4.0, 10.0, 18.0, 7.0, 25.0]
    if "saturated_fat" in name or "satfat" in name:
        return [5.0, 8.0, 12.0, 6.5, 18.0]
    if "fat_pct" in name:
        return [20.0, 28.0, 36.0, 24.0, 42.0]
    return [3.0, 7.0, 12.0, 5.0, 18.0]


def _density_sequence() -> list[float]:
    return [0.5, 1.0, 1.6, 0.8, 2.2]


def _energy_sequence() -> list[float]:
    return [1800.0, 1400.0, 2200.0, 1600.0, 1900.0]


def _tsp_sequence() -> list[float]:
    return [2.0, 6.0, 12.0, 4.0, 18.0]


def _base_values(actual_key: str, column: str, meta: dict[str, object]) -> list[float | int]:
    unit = str(meta.get("unit", "") or "").lower()
    normalized = column.lower()

    if normalized == "respondent_id":
        return [1001, 1002, 1003, 1004, 1005]
    if normalized == "repeat_num":
        return [1, 1, 1, 1, 1]
    if normalized == "gender":
        return [1, 2, 1, 2, 1]
    if normalized == "age":
        return [35.0, 1.5, 2.0, 67.0, 24.0]
    if normalized in {"total_kcal", "kcal"} or unit == "kcal":
        return _energy_sequence()
    if unit == "ratio":
        return _ratio_sequence(normalized)
    if "g/1000kcal" in unit:
        return _density_sequence()
    if "drinks/day" in unit:
        return [0.0, 0.5, 1.5, 0.25, 3.0]
    if "%" in unit:
        return _percent_sequence(normalized)
    if "tsp" in unit:
        return _tsp_sequence()
    if "servings/day" in unit or "cup eq." in unit or "oz eq." in unit:
        return _service_like_sequence(normalized)
    if unit == "g/day" or unit == "g":
        return _gram_sequence(normalized)
    if "mg/day" in unit or unit == "mg":
        return _milligram_sequence(normalized)
    if "μg" in unit or "ug" in unit:
        return _microgram_sequence(normalized)
    if normalized in {"fruit_items", "vegetable_items"}:
        return [1.0, 3.0, 5.0, 2.0, 6.0]
    if normalized.endswith("_items"):
        return [1.0, 2.0, 4.0, 2.0, 5.0]
    if normalized == "fatty_acid":
        return _ratio_sequence(normalized)
    if normalized == "hpf_rg_ratio":
        return _percent_sequence(normalized)
    if normalized == "hpf_servings":
        return _service_like_sequence(normalized)
    if normalized == "alcohol":
        if actual_key == "DII":
            return _gram_sequence(normalized)
        return [0.0, 0.5, 1.5, 0.25, 3.0]
    if normalized.startswith("vit") or normalized in {"folate", "bcarotene"}:
        return _microgram_sequence(normalized)
    if normalized in {"potassium", "magnesium", "calcium", "iron", "cholesterol"}:
        return _milligram_sequence(normalized)
    if normalized in {"coffee", "green_tea"}:
        return _service_like_sequence(normalized)
    return _service_like_sequence(normalized)


def _adjust_numeric_value(column: str, meta: dict[str, object], value: float | int, batch_idx: int) -> float | int:
    if batch_idx == 0:
        return value

    unit = str(meta.get("unit", "") or "").lower()
    normalized = column.lower()

    if normalized in {"respondent_id", "repeat_num", "gender", "age"}:
        return value
    if normalized in {"total_kcal", "kcal"} or unit == "kcal":
        return float(value) + (batch_idx * 60.0)
    if unit == "ratio":
        return round(float(value) + (batch_idx * 0.08), 3)
    if "%" in unit:
        return round(float(value) + (batch_idx * 0.35), 3)
    if "tsp" in unit:
        return round(float(value) + (batch_idx * 0.4), 3)
    if normalized.endswith("_items"):
        return round(float(value) + (batch_idx % 3), 3)
    return round(float(value) * (1.0 + batch_idx * 0.04), 3)


def _ordered_columns(actual_key: str) -> list[str]:
    return list(_unit_meta(actual_key).keys())


def sample_profile_meta(profile: str) -> dict[str, object]:
    if profile not in SAMPLE_PROFILES:
        raise KeyError(f"Unknown sample profile: {profile}")
    return SAMPLE_PROFILES[profile]


@lru_cache(maxsize=None)
def _cached_sample_csv(
    actual_key: str,
    row_count: int,
    include_missing: bool,
    allow_zero_energy: bool,
) -> bytes:
    df = build_sample_dataframe(
        actual_key,
        row_count=row_count,
        include_missing=include_missing,
        allow_zero_energy=allow_zero_energy,
    )
    return df.to_csv(index=False).encode("utf-8-sig")


def build_sample_dataframe(
    actual_key: str,
    row_count: int = 50,
    *,
    include_missing: bool = False,
    allow_zero_energy: bool = False,
    include_test_case: bool = False,
) -> pd.DataFrame:
    meta = _unit_meta(actual_key)
    columns = _ordered_columns(actual_key)
    if include_test_case:
        columns = columns + ["test_case"]

    rows: list[dict[str, object]] = []
    for row_idx in range(row_count):
        case_idx = row_idx % len(CASE_LABELS)
        batch_idx = row_idx // len(CASE_LABELS)
        row: dict[str, object] = {}

        for column in _ordered_columns(actual_key):
            if include_missing and actual_key == "DII" and column.isupper() and column not in DII_POPULATED_COLUMNS:
                row[column] = np.nan
                continue
            values = _base_values(actual_key, column, meta.get(column, {}))
            value = values[case_idx]
            if isinstance(value, (int, float, np.integer, np.floating)):
                value = _adjust_numeric_value(column, meta.get(column, {}), value, batch_idx)
            if column == "respondent_id":
                value = 1001 + row_idx
            row[column] = value

        if include_test_case:
            row["test_case"] = f"{CASE_LABELS[case_idx]}_{batch_idx + 1:02d}"

        rows.append(row)

    if include_missing:
        candidate_columns = [
            column
            for column in _ordered_columns(actual_key)
            if column not in {"respondent_id", "repeat_num", "gender", "age", "total_kcal", "KCAL"}
        ]
        if candidate_columns:
            for row_idx in range(3, row_count, len(CASE_LABELS)):
                rows[row_idx][candidate_columns[0]] = np.nan
                rows[row_idx][candidate_columns[len(candidate_columns) // 2]] = np.nan

    if rows:
        if "total_kcal" in rows[-1]:
            rows[-1]["total_kcal"] = 0.0 if allow_zero_energy else max(float(rows[-1]["total_kcal"]), 900.0)
        if "KCAL" in rows[-1]:
            rows[-1]["KCAL"] = 0.0 if allow_zero_energy else max(float(rows[-1]["KCAL"]), 900.0)

    return pd.DataFrame(rows, columns=columns)


def build_sample_csv_bytes(
    actual_key: str,
    row_count: int = 50,
    *,
    include_missing: bool = False,
    allow_zero_energy: bool = False,
) -> bytes:
    return _cached_sample_csv(actual_key, row_count, include_missing, allow_zero_energy)


def build_profile_sample_dataframe(
    actual_key: str,
    profile: str,
    row_count: int = 50,
    *,
    allow_zero_energy: bool = False,
    include_test_case: bool = False,
) -> pd.DataFrame:
    meta = sample_profile_meta(profile)
    return build_sample_dataframe(
        actual_key,
        row_count=row_count,
        include_missing=bool(meta["include_missing"]),
        allow_zero_energy=allow_zero_energy,
        include_test_case=include_test_case,
    )


def build_profile_sample_csv_bytes(
    actual_key: str,
    profile: str,
    row_count: int = 50,
    *,
    allow_zero_energy: bool = False,
) -> bytes:
    meta = sample_profile_meta(profile)
    return build_sample_csv_bytes(
        actual_key,
        row_count=row_count,
        include_missing=bool(meta["include_missing"]),
        allow_zero_energy=allow_zero_energy,
    )
