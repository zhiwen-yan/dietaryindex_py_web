"""Result packaging helpers."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

RESULT_PREVIEW_ROWS = 5


def _safe_float(value) -> float | None:
    try:
        if pd.isna(value):
            return None
        numeric = float(value)
        return numeric if math.isfinite(numeric) else None
    except Exception:
        return None


def build_result_payload(
    *,
    index_key: str,
    mode: str,
    result: pd.DataFrame,
    output_dir: str | Path | None = None,
    primary_output_column: str | None = None,
    mapping: dict | None = None,
) -> dict:
    numeric_cols = result.select_dtypes(include=["number"]).columns.tolist()
    if primary_output_column is None:
        primary_output_column = numeric_cols[0] if numeric_cols else (result.columns[0] if len(result.columns) else None)

    summary_stats = None
    if primary_output_column and primary_output_column in result.columns:
        series = pd.to_numeric(result[primary_output_column], errors="coerce")
        series = series.where(np.isfinite(series), np.nan)
        summary_stats = {
            "count": int(series.notna().sum()),
            "mean": _safe_float(series.mean()),
            "sd": _safe_float(series.std()),
            "min": _safe_float(series.min()),
            "max": _safe_float(series.max()),
        }

    files = {}
    if output_dir is not None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        csv_path = output_path / f"{index_key.lower()}_{mode}_results.csv"
        xlsx_path = output_path / f"{index_key.lower()}_{mode}_results.xlsx"
        result.to_csv(csv_path, index=False, encoding="utf-8-sig")
        with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
            result.to_excel(writer, index=False, sheet_name="Results")
        files = {
            "csv_path": str(csv_path),
            "xlsx_path": str(xlsx_path),
        }

    preview_frame = result.head(RESULT_PREVIEW_ROWS).copy()
    preview_frame = preview_frame.replace(
        [np.inf, -np.inf],
        np.nan,
    )
    preview = (
        preview_frame.astype(object)
        .where(preview_frame.notna(), None)
        .to_dict(orient="records")
    )

    return {
        "index_key": index_key,
        "mode": mode,
        "rows": int(len(result)),
        "columns": [str(col) for col in result.columns],
        "primary_output_column": primary_output_column,
        "summary_stats": summary_stats,
        "mapping_used": mapping or {},
        "preview": preview,
        "files": files,
    }
