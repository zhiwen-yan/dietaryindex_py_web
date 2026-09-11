"""Focused tests for the PDI / hPDI / uPDI family."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dietaryindex import compute_hpdi, compute_pdi, compute_updi, fit_reference_cutoffs


def _build_monotonic_inputs() -> pd.DataFrame:
    values = [1, 2, 3, 4, 5]
    return pd.DataFrame(
        {
            "respondent_id": [101, 102, 103, 104, 105],
            "whole_grain": values,
            "fruit": values,
            "vegetable": values,
            "nuts": values,
            "legumes": values,
            "vegetable_oil": values,
            "tea_coffee": values,
            "fruit_juice": values,
            "refined_grain": values,
            "potatoes": values,
            "ssb": values,
            "sweets_desserts": values,
            "animal_fat": values,
            "dairy": values,
            "eggs": values,
            "fish_seafood": values,
            "meat": values,
            "misc_animal_based": values,
        }
    )


def _compute_with(func, df: pd.DataFrame, **extra):
    return func(
        data=df,
        respondent_id=df["respondent_id"],
        whole_grain=df["whole_grain"],
        fruit=df["fruit"],
        vegetable=df["vegetable"],
        nuts=df["nuts"],
        legumes=df["legumes"],
        vegetable_oil=df["vegetable_oil"],
        tea_coffee=df["tea_coffee"],
        fruit_juice=df["fruit_juice"],
        refined_grain=df["refined_grain"],
        potatoes=df["potatoes"],
        ssb=df["ssb"],
        sweets_desserts=df["sweets_desserts"],
        animal_fat=df["animal_fat"],
        dairy=df["dairy"],
        eggs=df["eggs"],
        fish_seafood=df["fish_seafood"],
        meat=df["meat"],
        misc_animal_based=df["misc_animal_based"],
        **extra,
    )


def test_pdi_family_returns_expected_monotonic_totals():
    df = _build_monotonic_inputs()

    pdi = _compute_with(compute_pdi, df)
    hpdi = _compute_with(compute_hpdi, df)
    updi = _compute_with(compute_updi, df)

    assert pdi["PDI_ALL"].tolist() == [42.0, 48.0, 54.0, 60.0, 66.0]
    assert hpdi["HPDI_ALL"].tolist() == [62.0, 58.0, 54.0, 50.0, 46.0]
    assert updi["UPDI_ALL"].tolist() == [70.0, 62.0, 54.0, 46.0, 38.0]


def test_pdi_can_reuse_external_reference_cutoffs():
    df = _build_monotonic_inputs()
    reference = fit_reference_cutoffs(df, columns=[col for col in df.columns if col != "respondent_id"], method="quintile")

    direct = _compute_with(compute_pdi, df)
    reused = _compute_with(compute_pdi, df, reference=reference)

    assert direct.equals(reused)


if __name__ == "__main__":
    tests = [
        test_pdi_family_returns_expected_monotonic_totals,
        test_pdi_can_reuse_external_reference_cutoffs,
    ]
    passed = 0
    for fn in tests:
        fn()
        passed += 1
        print(f"[PASS] {fn.__name__}")
    print(f"PDI tests: {passed}/{len(tests)} passed")
