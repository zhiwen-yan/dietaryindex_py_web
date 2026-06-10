"""NHANES FPED tot-level adapters aligned to the dietaryindex R package."""

import numpy as np
import pandas as pd

from dietaryindex.core.dashi import compute_dashi
from dietaryindex.core.hei2015 import compute_hei2015
from dietaryindex.core.hei2020 import compute_hei2020_v2
from dietaryindex.core.med import compute_med


HEI2015_RESULT_COLS = [
    "SEQN", "HEI2015_ALL", "HEI2015_TOTALFRT", "HEI2015_FRT", "HEI2015_VEG",
    "HEI2015_GREENNBEAN", "HEI2015_TOTALPRO", "HEI2015_SEAPLANTPRO",
    "HEI2015_WHOLEGRAIN", "HEI2015_DAIRY", "HEI2015_FATTYACID",
    "HEI2015_REFINEDGRAIN", "HEI2015_SODIUM", "HEI2015_ADDEDSUGAR",
    "HEI2015_SATFAT",
]

HEI2020_RESULT_COLS = [
    "SEQN", "HEI2020_ALL", "HEI2020_TOTALFRT", "HEI2020_FRT", "HEI2020_VEG",
    "HEI2020_GREENNBEAN", "HEI2020_TOTALPRO", "HEI2020_SEAPLANTPRO",
    "HEI2020_WHOLEGRAIN", "HEI2020_DAIRY", "HEI2020_FATTYACID",
    "HEI2020_REFINEDGRAIN", "HEI2020_SODIUM", "HEI2020_ADDEDSUGAR",
    "HEI2020_SATFAT",
]

MED_RESULT_COLS = [
    "SEQN", "MED_ALL", "MED_NOETOH", "MED_FRT", "MED_VEG", "MED_WGRAIN",
    "MED_LEGUMES", "MED_NUTS", "MED_FISH", "MED_REDPROC_MEAT",
    "MED_MONSATFAT", "MED_ALCOHOL",
]

DASHI_RESULT_COLS = [
    "SEQN", "DASHI_ALL", "DASHI_TOTAL_FAT", "DASHI_SAT_FAT",
    "DASHI_CHOLESTEROL", "DASHI_SODIUM", "DASHI_PROTEIN", "DASHI_FIBER",
    "DASHI_POTASSIUM", "DASHI_MAGNESIUM", "DASHI_CALCIUM",
]


def _resolve_upload(file_arg):
    if file_arg is None:
        return None
    if isinstance(file_arg, pd.DataFrame):
        return file_arg.copy()

    import os

    if hasattr(file_arg, "read"):
        if hasattr(file_arg, "seek"):
            file_arg.seek(0)
        ext = os.path.splitext(getattr(file_arg, "name", ""))[1].lower()
    else:
        ext = os.path.splitext(str(file_arg))[1].lower()

    if ext in (".sas7bdat", ""):
        try:
            import pyreadstat
            return pyreadstat.read_sas7bdat(file_arg)[0]
        except Exception:
            pass
    if ext in (".xpt", ".xport", ""):
        try:
            return pd.read_sas(file_arg, format="xport", encoding="utf-8")
        except Exception:
            pass
    try:
        return pd.read_csv(file_arg)
    except Exception as exc:
        raise ValueError(f"Cannot load file: {file_arg}") from exc


def _detect_tot_day(df):
    for day in (1, 2):
        prefix = f"DR{day}T"
        if any(col.startswith(prefix) for col in df.columns):
            return day
    raise ValueError("Cannot detect NHANES recall day from TOT columns.")


def _series(df, col, default=0.0):
    if col in df.columns:
        series = pd.to_numeric(df[col], errors="coerce")
    else:
        series = pd.Series(default, index=df.index, dtype=float)
    return series.where(series.isna() | (series.abs() >= 1e-12), 0.0)


