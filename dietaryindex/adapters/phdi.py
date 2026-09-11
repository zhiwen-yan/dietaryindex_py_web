"""NHANES adapters for Planetary Health Diet Index (PHDI/PHD score)."""

import numpy as np
import pandas as pd
import re

from dietaryindex.adapters.nhanes_fped_other import _resolve_upload


PHDI_NHANES_RESULT_COLS = [
    "SEQN",
    "PHDI_ALL",
    "PHDI_140",
    "PHDI_140_LITERAL",
    "PHDI_140_RECONSTRUCTED",
    "PHDI_WGRAIN",
    "PHDI_FRUIT",
    "PHDI_VEG",
    "PHDI_NUTS",
    "PHDI_LEGUMES",
    "PHDI_SOY",
    "PHDI_OIL",
    "PHDI_STARCHY",
    "PHDI_DAIRY",
    "PHDI_REDMEAT",
    "PHDI_POULTRY",
    "PHDI_EGGS",
    "PHDI_FISH",
    "PHDI_SATFAT",
    "PHDI_SUGAR",
    "KCAL",
    "KCAL_TWO_DAY",
]


def compute_phdi_nhanes_fped(
    fped_path=None,
    nutrient_path=None,
    demo_path=None,
    fped_path2=None,
    nutrient_path2=None,
    *,
    score_version="reconstructed",
    min_age=20,
    energy_min=500,
    energy_max=8000,
):
    """Compute paper-aligned 0-140 PHDI from NHANES FPED total files.

    This adapter follows the NHANES 2005-2018 reconstruction logic used for
    the Food Science & Nutrition PHDI-140 paper supplied with this project.
    Day 1 is required; Day 2 is averaged with Day 1 when both recall statuses
    are complete. DEMO is required for sex-specific whole-grain scoring and
    adult filtering.
    """
    if fped_path is None or nutrient_path is None:
        raise ValueError("Day 1 FPED total and total nutrient files are required.")
    if demo_path is None:
        raise ValueError("DEMO file is required for PHDI NHANES scoring.")

    raw = build_phdi_nhanes_fped_components(
        fped_path=fped_path,
        nutrient_path=nutrient_path,
        demo_path=demo_path,
        fped_path2=fped_path2,
        nutrient_path2=nutrient_path2,
    )
    if raw.empty:
        return pd.DataFrame(columns=PHDI_NHANES_RESULT_COLS)

    score_version = str(score_version).lower()
    if score_version not in {"reconstructed", "literal"}:
        raise ValueError('score_version must be either "reconstructed" or "literal".')

    cohort = raw.copy()
    cohort = cohort[
        (pd.to_numeric(cohort["RIDAGEYR"], errors="coerce") >= min_age)
        & pd.to_numeric(cohort["KCAL"], errors="coerce").notna()
        & (pd.to_numeric(cohort["KCAL"], errors="coerce") >= energy_min)
        & (pd.to_numeric(cohort["KCAL"], errors="coerce") <= energy_max)
    ].copy()
    if cohort.empty:
        return pd.DataFrame(columns=PHDI_NHANES_RESULT_COLS)

    scored = _score_phdi140_from_components(cohort)
    chosen = "PHDI_140_RECONSTRUCTED" if score_version == "reconstructed" else "PHDI_140_LITERAL"
    scored["PHDI_ALL"] = scored[chosen]
    scored["PHDI_140"] = scored[chosen]

    demo = _load_nhanes_frame(demo_path)
    demo_cols = [c for c in demo.columns if c not in scored.columns and c != "SEQN"]
    if demo_cols:
        scored = scored.merge(demo[["SEQN"] + demo_cols], on="SEQN", how="left")

    ordered = [c for c in PHDI_NHANES_RESULT_COLS if c in scored.columns]
    rest = [c for c in scored.columns if c not in ordered]
    return scored[ordered + rest].reset_index(drop=True)


