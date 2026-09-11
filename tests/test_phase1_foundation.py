"""Tests for the phase-1 reference engine and registry foundation."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dietaryindex import (
    fit_reference_cutoffs,
    get_family_blueprint_table,
    get_index_spec_table,
    get_output_naming_rules,
    get_reference_cutoffs,
    reference_table_to_wide,
    score_series_with_reference,
)


def test_fit_reference_cutoffs_supports_grouped_quintiles():
    df = pd.DataFrame(
        {
            "gender": [1, 1, 1, 2, 2, 2],
            "fruit": [1.0, 2.0, 3.0, 10.0, 20.0, 30.0],
            "veg": [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],
        }
    )

    reference = fit_reference_cutoffs(
        df,
        columns=["fruit", "veg"],
        method="quintile",
        groupby="gender",
    )

    assert len(reference) == 24
    assert {"gender", "variable", "method", "rank", "prob", "cutoff", "n_non_missing"}.issubset(reference.columns)

    fruit_gender_1 = get_reference_cutoffs(reference, "fruit", filters={"gender": 1})
    assert fruit_gender_1["method"].iloc[0] == "quintile"
    assert fruit_gender_1["cutoff"].iloc[0] == 1.0
    assert fruit_gender_1["cutoff"].iloc[-1] == 3.0

    wide = reference_table_to_wide(reference)
    assert {"cutoff_0", "cutoff_5"}.issubset(wide.columns)


def test_score_series_with_reference_applies_group_specific_cutoffs():
    df = pd.DataFrame(
        {
            "gender": [1, 1, 1, 2, 2, 2],
            "fruit": [1.0, 2.0, 3.0, 10.0, 20.0, 30.0],
        }
    )
    reference = fit_reference_cutoffs(df, columns=["fruit"], method="quintile", groupby="gender")

    scored = score_series_with_reference(
        df["fruit"],
        reference,
        variable="fruit",
        direction="healthy",
        group=df["gender"],
    )

    assert scored.tolist() == [1.0, 3.0, 5.0, 1.0, 3.0, 5.0]


def test_score_series_with_reference_supports_grouped_medians():
    df = pd.DataFrame(
        {
            "gender": [1, 1, 1, 2, 2, 2],
            "legume": [1.0, 2.0, 3.0, 10.0, 20.0, 30.0],
        }
    )
    reference = fit_reference_cutoffs(df, columns=["legume"], method="median", groupby="gender")

    scored = score_series_with_reference(
        df["legume"],
        reference,
        variable="legume",
        direction="healthy",
        group=df["gender"],
    )

    assert scored.tolist() == [0.0, 1.0, 1.0, 0.0, 1.0, 1.0]


def test_registry_tables_expose_active_and_planned_indices():
    specs = get_index_spec_table(include_planned=True)
    active_specs = get_index_spec_table(include_planned=False)
    families = get_family_blueprint_table(include_planned=True)
    rules = get_output_naming_rules()

    assert "DII" in specs["index_key"].tolist()
    assert "PDI" in specs["index_key"].tolist()
    assert "PDI" in active_specs["index_key"].tolist()
    assert specs.loc[specs["index_key"] == "PDI", "supported_modes"].iloc[0] == "general"
    assert specs.loc[specs["index_key"] == "PHDI", "family_key"].iloc[0] == "plant_based"
    assert "inflammatory" in families["family_key"].tolist()
    assert "plant_based" in families["family_key"].tolist()
    assert "total_score" in rules["rule_key"].tolist()


if __name__ == "__main__":
    tests = [
        test_fit_reference_cutoffs_supports_grouped_quintiles,
        test_score_series_with_reference_applies_group_specific_cutoffs,
        test_score_series_with_reference_supports_grouped_medians,
        test_registry_tables_expose_active_and_planned_indices,
    ]
    passed = 0
    for fn in tests:
        fn()
        passed += 1
        print(f"[PASS] {fn.__name__}")
    print(f"Phase-1 foundation tests: {passed}/{len(tests)} passed")