def _ratio_or_zero(numerator, denominator):
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)
    result = np.zeros_like(numerator, dtype=float)
    valid = (~np.isnan(numerator)) & (~np.isnan(denominator)) & (np.abs(denominator) >= 1e-12)
    np.divide(numerator, denominator, out=result, where=valid)
    result[(~valid) & (np.isnan(numerator) | np.isnan(denominator))] = np.nan
    return result


def _prepare_tot_day(
    fped_path,
    nutrient_path,
    demo_path=None,
    *,
    min_age=None,
    join_how="inner",
    filter_positive_kcal=True,
):
    if nutrient_path is None:
        return None, None

    nutrient = _resolve_upload(nutrient_path)
    if nutrient is None:
        return None, None

    day = _detect_tot_day(nutrient)
    line_col = f"DR{day}ILINE"
    if line_col in nutrient.columns:
        raise ValueError(
            f"Please use the population-level data for day {day}. The file name should contain: TOT"
        )

    nutrient = nutrient.copy()
    nutrient["SEQN"] = pd.to_numeric(nutrient["SEQN"], errors="coerce")
    nutrient = nutrient.dropna(subset=["SEQN"]).copy()
    nutrient["SEQN"] = nutrient["SEQN"].astype(int)

    status_col = f"DR{day}DRSTZ"
    if status_col in nutrient.columns:
        nutrient = nutrient[_series(nutrient, status_col) == 1].copy()

    kcal_col = f"DR{day}TKCAL"
    if filter_positive_kcal and kcal_col in nutrient.columns:
        nutrient = nutrient[_series(nutrient, kcal_col) > 1e-12].copy()

    nutrient = nutrient.sort_values("SEQN").reset_index(drop=True)

    demo = None
    if demo_path is not None:
        demo = _resolve_upload(demo_path)
        demo = demo.copy()
        demo["SEQN"] = pd.to_numeric(demo["SEQN"], errors="coerce")
        demo = demo.dropna(subset=["SEQN"]).copy()
        demo["SEQN"] = demo["SEQN"].astype(int)
        if min_age is not None and "RIDAGEYR" in demo.columns:
            demo = demo[_series(demo, "RIDAGEYR") >= min_age].copy()
        demo = demo.sort_values("SEQN").reset_index(drop=True)
        nutrient = nutrient.merge(demo, on="SEQN", how="inner", suffixes=("", "_DEMO"))

    cohort = nutrient
    if fped_path is not None:
        fped = _resolve_upload(fped_path)
        if fped is None:
            return cohort, day
        if line_col in fped.columns:
            raise ValueError(
                f"Please use the population-level data for day {day}. The file name should contain: TOT"
            )
        fped = fped.copy()
        fped["SEQN"] = pd.to_numeric(fped["SEQN"], errors="coerce")
        fped = fped.dropna(subset=["SEQN"]).copy()
        fped["SEQN"] = fped["SEQN"].astype(int)
        if min_age is not None and "RIDAGEYR" in fped.columns:
            fped = fped[_series(fped, "RIDAGEYR") >= min_age].copy()
        fped = fped.sort_values("SEQN").reset_index(drop=True)
        cohort = cohort.merge(fped, on="SEQN", how=join_how, suffixes=("", "_FPED"))

    return cohort.sort_values("SEQN").reset_index(drop=True), day


def _average_two_day_results(day1_result, day2_result):
    if day1_result is None:
        return day2_result
    if day2_result is None:
        return day1_result

    common_cols = [col for col in day1_result.columns if col in day2_result.columns and col != "SEQN"]
    merged = day1_result[["SEQN"] + common_cols].merge(
        day2_result[["SEQN"] + common_cols],
        on="SEQN",
        how="inner",
        suffixes=("_DAY1", "_DAY2"),
    )

    result = pd.DataFrame({"SEQN": merged["SEQN"].astype(int)})
    for col in common_cols:
        result[col] = (
            pd.to_numeric(merged[f"{col}_DAY1"], errors="coerce")
            + pd.to_numeric(merged[f"{col}_DAY2"], errors="coerce")
        ) / 2.0
    return result