def compute_phdi_nhanes_mped(
    pyramid_path=None,
    nutrient_path=None,
    demo_path=None,
    pyramid_path2=None,
    nutrient_path2=None,
    *,
    score_version="reconstructed",
    min_age=20,
    energy_min=500,
    energy_max=8000,
):
    """Compute paper-aligned 0-140 PHDI from early NHANES Pyramid/MPED totals.

    This supports NHANES 2003-2004 ``pyr_tot_d1/d2.sas7bdat`` plus
    ``DR1TOT/DR2TOT`` files, matching the Article A reconstruction supplied
    with this project. Older 1999-2002 ``pyr_tot.sas7bdat`` and ``DRXTOT``
    files are accepted as a one-day experimental pathway when uploaded.
    """
    if pyramid_path is None or nutrient_path is None:
        raise ValueError("Day 1 Pyramid total and total nutrient files are required.")
    if demo_path is None:
        raise ValueError("DEMO file is required for PHDI NHANES scoring.")

    raw = build_phdi_nhanes_mped_components(
        pyramid_path=pyramid_path,
        nutrient_path=nutrient_path,
        demo_path=demo_path,
        pyramid_path2=pyramid_path2,
        nutrient_path2=nutrient_path2,
    )
    if raw.empty:
        return pd.DataFrame(columns=PHDI_NHANES_RESULT_COLS)

    score_version = str(score_version).lower()
    if score_version not in {"reconstructed", "literal"}:
        raise ValueError('score_version must be either "reconstructed" or "literal".')

    cohort = raw.copy()
    cohort = cohort[
        (pd.to_numeric(cohort["RIDAGEYR"], errors="coerce") >= min_age)
        & pd.to_numeric(cohort["KCAL"], errors="coerce").notna()
        & (pd.to_numeric(cohort["KCAL"], errors="coerce") >= energy_min)
        & (pd.to_numeric(cohort["KCAL"], errors="coerce") <= energy_max)
    ].copy()
    if cohort.empty:
        return pd.DataFrame(columns=PHDI_NHANES_RESULT_COLS)

    scored = _score_phdi140_from_components(cohort)
    chosen = "PHDI_140_RECONSTRUCTED" if score_version == "reconstructed" else "PHDI_140_LITERAL"
    scored["PHDI_ALL"] = scored[chosen]
    scored["PHDI_140"] = scored[chosen]

    demo = _load_nhanes_frame(demo_path)
    demo_cols = [c for c in demo.columns if c not in scored.columns and c != "SEQN"]
    if demo_cols:
        scored = scored.merge(demo[["SEQN"] + demo_cols], on="SEQN", how="left")

    ordered = [c for c in PHDI_NHANES_RESULT_COLS if c in scored.columns]
    rest = [c for c in scored.columns if c not in ordered]
    return scored[ordered + rest].reset_index(drop=True)


def compute_phdi_asa24(data_path, recall_summarize=True):
    """Compute PHDI from ASA24 Totals.csv with automatic column recognition."""
    df = _load_tabular_frame(data_path)
    if recall_summarize:
        id_col = _find_col(df, _ID_ALIASES, required=False)
        if id_col is not None:
            numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(pd.to_numeric(df[c], errors="coerce"))]
            agg = {c: "mean" for c in numeric_cols if c != id_col}
            agg[id_col] = "first"
            df = df.groupby(id_col, as_index=False).agg(agg)
    return _compute_phdi_questionnaire(df, source_label="ASA24")


def compute_phdi_dhq3(data_path):
    """Compute PHDI from DHQ3 Total Daily Results with automatic column recognition."""
    df = _load_tabular_frame(data_path)
    return _compute_phdi_questionnaire(df, source_label="DHQ3")


def compute_phdi_block(data_path):
    """Compute PHDI from BLOCK FFQ exports with automatic column recognition."""
    df = _load_tabular_frame(data_path)
    return _compute_phdi_questionnaire(df, source_label="BLOCK")


def build_phdi_nhanes_fped_components(
    fped_path=None,
    nutrient_path=None,
    demo_path=None,
    fped_path2=None,
    nutrient_path2=None,
):
    """Build NHANES-derived PHDI input components before scoring."""
    day1 = _prepare_phdi_day(fped_path, nutrient_path, demo_path)
    day2 = _prepare_phdi_day(fped_path2, nutrient_path2, None) if (fped_path2 is not None or nutrient_path2 is not None) else None
    raw = _combine_phdi_days(day1, day2)
    return _derive_phdi_components(raw)


def build_phdi_nhanes_mped_components(
    pyramid_path=None,
    nutrient_path=None,
    demo_path=None,
    pyramid_path2=None,
    nutrient_path2=None,
):
    """Build early NHANES Pyramid/MPED-derived PHDI input components."""
    day1 = _prepare_phdi_pyramid_day(pyramid_path, nutrient_path, demo_path, day_hint=1)
    day2 = (
        _prepare_phdi_pyramid_day(pyramid_path2, nutrient_path2, None, day_hint=2)
        if (pyramid_path2 is not None or nutrient_path2 is not None)
        else None
    )
    raw = _combine_phdi_days(day1, day2)
    return _derive_phdi_components(raw)


_ID_ALIASES = [
    "respondent_id", "respondent id", "respondentid", "participant_id",
    "participant id", "subject_id", "subject id", "username", "user_name",
    "user name", "seqn", "id",
]


def _norm_col_name(name):
    return re.sub(r"[^a-z0-9]+", "", str(name).lower())


