"""Smoke tests for FISI/FII Python implementation."""

import numpy as np
import pandas as pd

from dietaryindex import (
    compute_fisi,
    compute_fisi_nhanes,
    compute_fisi26_nhanes,
    compute_fisi1_nhanes,
    compute_flav_fisi_nhanes,
)


def _assert_close(actual, expected, tol=1e-12):
    if not np.isclose(actual, expected, atol=tol, rtol=tol):
        raise AssertionError(f"{actual} != {expected}")


def test_compute_fisi_basic():
    df = pd.DataFrame(
        {
            "ID": ["A", "B"],
            "Protein": [56.0, 112.0],
            "Fiber": [31.0, 15.5],
            "Vitamin_C": [90.0, 45.0],
        }
    )
    out = compute_fisi(df, id_col="ID", version="usda")
    assert list(out["ID"]) == ["A", "B"]
    assert "FISI_Total" in out.columns
    assert "FISI_Protein" in out.columns
    assert "Intake_Fiber" in out.columns

    expected_a = 0.021 + (-0.663) + (-0.424)
    _assert_close(out.loc[0, "FISI_Total"], expected_a)
    assert out.loc[0, "Components_Used"] == 3


def test_compute_fisi_col_map_and_china_fallback():
    df = pd.DataFrame(
        {
            "subj": [1],
            "prot_g": [65.0],
            "vitd": [15.0],
        }
    )
    out = compute_fisi(
        df,
        id_col="subj",
        version="china",
        col_map={"Protein": "prot_g", "Vitamin_D": "vitd"},
    )
    # Protein uses China NRV 65; Vitamin_D falls back to USDA NRV 15.
    expected = 0.021 * 65.0 / 65.0 + (-0.446) * 15.0 / 15.0
    _assert_close(out.loc[0, "FISI_Total"], expected)


def test_compute_fisi_component_set_is_enforced():
    df = pd.DataFrame(
        {
            "ID": [1],
            "Protein": [56.0],
            "Fiber": [31.0],
            "Alcohol": [5.15],
        }
    )
    out = compute_fisi(
        df,
        id_col="ID",
        version="usda",
        components=("Protein", "Fiber"),
    )
    assert out.loc[0, "Components_Used"] == 2
    assert "FISI_Alcohol" not in out.columns


def test_compute_fisi_all_missing_row_has_missing_total():
    out = compute_fisi(
        pd.DataFrame({"ID": [1], "Protein": [np.nan], "Fiber": [np.nan]}),
        id_col="ID",
    )
    assert out.loc[0, "Components_Used"] == 0
    assert np.isnan(out.loc[0, "FISI_Total"])


def test_compute_fisi26_nhanes_dataframe():
    day1 = pd.DataFrame(
        {
            "SEQN": [10, 11, 12],
            "DR1DRSTZ": [1, 1, 1],
            "DR1TKCAL": [2000.0, 6000.0, 1800.0],
            "DR1TPROT": [56.0, 56.0, 112.0],
            "DR1TFIBE": [31.0, 31.0, 15.5],
        }
    )
    day2 = pd.DataFrame(
        {
            "SEQN": [10, 12],
            "DR2DRSTZ": [1, 1],
            "DR2TKCAL": [2200.0, 1900.0],
            "DR2TPROT": [112.0, 56.0],
            "DR2TFIBE": [15.5, 31.0],
        }
    )
    demo = pd.DataFrame({"SEQN": [10, 11, 12], "RIDAGEYR": [30, 40, 1], "RIAGENDR": [1, 2, 1]})
    out = compute_fisi26_nhanes(day1, day2, demo, version="usda")
    assert list(out["SEQN"]) == [10, 12]
    assert "RIDAGEYR" in out.columns
    assert np.isnan(out.loc[out["SEQN"] == 12, "RIDAGEYR"]).all()
    assert "FISI_Protein" in out.columns


def test_fisi34_and_fisi26_use_distinct_component_sets():
    day1 = pd.DataFrame(
        {
            "SEQN": [10],
            "DR1DRSTZ": [1],
            "DR1TKCAL": [2000.0],
            "DR1TPROT": [56.0],
            "DR1TALCO": [5.15],
            "DR1TCAFF": [8.05],
        }
    )
    fisi34 = compute_fisi_nhanes(day1, exclude_extremes=False)
    fisi26 = compute_fisi26_nhanes(day1, version="usda", exclude_extremes=False)
    assert "FISI_Alcohol" in fisi34.columns
    assert "FISI_Caffeine" in fisi34.columns
    assert "FISI_Alcohol" not in fisi26.columns
    assert "FISI_Caffeine" not in fisi26.columns
    assert fisi34.loc[0, "Components_Count"] == 4
    assert fisi26.loc[0, "Components_Count"] == 2


def test_compute_fisi1_nhanes_dataframe():
    iff1 = pd.DataFrame({"SEQN": [1, 1, 2], "DR1IFDCD": [1001.0, 1002.0, 1001.0], "DR1IGRMS": [50.0, 100.0, 200.0]})
    tot1 = pd.DataFrame({"SEQN": [1, 2], "DR1DRSTZ": [1, 1], "DR1TKCAL": [2000.0, 1800.0], "DR1TALCO": [0.0, 0.0]})
    food_fii = pd.DataFrame({"FDCD": ["1001", "1002"], "FII": [2.0, -1.0]})
    out = compute_fisi1_nhanes(iff1, tot1, food_fii)
    assert list(out["SEQN"]) == [1, 2]
    _assert_close(out.loc[out["SEQN"] == 1, "FISI1"].iloc[0], 0.0)
    _assert_close(out.loc[out["SEQN"] == 2, "FISI1"].iloc[0], 4.0)


def test_compute_flav_fisi_nhanes_dataframe():
    flav = pd.DataFrame(
        {
            "SEQN": [1, 2],
            "DR1T_FL_3_OLS": [95.8, 47.9],
            "DR1T_FL_ONES": [1.55, 0.0],
        }
    )
    out = compute_flav_fisi_nhanes(flav)
    assert "FLAV_FISI" in out.columns
    assert "FLAV_Flavan_3_ols" in out.columns
    assert out.loc[0, "Flavonoids_Count"] == 2


if __name__ == "__main__":
    tests = [
        test_compute_fisi_basic,
        test_compute_fisi_col_map_and_china_fallback,
        test_compute_fisi_component_set_is_enforced,
        test_compute_fisi26_nhanes_dataframe,
        test_fisi34_and_fisi26_use_distinct_component_sets,
        test_compute_fisi1_nhanes_dataframe,
        test_compute_flav_fisi_nhanes_dataframe,
    ]
    passed = 0
    for fn in tests:
        fn()
        passed += 1
        print(f"[PASS] {fn.__name__}")
    print(f"FISI tests: {passed}/{len(tests)} passed")