def _merge_demo_cols(result, demo_path):
    if demo_path is None or result is None or result.empty:
        return result

    demo = _resolve_upload(demo_path)
    demo = demo.copy()
    demo["SEQN"] = pd.to_numeric(demo["SEQN"], errors="coerce")
    demo = demo.dropna(subset=["SEQN"]).copy()
    demo["SEQN"] = demo["SEQN"].astype(int)
    demo_cols = [c for c in demo.columns if c not in result.columns and c != "SEQN"]
    if not demo_cols:
        return result
    return result.merge(demo[["SEQN"] + demo_cols], on="SEQN", how="left")


def _score_hei2015_day(fped_path, nutrient_path, demo_path):
    cohort, day = _prepare_tot_day(
        fped_path,
        nutrient_path,
        demo_path,
        min_age=2,
        join_how="inner",
        filter_positive_kcal=False,
    )
    if cohort is None or cohort.empty:
        return None

    d = str(day)
    result = compute_hei2015(
        data=cohort,
        respondent_id=cohort["SEQN"].values,
        total_kcal=_series(cohort, f"DR{d}TKCAL").values,
        total_fruit=_series(cohort, f"DR{d}T_F_TOTAL").values,
        whole_fruit=(_series(cohort, f"DR{d}T_F_CITMLB") + _series(cohort, f"DR{d}T_F_OTHER")).values,
        total_vegetable=(_series(cohort, f"DR{d}T_V_TOTAL") + _series(cohort, f"DR{d}T_V_LEGUMES")).values,
        green_and_bean=(_series(cohort, f"DR{d}T_V_DRKGR") + _series(cohort, f"DR{d}T_V_LEGUMES")).values,
        total_protein=(
            _series(cohort, f"DR{d}T_PF_MPS_TOTAL")
            + _series(cohort, f"DR{d}T_PF_EGGS")
            + _series(cohort, f"DR{d}T_PF_NUTSDS")
            + _series(cohort, f"DR{d}T_PF_SOY")
            + _series(cohort, f"DR{d}T_PF_LEGUMES")
        ).values,
        seafood_plant_protein=(
            _series(cohort, f"DR{d}T_PF_SEAFD_HI")
            + _series(cohort, f"DR{d}T_PF_SEAFD_LOW")
            + _series(cohort, f"DR{d}T_PF_NUTSDS")
            + _series(cohort, f"DR{d}T_PF_SOY")
            + _series(cohort, f"DR{d}T_PF_LEGUMES")
        ).values,
        whole_grain=_series(cohort, f"DR{d}T_G_WHOLE").values,
        dairy=_series(cohort, f"DR{d}T_D_TOTAL").values,
        fatty_acid=_ratio_or_zero(
            (_series(cohort, f"DR{d}TMFAT") + _series(cohort, f"DR{d}TPFAT")).to_numpy(dtype=float),
            _series(cohort, f"DR{d}TSFAT").to_numpy(dtype=float),
        ),
        refined_grain=_series(cohort, f"DR{d}T_G_REFINED").values,
        sodium=_series(cohort, f"DR{d}TSODI").values,
        added_sugar=_series(cohort, f"DR{d}T_ADD_SUGARS").values,
        saturated_fat=_series(cohort, f"DR{d}TSFAT").values,
    )
    result["SEQN"] = cohort["SEQN"].values
    return result[HEI2015_RESULT_COLS]