def _load_tabular_frame(file_arg):
    if isinstance(file_arg, pd.DataFrame):
        return file_arg.copy()
    import os
    from io import BytesIO

    if isinstance(file_arg, (str, os.PathLike)):
        ext = os.path.splitext(str(file_arg))[1].lower()
        if ext in {".xlsx", ".xls"}:
            return pd.read_excel(file_arg)
        return pd.read_csv(file_arg, low_memory=False)
    if isinstance(file_arg, BytesIO) or hasattr(file_arg, "read"):
        if hasattr(file_arg, "seek"):
            file_arg.seek(0)
        name = getattr(file_arg, "name", "").lower()
        if name.endswith((".xlsx", ".xls")):
            return pd.read_excel(file_arg)
        return pd.read_csv(file_arg, low_memory=False)
    raise ValueError(f"Unsupported tabular file type: {type(file_arg)}")


def _find_col(df, aliases, required=False):
    norm_to_col = {_norm_col_name(c): c for c in df.columns}
    for alias in aliases:
        key = _norm_col_name(alias)
        if key in norm_to_col:
            return norm_to_col[key]
    for alias in aliases:
        key = _norm_col_name(alias)
        for norm, col in norm_to_col.items():
            if key and (key in norm or norm in key):
                return col
    if required:
        raise ValueError(f"Required column not found. Tried: {', '.join(aliases[:8])}")
    return None


def _qnum(df, aliases, default=0.0):
    col = _find_col(df, aliases, required=False)
    if col is None:
        return pd.Series(default, index=df.index, dtype=float)
    return pd.to_numeric(df[col], errors="coerce")


def _qfirst(df, aliases, default=np.nan):
    return _qnum(df, aliases, default=default)


def _qgrams(df, gram_aliases, cup_aliases=None, oz_aliases=None, cup_factor=1.0, oz_factor=28.35, default=0.0):
    col = _find_col(df, gram_aliases or [], required=False)
    if col is not None:
        return pd.to_numeric(df[col], errors="coerce")
    col = _find_col(df, cup_aliases or [], required=False)
    if col is not None:
        return pd.to_numeric(df[col], errors="coerce") * cup_factor
    col = _find_col(df, oz_aliases or [], required=False)
    if col is not None:
        return pd.to_numeric(df[col], errors="coerce") * oz_factor
    return pd.Series(default, index=df.index, dtype=float)


