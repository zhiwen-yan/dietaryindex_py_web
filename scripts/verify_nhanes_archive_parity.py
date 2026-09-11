"""Compare current NHANES FPED results with archived R outputs.

This is an optional release audit. It requires ``dietaryindex[adapters]`` and
the NHANES 2017-2018 Day 1/Day 2 individual-food files.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from dietaryindex import (
    compute_ahei_nhanes_fped,
    compute_dash_nhanes_fped,
    compute_di_gm_nhanes_fped,
    compute_medi_nhanes_fped,
)


def compare(actual: pd.DataFrame, expected_path: Path, tolerance: float) -> dict:
    expected = pd.read_csv(expected_path)
    joined = expected.merge(actual, on="SEQN", how="outer", suffixes=("_r", "_py"), indicator=True)
    common_columns = [column for column in expected.columns if column != "SEQN" and column in actual]
    mismatch_cells = 0
    max_abs = 0.0
    for column in common_columns:
        delta = (
            pd.to_numeric(joined[f"{column}_py"], errors="coerce")
            - pd.to_numeric(joined[f"{column}_r"], errors="coerce")
        ).abs()
        mismatch_cells += int(((joined["_merge"] == "both") & (delta > tolerance)).sum())
        if delta.notna().any():
            max_abs = max(max_abs, float(delta.max()))
    return {
        "r_rows": len(expected),
        "python_rows": len(actual),
        "matched_rows": int((joined["_merge"] == "both").sum()),
        "r_only_rows": int((joined["_merge"] == "left_only").sum()),
        "python_only_rows": int((joined["_merge"] == "right_only").sum()),
        "common_columns": len(common_columns),
        "mismatch_cells": mismatch_cells,
        "max_abs": max_abs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nhanes-root", required=True, type=Path)
    parser.add_argument("--archive-dir", required=True, type=Path)
    parser.add_argument("--tolerance", type=float, default=1e-11)
    args = parser.parse_args()

    dietary = args.nhanes_root / "Dietary"
    common = {
        "fped_ind_path": dietary / "fped_dr1iff_1718.sas7bdat",
        "nutrient_ind_path": dietary / "dr1iff_j.xpt",
        "fped_ind_path2": dietary / "fped_dr2iff_1718.sas7bdat",
        "nutrient_ind_path2": dietary / "dr2iff_j.xpt",
        "demo_path": args.nhanes_root / "Demographics" / "demo_j.xpt",
    }
    audits = {
        "DASH": (compute_dash_nhanes_fped(**common), "_tmp_r_dash_nhanes.csv"),
        "AHEI": (compute_ahei_nhanes_fped(**common), "_tmp_r_ahei_nhanes.csv"),
        "MEDI": (compute_medi_nhanes_fped(**common), "_tmp_r_medi_nhanes.csv"),
        "DI_GM": (
            compute_di_gm_nhanes_fped(**common, two_day_method="score_average"),
            "_tmp_r_di_gm_nhanes.csv",
        ),
    }

    failed = False
    for name, (actual, archive_name) in audits.items():
        result = compare(actual, args.archive_dir / archive_name, args.tolerance)
        status = "PASS" if result["mismatch_cells"] == 0 and not result["r_only_rows"] and not result["python_only_rows"] else "FAIL"
        print(f"{name}: {status} {result}")
        failed |= status == "FAIL"
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