def _score_hei2020_day(fped_path, nutrient_path, demo_path):
    cohort, day = _prepare_tot_day(fped_path, nutrient_path, demo_path, min_age=1, join_how="inner")
    if cohort is None or cohort.empty:
        return None

    d = str(day)
    result = compute_hei2020_v2(
        data=cohort,
        respondent_id=cohort["SEQN"].values,
        age=_series(cohort, "RIDAGEYR", default=np.nan).values,
        total_kcal=_series(cohort, f"DR{d}TKCAL").values,
        total_fruit=_series(cohort, f"DR{d}T_F_TOTAL").values,
        whole_fruit=(_series(cohort, f"DR{d}T_F_CITMLB") + _series(cohort, f"DR{d}T_F_OTHER")).values,
        total_vegetable=(_series(cohort, f"DR{d}T_V_TOTAL") + _series(cohort, f"DR{d}T_V_LEGUMES")).values,
        green_and_bean=(_series(cohort, f"DR{d}T_V_DRKGR") + _series(cohort, f"DR{d}T_V_LEGUMES")).values,
        total_protein=(
            _series(cohort, f"DR{d}T_PF_MPS_TOTAL")
            + _series(cohort, f"DR{d}T_PF_EGGS")
            + _series(cohort, f"DR{d}T_PF_NUTSDS")
            + _series(cohort, f"DR{d}T_PF_SOY")
            + _series(cohort, f"DR{d}T_PF_LEGUMES")
        ).values,
        seafood_plant_protein=(
            _series(cohort, f"DR{d}T_PF_SEAFD_HI")
            + _series(cohort, f"DR{d}T_PF_SEAFD_LOW")
            + _series(cohort, f"DR{d}T_PF_NUTSDS")
            + _series(cohort, f"DR{d}T_PF_SOY")
            + _series(cohort, f"DR{d}T_PF_LEGUMES")
        ).values,
        whole_grain=_series(cohort, f"DR{d}T_G_WHOLE").values,
        dairy=_series(cohort, f"DR{d}T_D_TOTAL").values,
        fatty_acid=_ratio_or_zero(
            (_series(cohort, f"DR{d}TMFAT") + _series(cohort, f"DR{d}TPFAT")).to_numpy(dtype=float),
            _series(cohort, f"DR{d}TSFAT").to_numpy(dtype=float),
        ),
        refined_grain=_series(cohort, f"DR{d}T_G_REFINED").values,
        sodium=_series(cohort, f"DR{d}TSODI").values,
        added_sugar=_series(cohort, f"DR{d}T_ADD_SUGARS").values,
        saturated_fat=_series(cohort, f"DR{d}TSFAT").values,
    )
    result["SEQN"] = cohort["SEQN"].values
    return result[HEI2020_RESULT_COLS]


def _score_med_day(fped_path, nutrient_path, demo_path):
    cohort, day = _prepare_tot_day(fped_path, nutrient_path, demo_path, min_age=2, join_how="left")
    if cohort is None or cohort.empty:
        return None

    d = str(day)
    result = compute_med(
        data=cohort,
        respondent_id=cohort["SEQN"].values,
        fruit_fruit_juice=_series(cohort, f"DR{d}T_F_TOTAL").values,
        vegetable=(
            _series(cohort, f"DR{d}T_V_DRKGR")
            + (
                _series(cohort, f"DR{d}T_V_REDOR_TOTAL")
                + _series(cohort, f"DR{d}T_V_OTHER")
                + _series(cohort, f"DR{d}T_V_STARCHY_OTHER")
            ) / 0.5
        ).values,
        whole_grain=_series(cohort, f"DR{d}T_G_WHOLE").values,
        legumes=(_series(cohort, f"DR{d}T_PF_LEGUMES") + _series(cohort, f"DR{d}T_PF_SOY")).values,
        nuts=_series(cohort, f"DR{d}T_PF_NUTSDS").values,
        fish=(_series(cohort, f"DR{d}T_PF_SEAFD_HI") + _series(cohort, f"DR{d}T_PF_SEAFD_LOW")).values,
        red_processed_meat=(
            _series(cohort, f"DR{d}T_PF_CUREDMEAT") / 1.5
            + (_series(cohort, f"DR{d}T_PF_MEAT") + _series(cohort, f"DR{d}T_PF_ORGAN")) / 4.0
        ).values,
        mon_sat_fat_ratio=_ratio_or_zero(
            _series(cohort, f"DR{d}TMFAT").to_numpy(dtype=float),
            _series(cohort, f"DR{d}TSFAT").to_numpy(dtype=float),
        ),
        alcohol=_series(cohort, f"DR{d}TALCO").values,
    )
    result["SEQN"] = cohort["SEQN"].values
    return result[MED_RESULT_COLS]