def _compute_phdi_questionnaire(df, source_label):
    data = df.copy()
    id_col = _find_col(data, _ID_ALIASES, required=False)
    sex_col = _find_col(data, ["riagendr", "gender", "sex", "sex 1 male 2 female", "sex 1=male 2=female"], required=False)
    if sex_col is None:
        raise ValueError(f"{source_label} PHDI requires a gender/sex column (1=male, 2=female).")

    raw = pd.DataFrame()
    raw["SEQN"] = data[id_col].values if id_col is not None else np.arange(1, len(data) + 1)
    raw["RIAGENDR"] = pd.to_numeric(data[sex_col], errors="coerce")
    raw["RIDAGEYR"] = _qfirst(data, ["ridageyr", "age", "age_years", "age years"], default=20.0)
    raw["KCAL"] = _qfirst(data, ["kcal", "energy kcal", "energy (kcal)", "calories", "total energy"], default=np.nan)

    raw["WGRAIN_DRY_G"] = _qgrams(
        data,
        ["whole grain g", "whole grains g", "wholegrain g"],
        oz_aliases=["whole grain oz", "whole grains oz", "whole grain ounce", "whole grains ounce"],
        oz_factor=16.0,
    )
    fruit_total = _qgrams(
        data,
        ["fruit g", "total fruit g"],
        cup_aliases=["fruit cup", "fruit cups", "total fruit cup", "total fruit cups"],
        cup_factor=150.0,
    )
    raw["JUICE_G"] = _qgrams(
        data,
        ["juice g", "fruit juice g"],
        cup_aliases=["juice fruit cup", "juice fruit cups", "fruit juice cup", "fruit juice cups"],
        cup_factor=245.0,
    )
    raw["FRUIT_G"] = _qgrams(
        data,
        ["whole fruit g", "non juice fruit g"],
        cup_aliases=["whole fruit cup", "whole fruit cups", "non juice fruit cup", "non juice fruit cups"],
        cup_factor=150.0,
        default=np.nan,
    )
    raw["FRUIT_G"] = raw["FRUIT_G"].where(raw["FRUIT_G"].notna(), (fruit_total - raw["JUICE_G"]).clip(lower=0.0))

    starchy = _qgrams(
        data,
        ["starchy vegetable g", "starchy vegetables g"],
        cup_aliases=["starchy vegetable cup", "starchy vegetables cup", "other starchy vegetable cups"],
        cup_factor=150.0,
    )
    legumes = _qgrams(
        data,
        ["legumes g", "nonsoy legumes g", "beans peas lentils g"],
        oz_aliases=["legumes oz", "nonsoy legumes oz", "legume oz"],
        oz_factor=28.35,
    )
    total_veg = _qgrams(
        data,
        ["vegetable g", "total vegetable g", "total vegetables g"],
        cup_aliases=["vegetable cup", "vegetable cups", "total vegetable cup", "total vegetable cups", "total vegetables cups"],
        cup_factor=150.0,
    )
    direct_veg = _qgrams(
        data,
        ["non starchy vegetable g", "nonstarchy vegetable g"],
        cup_aliases=["non starchy vegetable cup", "nonstarchy vegetable cup"],
        cup_factor=150.0,
        default=np.nan,
    )
    raw["VEG_G"] = direct_veg.where(direct_veg.notna(), (total_veg - starchy - legumes).clip(lower=0.0))
    raw["STARCHY_G"] = starchy
    raw["DAIRY_G"] = _qgrams(data, ["dairy g", "total dairy g"], cup_aliases=["dairy cup", "dairy cups", "total dairy cup"], cup_factor=245.0)
    raw["REDMEAT_G"] = _qgrams(
        data,
        ["red meat g", "red processed meat g", "red and processed meat g"],
        oz_aliases=["red meat oz", "red processed meat oz", "cured meat protein foods oz", "meat from beef pork veal lamb and game protein foods oz"],
        oz_factor=28.35,
    )
    raw["POULTRY_G"] = _qgrams(data, ["poultry g"], oz_aliases=["poultry oz", "poultry protein foods oz"], oz_factor=28.35)
    raw["EGGS_G"] = _qgrams(data, ["egg g", "eggs g"], oz_aliases=["egg oz", "eggs oz", "egg protein foods oz"], oz_factor=28.35)
    raw["FISH_G"] = _qgrams(data, ["fish g", "seafood g"], oz_aliases=["fish oz", "seafood oz", "seafood protein foods oz"], oz_factor=28.35)
    raw["LEGUMES_G"] = legumes
    raw["SOY_G"] = _qgrams(data, ["soy g", "soybean g", "soy protein g"], oz_aliases=["soy oz", "soy protein foods oz"], oz_factor=28.35)
    raw["NUTS_G"] = _qgrams(data, ["nuts g", "nuts seeds g"], oz_aliases=["nuts oz", "nuts seeds oz", "nuts seeds soy and legumes oz"], oz_factor=28.35)
    raw["ADDED_SUGAR_G"] = _qgrams(
        data,
        ["added sugar g", "added sugars g", "*added sugars g"],
        oz_aliases=[],
        default=np.nan,
    )
    tsp_added = _qnum(data, ["added sugar tsp", "added sugars tsp", "teaspoon added sugars"], default=np.nan)
    raw["ADDED_SUGAR_G"] = raw["ADDED_SUGAR_G"].where(raw["ADDED_SUGAR_G"].notna(), tsp_added * 4.2)

    sat_g = _qfirst(data, ["saturated fat g", "sat fat g", "saturated fatty acids g", "sfat"], default=np.nan)
    solid_g = _qfirst(data, ["solid fat g", "solid fats g"], default=np.nan)
    mufa = _qfirst(data, ["mono fat g", "monounsaturated fat g", "mfat", "mufa"], default=np.nan)
    pufa = _qfirst(data, ["poly fat g", "polyunsaturated fat g", "pfat", "pufa"], default=np.nan)
    oil_pct = _qfirst(data, ["oil pct energy", "unsaturated fat pct energy", "added unsaturated fats %kcal"], default=np.nan)

    with np.errstate(divide="ignore", invalid="ignore"):
        raw["SATFAT_PCT_ENERGY"] = sat_g * 9.0 / raw["KCAL"] * 100.0
        solid_pct = solid_g * 9.0 / raw["KCAL"] * 100.0
        raw["SOLIDFAT_PCT_ENERGY"] = solid_pct.where(solid_g.notna(), raw["SATFAT_PCT_ENERGY"])
        raw["OIL_PCT_ENERGY"] = oil_pct.where(oil_pct.notna(), (mufa.fillna(0.0) + pufa.fillna(0.0)) * 9.0 / raw["KCAL"] * 100.0)
        raw["SUGAR_JUICE_PCT_ENERGY"] = (raw["ADDED_SUGAR_G"].fillna(0.0) * 4.0 + raw["JUICE_G"].fillna(0.0) * 0.46) / raw["KCAL"] * 100.0

    raw["FPED_SOLID_FAT_G"] = solid_g.where(solid_g.notna(), sat_g)
    raw["KCAL_TWO_DAY"] = np.nan
    missing = [
        name for name in ["KCAL", "WGRAIN_DRY_G", "FRUIT_G", "VEG_G", "STARCHY_G", "DAIRY_G"]
        if raw[name].isna().all()
    ]
    if missing:
        raise ValueError(f"{source_label} PHDI could not identify required columns: {', '.join(missing)}.")

    scored = _score_phdi140_from_components(raw)
    scored["PHDI_ALL"] = scored["PHDI_140_RECONSTRUCTED"]
    scored["PHDI_140"] = scored["PHDI_140_RECONSTRUCTED"]
    ordered = [c for c in PHDI_NHANES_RESULT_COLS if c in scored.columns]
    rest = [c for c in scored.columns if c not in ordered]
    return scored[ordered + rest].reset_index(drop=True)


