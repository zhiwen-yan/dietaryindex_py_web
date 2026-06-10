"""NHANES FPED population-level DII adapter aligned to the dietaryindex R package."""

import os
from io import BytesIO

import numpy as np
import pandas as pd

from dietaryindex.core.dii import compute_dii


# NHANES Nutrient 列名 → DII 参数名 映射
NHANES_NUTRIENT_TO_DII = {
    "DR1TKCAL": "KCAL",
    "DR1TPROT": "PROTEIN",
    "DR1TCARB": "CARB",
    "DR1TFIBE": "FIBER",
    "DR1TTFAT": "TOTALFAT",
    "DR1TSFAT": "SATFAT",
    "DR1TMFAT": "MUFA",
    "DR1TPFAT": "PUFA",
    "DR1TCHOL": "CHOLES",
    "DR1TALCO": "ALCOHOL",
    "DR1TCAFF": "CAFFEINE",
    "DR1TFOLA": "FOLICACID",
    "DR1TNIAC": "NIACIN",
    "DR1TMAGN": "MG",
    "DR1TIRON": "IRON",
    "DR1TZINC": "ZN",
    "DR1TSELE": "SE",
    "DR1TVB1": "THIAMIN",
    "DR1TVB2": "RIBOFLAVIN",
    "DR1TVB6": "VITB6",
    "DR1TVB12": "VITB12",
    "DR1TVC": "VITC",
    "DR1TVD": "VITD",
    "DR1TVARA": "VITA",
    "DR1TATOC": "VITE",
    "DR1TRET": "VITA",
}



def _load_sas_or_xpt(filepath_or_bytes):
    import pyreadstat

    if isinstance(filepath_or_bytes, (str, os.PathLike)):
        path = str(filepath_or_bytes).lower()
        if path.endswith(".sas7bdat"):
            return pyreadstat.read_sas7bdat(filepath_or_bytes)[0]
        if path.endswith(".xpt") or path.endswith(".xport"):
            return pyreadstat.read_xport(filepath_or_bytes)[0]
        raise ValueError(f"Unsupported file format: {filepath_or_bytes}")

    if isinstance(filepath_or_bytes, BytesIO):
        filepath_or_bytes.seek(0)
        raw = filepath_or_bytes.read()
        bio = BytesIO(raw)
        try:
            return pyreadstat.read_sas7bdat(bio)[0]
        except Exception:
            bio.seek(0)
            return pyreadstat.read_xport(bio)[0]

    raise ValueError(f"Unsupported file type: {type(filepath_or_bytes)}")


def _load_other_ingredients(filepath_or_bytes):
    if isinstance(filepath_or_bytes, (str, os.PathLike)):
        return pd.read_csv(filepath_or_bytes)
    if isinstance(filepath_or_bytes, BytesIO):
        filepath_or_bytes.seek(0)
        return pd.read_csv(filepath_or_bytes)
    raise ValueError(f"Unsupported file type: {type(filepath_or_bytes)}")


def _detect_day(df):
    for day in (1, 2):
        if any(col.startswith(f"DR{day}T") for col in df.columns):
            return day
    raise ValueError("Cannot detect NHANES recall day from TOT columns.")


def _series(df, col, default=0.0):
    if col in df.columns:
        series = pd.to_numeric(df[col], errors="coerce")
    else:
        series = pd.Series(default, index=df.index, dtype=float)
    return series.where(series.isna() | (series.abs() >= 1e-12), 0.0)


def _merge_demo_cols(result, demo_path):
    if demo_path is None or result is None or result.empty:
        return result

    demo_df = _load_sas_or_xpt(demo_path).copy()
    demo_df["SEQN"] = pd.to_numeric(demo_df["SEQN"], errors="coerce")
    demo_df = demo_df.dropna(subset=["SEQN"]).copy()
    demo_df["SEQN"] = demo_df["SEQN"].astype(int)
    demo_cols = [c for c in demo_df.columns if c not in result.columns and c != "SEQN"]
    if not demo_cols:
        return result
    return result.merge(demo_df[["SEQN"] + demo_cols], on="SEQN", how="left")


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


def _prepare_day(nutrient_file, demo_file):
    nutrient = _load_sas_or_xpt(nutrient_file)
    day = _detect_day(nutrient)
    if f"DR{day}ILINE" in nutrient.columns:
        raise ValueError(
            f"Please use the population-level data for day {day}. The file name should be like: Totals.csv"
        )

    nutrient = nutrient.copy()
    nutrient["SEQN"] = pd.to_numeric(nutrient["SEQN"], errors="coerce")
    nutrient = nutrient.dropna(subset=["SEQN"]).copy()
    nutrient["SEQN"] = nutrient["SEQN"].astype(int)

    status_col = f"DR{day}DRSTZ"
    if status_col in nutrient.columns:
        nutrient = nutrient[_series(nutrient, status_col) == 1].copy()

    kcal_col = f"DR{day}TKCAL"
    nutrient = nutrient[_series(nutrient, kcal_col) > 1e-12].copy()

    if demo_file is None:
        return nutrient.sort_values("SEQN").reset_index(drop=True), day

    demo = _load_sas_or_xpt(demo_file).copy()
    demo["SEQN"] = pd.to_numeric(demo["SEQN"], errors="coerce")
    demo = demo.dropna(subset=["SEQN"]).copy()
    demo["SEQN"] = demo["SEQN"].astype(int)
    if "RIDAGEYR" in demo.columns:
        demo = demo[_series(demo, "RIDAGEYR", default=np.nan) >= 2].copy()
    demo = demo.sort_values("SEQN").reset_index(drop=True)

    cohort = nutrient.merge(demo[["SEQN"]], on="SEQN", how="inner")
    return cohort.sort_values("SEQN").reset_index(drop=True), day