def _score_dashi_day(nutrient_path):
    cohort, day = _prepare_tot_day(None, nutrient_path, None)
    if cohort is None or cohort.empty:
        return None

    d = str(day)
    kcal = _series(cohort, f"DR{d}TKCAL").to_numpy(dtype=float)
    result = compute_dashi(
        data=cohort,
        respondent_id=cohort["SEQN"].values,
        total_kcal=kcal,
        total_fat_pct=(_series(cohort, f"DR{d}TTFAT").to_numpy(dtype=float) * 9.0 / kcal) * 100.0,
        sat_fat_pct=(_series(cohort, f"DR{d}TSFAT").to_numpy(dtype=float) * 9.0 / kcal) * 100.0,
        protein_pct=(_series(cohort, f"DR{d}TPROT").to_numpy(dtype=float) * 4.0 / kcal) * 100.0,
        cholesterol=(_series(cohort, f"DR{d}TCHOL").to_numpy(dtype=float) / (kcal / 2000.0)),
        fiber=(_series(cohort, f"DR{d}TFIBE").to_numpy(dtype=float) / (kcal / 2000.0)),
        potassium=(_series(cohort, f"DR{d}TPOTA").to_numpy(dtype=float) / (kcal / 2000.0)),
        magnesium=(_series(cohort, f"DR{d}TMAGN").to_numpy(dtype=float) / (kcal / 2000.0)),
        calcium=(_series(cohort, f"DR{d}TCALC").to_numpy(dtype=float) / (kcal / 2000.0)),
        sodium=(_series(cohort, f"DR{d}TSODI").to_numpy(dtype=float) / (kcal / 2000.0)),
    )
    result["SEQN"] = cohort["SEQN"].values
    return result[DASHI_RESULT_COLS]


def compute_hei2015_nhanes_fped(
    fped_path=None,
    nutrient_path=None,
    demo_path=None,
    fped_path2=None,
    nutrient_path2=None,
):
    day1 = _score_hei2015_day(fped_path, nutrient_path, demo_path) if nutrient_path is not None else None
    day2 = _score_hei2015_day(fped_path2, nutrient_path2, demo_path) if nutrient_path2 is not None else None
    result = _average_two_day_results(day1, day2) if day1 is not None and day2 is not None else (day1 if day1 is not None else day2)
    return _merge_demo_cols(result, demo_path)


def compute_hei2020_nhanes_fped(
    fped_path=None,
    nutrient_path=None,
    demo_path=None,
    fped_path2=None,
    nutrient_path2=None,
):
    day1 = _score_hei2020_day(fped_path, nutrient_path, demo_path) if nutrient_path is not None else None
    day2 = _score_hei2020_day(fped_path2, nutrient_path2, demo_path) if nutrient_path2 is not None else None
    result = _average_two_day_results(day1, day2) if day1 is not None and day2 is not None else (day1 if day1 is not None else day2)
    return _merge_demo_cols(result, demo_path)


def compute_med_nhanes_fped(
    fped_path=None,
    nutrient_path=None,
    demo_path=None,
    fped_path2=None,
    nutrient_path2=None,
):
    day1 = _score_med_day(fped_path, nutrient_path, demo_path) if nutrient_path is not None else None
    day2 = _score_med_day(fped_path2, nutrient_path2, demo_path) if nutrient_path2 is not None else None
    result = _average_two_day_results(day1, day2) if day1 is not None and day2 is not None else (day1 if day1 is not None else day2)
    return _merge_demo_cols(result, demo_path)


def compute_dashi_nhanes_fped(
    nutrient_path=None,
    nutrient_path2=None,
    demo_path=None,
):
    day1 = _score_dashi_day(nutrient_path) if nutrient_path is not None else None
    day2 = _score_dashi_day(nutrient_path2) if nutrient_path2 is not None else None
    result = _average_two_day_results(day1, day2) if day1 is not None and day2 is not None else (day1 if day1 is not None else day2)
    return _merge_demo_cols(result, demo_path)