def _load_nhanes_frame(file_arg):
    df = _resolve_upload(file_arg)
    if df is None:
        raise ValueError("Cannot load NHANES file.")
    df = df.copy()
    df.columns = [str(c).upper() for c in df.columns]
    if "SEQN" not in df.columns:
        raise ValueError("NHANES file must contain SEQN.")
    df["SEQN"] = pd.to_numeric(df["SEQN"], errors="coerce")
    df = df.dropna(subset=["SEQN"]).copy()
    df["SEQN"] = df["SEQN"].astype(int)
    return df


def _detect_tot_day(df):
    for day in (1, 2):
        if any(str(col).startswith(f"DR{day}T") for col in df.columns):
            return day
    raise ValueError("Cannot detect NHANES recall day from total dietary columns.")


def _first_numeric(df, columns, default=np.nan):
    for col in columns:
        if col in df.columns:
            return _num(df, col, default=default)
    return pd.Series(default, index=df.index, dtype=float)


def _find_nutrient_col(df, day, suffix):
    candidates = [
        f"DR{day}T{suffix}",
        f"DRXT{suffix}",
        f"DRD{suffix}",
        suffix,
    ]
    for col in candidates:
        if col in df.columns:
            return col
    for col in df.columns:
        if str(col).upper().endswith(suffix):
            return col
    return None


def _num(df, col, default=np.nan):
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series(default, index=df.index, dtype=float)


def _sum_cols(df, cols):
    total = pd.Series(0.0, index=df.index, dtype=float)
    for col in cols:
        total = total + _num(df, col, default=0.0).fillna(0.0)
    return total


def _prepare_phdi_day(fped_path, nutrient_path, demo_path=None):
    if fped_path is None or nutrient_path is None:
        return None

    nutrient = _load_nhanes_frame(nutrient_path)
    fped = _load_nhanes_frame(fped_path)
    day = _detect_tot_day(nutrient)
    prefix = f"DR{day}T"

    if any(col.startswith(f"DR{day}I") for col in nutrient.columns) or any(col.startswith(f"DR{day}I") for col in fped.columns):
        raise ValueError("Use NHANES total-level files (DR1TOT/DR2TOT and FPED tot), not iff files.")

    cohort = nutrient.merge(fped, on="SEQN", how="inner", suffixes=("", "_FPED"))
    if demo_path is not None:
        demo = _load_nhanes_frame(demo_path)
        keep = ["SEQN"] + [c for c in ["RIAGENDR", "RIDAGEYR", "RIDEXPRG"] if c in demo.columns]
        cohort = cohort.merge(demo[keep], on="SEQN", how="inner")

    out = pd.DataFrame({"SEQN": cohort["SEQN"].astype(int)})
    if "RIAGENDR" in cohort.columns:
        out["RIAGENDR"] = _num(cohort, "RIAGENDR")
    if "RIDAGEYR" in cohort.columns:
        out["RIDAGEYR"] = _num(cohort, "RIDAGEYR")
    if "RIDEXPRG" in cohort.columns:
        out["RIDEXPRG"] = _num(cohort, "RIDEXPRG")

    out[f"DR{day}DRSTZ"] = _num(cohort, f"DR{day}DRSTZ")
    out[f"KCAL_D{day}"] = _num(cohort, f"{prefix}KCAL")
    out[f"SAT_FAT_G_D{day}"] = _num(cohort, f"{prefix}SFAT")
    out[f"UNSAT_FAT_G_D{day}"] = _num(cohort, f"{prefix}MFAT") + _num(cohort, f"{prefix}PFAT")
    out[f"TOTAL_SUGAR_G_D{day}"] = _num(cohort, f"{prefix}SUGR")

    fp = f"{prefix}_"
    out[f"G_TOTAL_OZ_D{day}"] = _num(cohort, fp + "G_TOTAL")
    out[f"G_WHOLE_OZ_D{day}"] = _num(cohort, fp + "G_WHOLE")
    out[f"FRUIT_CUP_D{day}"] = _sum_cols(cohort, [fp + "F_CITMLB", fp + "F_OTHER"])
    out[f"JUICE_CUP_D{day}"] = _num(cohort, fp + "F_JUICE")
    out[f"VEG_CUP_D{day}"] = (
        _num(cohort, fp + "V_TOTAL", default=0.0).fillna(0.0)
        - _num(cohort, fp + "V_STARCHY_TOTAL", default=0.0).fillna(0.0)
        - _num(cohort, fp + "V_LEGUMES", default=0.0).fillna(0.0)
    )
    out[f"STARCHY_CUP_D{day}"] = _num(cohort, fp + "V_STARCHY_TOTAL")
    out[f"DAIRY_CUP_D{day}"] = _num(cohort, fp + "D_TOTAL")
    out[f"REDMEAT_OZ_D{day}"] = _sum_cols(cohort, [fp + "PF_MEAT", fp + "PF_CUREDMEAT", fp + "PF_ORGAN"])
    out[f"POULTRY_OZ_D{day}"] = _num(cohort, fp + "PF_POULT")
    out[f"EGG_OZ_D{day}"] = _num(cohort, fp + "PF_EGGS")
    out[f"FISH_OZ_D{day}"] = _sum_cols(cohort, [fp + "PF_SEAFD_HI", fp + "PF_SEAFD_LOW"])
    out[f"NONSOY_LEGUME_OZ_D{day}"] = _num(cohort, fp + "PF_LEGUMES")
    out[f"SOY_OZ_D{day}"] = _num(cohort, fp + "PF_SOY")
    out[f"NUTS_OZ_D{day}"] = _num(cohort, fp + "PF_NUTSDS")
    out[f"FPED_OILS_D{day}"] = _num(cohort, fp + "OILS")
    out[f"FPED_SOLID_FATS_D{day}"] = _num(cohort, fp + "SOLID_FATS")
    out[f"FPED_ADD_SUGARS_TSP_D{day}"] = _num(cohort, fp + "ADD_SUGARS")
    return out