def _score_day(nutrient_file, demo_file=None, other_ingredients_file=None):
    cohort, day = _prepare_day(nutrient_file, demo_file)
    if cohort is None or cohort.empty:
        return None

    d = str(day)
    kwargs = {
        "respondent_id": cohort["SEQN"].values,
        "ALCOHOL": _series(cohort, f"DR{d}TALCO").values,
        "VITB12": _series(cohort, f"DR{d}TVB12").values,
        "VITB6": _series(cohort, f"DR{d}TVB6").values,
        "BCAROTENE": _series(cohort, f"DR{d}TBCAR").values,
        "CAFFEINE": (_series(cohort, f"DR{d}TCAFF") / 1000.0).values,
        "CARB": _series(cohort, f"DR{d}TCARB").values,
        "CHOLES": _series(cohort, f"DR{d}TCHOL").values,
        "KCAL": _series(cohort, f"DR{d}TKCAL").values,
        "TOTALFAT": _series(cohort, f"DR{d}TTFAT").values,
        "FIBER": _series(cohort, f"DR{d}TFIBE").values,
        "FOLICACID": _series(cohort, f"DR{d}TFA").values,
        "IRON": _series(cohort, f"DR{d}TIRON").values,
        "MG": _series(cohort, f"DR{d}TMAGN").values,
        "MUFA": _series(cohort, f"DR{d}TMFAT").values,
        "NIACIN": _series(cohort, f"DR{d}TNIAC").values,
        "N3FAT": (
            _series(cohort, f"DR{d}TP183")
            + _series(cohort, f"DR{d}TP184")
            + _series(cohort, f"DR{d}TP205")
            + _series(cohort, f"DR{d}TP225")
            + _series(cohort, f"DR{d}TP226")
        ).values,
        "N6FAT": (_series(cohort, f"DR{d}TP182") + _series(cohort, f"DR{d}TP204")).values,
        "PROTEIN": _series(cohort, f"DR{d}TPROT").values,
        "PUFA": _series(cohort, f"DR{d}TPFAT").values,
        "RIBOFLAVIN": _series(cohort, f"DR{d}TVB2").values,
        "SATFAT": _series(cohort, f"DR{d}TSFAT").values,
        "SE": _series(cohort, f"DR{d}TSELE").values,
        "THIAMIN": _series(cohort, f"DR{d}TVB1").values,
        "VITA": _series(cohort, f"DR{d}TVARA").values,
        "VITC": _series(cohort, f"DR{d}TVC").values,
        "VITE": _series(cohort, f"DR{d}TATOC").values,
        "ZN": _series(cohort, f"DR{d}TZINC").values,
    }

    vitd_col = f"DR{d}TVD"
    if vitd_col in cohort.columns:
        kwargs["VITD"] = _series(cohort, vitd_col).values

    if other_ingredients_file is not None:
        other = _load_other_ingredients(other_ingredients_file).copy()
        if "SEQN" in other.columns:
            other["SEQN"] = pd.to_numeric(other["SEQN"], errors="coerce")
            other = other.dropna(subset=["SEQN"]).copy()
            other["SEQN"] = other["SEQN"].astype(int)
            cohort = cohort.merge(other, on="SEQN", how="left", suffixes=("", "_OTHER"))

        def _other(*names):
            for name in names:
                if name in cohort.columns:
                    return _series(cohort, name).values
            return None

        extras = {
            "GARLIC": _other(f"DR{d}TGARLIC", "GARLIC"),
            "GINGER": _other(f"DR{d}TGINGER", "GINGER"),
            "ONION": _other(f"DR{d}TONION", "ONION"),
            "FLA3OL": _other(f"dr{d}t_fl_3_ols", "FLA3OL"),
            "FLAVONES": _other(f"dr{d}t_fl_ones", "FLAVONES"),
            "FLAVONOLS": _other(f"dr{d}t_fl_ols", "FLAVONOLS"),
            "FLAVONONES": _other(f"dr{d}t_fl_nones", "FLAVONONES"),
            "ANTHOC": _other(f"dr{d}t_fl_antho", "ANTHOC"),
            "ISOFLAVONES": _other(f"dr{d}t_fl_iso", "ISOFLAVONES"),
            "PEPPER": _other(f"DR{d}TPEPPER", "PEPPER"),
            "THYME_OREGANO": _other(f"DR{d}TTHYME", f"DR{d}TOREGANO", "THYME_OREGANO"),
        }
        if extras["THYME_OREGANO"] is None and f"DR{d}TTHYME" in cohort.columns and f"DR{d}TOREGANO" in cohort.columns:
            extras["THYME_OREGANO"] = (
                _series(cohort, f"DR{d}TTHYME") + _series(cohort, f"DR{d}TOREGANO")
            ).values
        for key, value in extras.items():
            if value is not None:
                kwargs[key] = value

    result = compute_dii(data=cohort, **kwargs)
    result["SEQN"] = cohort["SEQN"].values
    return result


def compute_dii_nhanes_fped(
    fped_path=None,
    nutrient_path=None,
    demo_path=None,
    fped_path2=None,
    nutrient_path2=None,
    other_ingredients1=None,
    other_ingredients2=None,
):
    if nutrient_path is None and nutrient_path2 is None:
        raise ValueError(
            "Please provide the file path for the FPED and NUTRIENT data, day 1 or day 2 or day 1 and day 2."
        )

    day1 = _score_day(nutrient_path, demo_path, other_ingredients1) if nutrient_path is not None else None
    day2 = _score_day(nutrient_path2, demo_path, other_ingredients2) if nutrient_path2 is not None else None
    result = _average_two_day_results(day1, day2) if day1 is not None and day2 is not None else (day1 if day1 is not None else day2)
    return _merge_demo_cols(result, demo_path)