def _prepare_phdi_pyramid_day(pyramid_path, nutrient_path, demo_path=None, day_hint=1):
    if pyramid_path is None or nutrient_path is None:
        return None

    nutrient = _load_nhanes_frame(nutrient_path)
    pyramid = _load_nhanes_frame(pyramid_path)
    day = 2 if day_hint == 2 else 1

    cohort = nutrient.merge(pyramid, on="SEQN", how="inner", suffixes=("", "_PYR"))
    if demo_path is not None:
        demo = _load_nhanes_frame(demo_path)
        keep = ["SEQN"] + [c for c in ["RIAGENDR", "RIDAGEYR", "RIDEXPRG", "RIDPREG"] if c in demo.columns]
        cohort = cohort.merge(demo[keep], on="SEQN", how="inner", suffixes=("", "_DEMO"))

    out = pd.DataFrame({"SEQN": cohort["SEQN"].astype(int)})
    out["RIAGENDR"] = _first_numeric(cohort, ["RIAGENDR", "RIAGENDR_PYR", "RIAGENDR_DEMO"])
    out["RIDAGEYR"] = _first_numeric(cohort, ["RIDAGEYR", "RIDAGEYR_PYR", "RIDAGEYR_DEMO"])
    if any(c in cohort.columns for c in ["RIDEXPRG", "RIDPREG", "RIDEXPRG_DEMO", "RIDPREG_DEMO"]):
        out["RIDEXPRG"] = _first_numeric(cohort, ["RIDEXPRG", "RIDEXPRG_DEMO", "RIDPREG", "RIDPREG_DEMO"])

    status_cols = [
        f"DR{day}DRSTZ",
        f"DR{day}DRSTZ_PYR",
        "DRDDRSTZ",
        "DRDDRSTZ_PYR",
        "DRDDRSTS",
        "DRDDRSTS_PYR",
    ]
    out[f"DR{day}DRSTZ"] = _first_numeric(cohort, status_cols, default=1.0)

    kcal_col = _find_nutrient_col(cohort, day, "KCAL")
    sfat_col = _find_nutrient_col(cohort, day, "SFAT")
    mfat_col = _find_nutrient_col(cohort, day, "MFAT")
    pfat_col = _find_nutrient_col(cohort, day, "PFAT")
    sugr_col = _find_nutrient_col(cohort, day, "SUGR")

    out[f"KCAL_D{day}"] = _num(cohort, kcal_col) if kcal_col else np.nan
    out[f"SAT_FAT_G_D{day}"] = _num(cohort, sfat_col) if sfat_col else np.nan
    out[f"UNSAT_FAT_G_D{day}"] = (
        (_num(cohort, mfat_col) if mfat_col else 0.0)
        + (_num(cohort, pfat_col) if pfat_col else 0.0)
    )
    out[f"TOTAL_SUGAR_G_D{day}"] = _num(cohort, sugr_col) if sugr_col else np.nan

    out[f"G_TOTAL_OZ_D{day}"] = _num(cohort, "G_TOTAL")
    out[f"G_WHOLE_OZ_D{day}"] = _num(cohort, "G_WHL")
    out[f"FRUIT_CUP_D{day}"] = _sum_cols(cohort, ["F_CITMLB", "F_OTHER"])
    out[f"JUICE_CUP_D{day}"] = _num(cohort, "F_JUICE", default=0.0)
    out[f"VEG_CUP_D{day}"] = (
        _num(cohort, "V_TOTAL", default=0.0).fillna(0.0)
        - _num(cohort, "V_STARCY", default=0.0).fillna(0.0)
        - _num(cohort, "LEGUMES", default=0.0).fillna(0.0)
    )
    out[f"STARCHY_CUP_D{day}"] = _num(cohort, "V_STARCY")
    out[f"DAIRY_CUP_D{day}"] = _num(cohort, "D_TOTAL")
    out[f"REDMEAT_OZ_D{day}"] = _sum_cols(cohort, ["M_MEAT", "M_FRANK", "M_ORGAN"])
    out[f"POULTRY_OZ_D{day}"] = _num(cohort, "M_POULT")
    out[f"EGG_OZ_D{day}"] = _num(cohort, "M_EGG")
    out[f"FISH_OZ_D{day}"] = _sum_cols(cohort, ["M_FISH_HI", "M_FISH_LO"])
    out[f"NONSOY_LEGUME_OZ_D{day}"] = _num(cohort, "LEGUMES")
    out[f"SOY_OZ_D{day}"] = _num(cohort, "M_SOY")
    out[f"NUTS_OZ_D{day}"] = _num(cohort, "M_NUTSD")
    out[f"FPED_OILS_D{day}"] = _num(cohort, "DISCFAT_OIL")
    out[f"FPED_SOLID_FATS_D{day}"] = _num(cohort, "DISCFAT_SOL")
    out[f"FPED_ADD_SUGARS_TSP_D{day}"] = _num(cohort, "ADD_SUG")
    return out


def _combine_phdi_days(day1, day2):
    if day1 is None and day2 is None:
        raise ValueError("At least one NHANES recall day is required.")
    if day1 is None:
        return day2.copy()
    if day2 is None:
        return day1.copy()
    return day1.merge(day2, on="SEQN", how="inner", suffixes=("", "_D2JOIN"))


def _average_recall(df, base, require_two_days=False):
    v1 = _num(df, f"{base}_D1")
    v2 = _num(df, f"{base}_D2")
    s1 = _num(df, "DR1DRSTZ")
    s2 = _num(df, "DR2DRSTZ")
    both = (s1 == 1) & (s2 == 1)
    if require_two_days:
        return pd.Series(np.where(both, (v1 + v2) / 2.0, np.nan), index=df.index)
    return pd.Series(
        np.where(
            both,
            (v1 + v2) / 2.0,
            np.where(s1 == 1, v1, np.where(s2 == 1, v2, np.nan)),
        ),
        index=df.index,
    )


def _derive_phdi_components(df):
    out = df.copy()
    out["KCAL"] = _average_recall(out, "KCAL", require_two_days=False)
    out["KCAL_TWO_DAY"] = _average_recall(out, "KCAL", require_two_days=True)
    out["SAT_FAT_G"] = _average_recall(out, "SAT_FAT_G")
    out["UNSAT_FAT_G"] = _average_recall(out, "UNSAT_FAT_G")
    out["TOTAL_SUGAR_G"] = _average_recall(out, "TOTAL_SUGAR_G")
    out["WGRAIN_DRY_G"] = _average_recall(out, "G_WHOLE_OZ") * 16.0
    out["FRUIT_G"] = _average_recall(out, "FRUIT_CUP") * 150.0
    out["JUICE_G"] = _average_recall(out, "JUICE_CUP") * 245.0
    out["VEG_G"] = _average_recall(out, "VEG_CUP") * 150.0
    out["STARCHY_G"] = _average_recall(out, "STARCHY_CUP") * 150.0
    out["DAIRY_G"] = _average_recall(out, "DAIRY_CUP") * 245.0
    out["REDMEAT_G"] = _average_recall(out, "REDMEAT_OZ") * 28.35
    out["POULTRY_G"] = _average_recall(out, "POULTRY_OZ") * 28.35
    out["EGGS_G"] = _average_recall(out, "EGG_OZ") * 28.35
    out["FISH_G"] = _average_recall(out, "FISH_OZ") * 28.35
    out["LEGUMES_G"] = _average_recall(out, "NONSOY_LEGUME_OZ") * 28.35
    out["SOY_G"] = _average_recall(out, "SOY_OZ") * 28.35
    out["NUTS_G"] = _average_recall(out, "NUTS_OZ") * 28.35
    out["FPED_SOLID_FAT_G"] = _average_recall(out, "FPED_SOLID_FATS")
    out["ADDED_SUGAR_G"] = _average_recall(out, "FPED_ADD_SUGARS_TSP") * 4.2

    with np.errstate(divide="ignore", invalid="ignore"):
        out["OIL_PCT_ENERGY"] = out["UNSAT_FAT_G"] * 9.0 / out["KCAL"] * 100.0
        out["SATFAT_PCT_ENERGY"] = out["SAT_FAT_G"] * 9.0 / out["KCAL"] * 100.0
        out["SOLIDFAT_PCT_ENERGY"] = out["FPED_SOLID_FAT_G"] * 9.0 / out["KCAL"] * 100.0
        out["SUGAR_JUICE_PCT_ENERGY"] = (
            out["ADDED_SUGAR_G"] * 4.0 + out["JUICE_G"] * 0.46
        ) / out["KCAL"] * 100.0
    return out


def _clean_actual(x):
    arr = np.asarray(x, dtype=float)
    return np.where(np.isnan(arr) | (arr < 0), 0.0, arr)


def _score_adequacy(x, target, max_pts=10.0):
    x = _clean_actual(x)
    return np.minimum(max_pts, max_pts * x / target)


def _score_unhealthy_range(x, worst, best, max_pts=10.0):
    x = _clean_actual(x)
    return np.where(
        x >= worst,
        0.0,
        np.where(x <= best, max_pts, (worst - x) * max_pts / (worst - best)),
    )


def _score_optimum_range(x, peak, upper, max_pts=10.0):
    x = _clean_actual(x)
    return np.where(
        x <= 0,
        0.0,
        np.where(
            x < peak,
            x * max_pts / peak,
            np.where(x == peak, max_pts, np.where(x < upper, (upper - x) * max_pts / (upper - peak), 0.0)),
        ),
    )


def _score_phdi140_from_components(raw):
    out = raw.copy()
    female = pd.to_numeric(out["RIAGENDR"], errors="coerce") == 2
    out["PHDI_WGRAIN"] = np.where(
        female,
        _score_adequacy(out["WGRAIN_DRY_G"], 75, 10),
        _score_adequacy(out["WGRAIN_DRY_G"], 90, 10),
    )
    out["PHDI_FRUIT"] = _score_adequacy(out["FRUIT_G"], 200, 10)
    out["PHDI_VEG"] = _score_adequacy(out["VEG_G"], 300, 10)
    out["PHDI_NUTS"] = _score_adequacy(out["NUTS_G"], 50, 10)
    out["PHDI_LEGUMES"] = _score_adequacy(out["LEGUMES_G"], 100, 5)
    out["PHDI_SOY"] = _score_adequacy(out["SOY_G"], 50, 5)
    out["PHDI_OIL"] = _score_adequacy(out["OIL_PCT_ENERGY"], 10, 10)
    out["PHDI_STARCHY"] = _score_unhealthy_range(out["STARCHY_G"], 200, 50, 10)
    out["PHDI_DAIRY"] = _score_unhealthy_range(out["DAIRY_G"], 1000, 250, 10)
    out["PHDI_REDMEAT"] = _score_unhealthy_range(out["REDMEAT_G"], 300, 14, 10)
    out["PHDI_POULTRY"] = _score_unhealthy_range(out["POULTRY_G"], 58, 29, 10)
    out["PHDI_EGGS"] = _score_unhealthy_range(out["EGGS_G"], 120, 12, 10)
    out["PHDI_FISH"] = _score_unhealthy_range(out["FISH_G"], 50, 15, 10)
    out["PHDI_SATFAT"] = _score_unhealthy_range(out["SATFAT_PCT_ENERGY"], 21, 3.5, 10)
    out["PHDI_SUGAR"] = _score_unhealthy_range(out["SUGAR_JUICE_PCT_ENERGY"], 25, 5, 10)
    literal_cols = [
        "PHDI_WGRAIN", "PHDI_FRUIT", "PHDI_VEG", "PHDI_NUTS", "PHDI_LEGUMES",
        "PHDI_SOY", "PHDI_OIL", "PHDI_STARCHY", "PHDI_DAIRY", "PHDI_REDMEAT",
        "PHDI_POULTRY", "PHDI_EGGS", "PHDI_FISH", "PHDI_SATFAT", "PHDI_SUGAR",
    ]
    out["PHDI_140_LITERAL"] = out[literal_cols].sum(axis=1)

    out["PHDIR_STARCHY"] = _score_optimum_range(out["STARCHY_G"], 50, 200, 10)
    out["PHDIR_DAIRY"] = _score_optimum_range(out["DAIRY_G"], 250, 1000, 10)
    out["PHDIR_POULTRY"] = _score_optimum_range(out["POULTRY_G"], 29, 58, 10)
    out["PHDIR_EGGS"] = _score_optimum_range(out["EGGS_G"], 12, 120, 10)
    out["PHDIR_SATFAT"] = _score_unhealthy_range(out["SOLIDFAT_PCT_ENERGY"], 21, 3.5, 10)
    reconstructed_cols = [
        "PHDI_WGRAIN", "PHDI_FRUIT", "PHDI_VEG", "PHDI_NUTS", "PHDI_LEGUMES",
        "PHDI_SOY", "PHDI_OIL", "PHDIR_STARCHY", "PHDIR_DAIRY", "PHDI_REDMEAT",
        "PHDIR_POULTRY", "PHDIR_EGGS", "PHDI_FISH", "PHDIR_SATFAT", "PHDI_SUGAR",
    ]
    out["PHDI_140_RECONSTRUCTED"] = out[reconstructed_cols].sum(axis=1)
    return out
