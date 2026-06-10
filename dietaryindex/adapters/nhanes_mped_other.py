"""NHANES MPED adapters for non-DII indices (HEI2015, HEI2020, MED, DASHI, AHEI, MEDI).

NHANES 1999-2004 uses the MPED (MyPyramid Equivalents Database) format,
which differs from the 2005+ FPED format. Key differences:
  - equiv.txt: fixed-width text or .sas7bdat mapping food codes to pyramid servings
  - Nutrient columns use DRX/DRD prefix (not DR1)
  - VITD is not available
  - NUTRIENT_IND file needed for individual food processing
"""

import numpy as np
import pandas as pd

from dietaryindex.core.hei2015 import compute_hei2015
from dietaryindex.core.hei2020 import compute_hei2020
from dietaryindex.core.med import compute_med
from dietaryindex.core.dashi import compute_dashi
from dietaryindex.core.ahei import compute_ahei
from dietaryindex.core.medi import compute_medi
from dietaryindex.core.dash import compute_dash
from dietaryindex.core.di_gm import compute_di_gm

# ── equiv.txt column widths and names (MPED 1999-2004) ──────────────────────
_MPED_EQUIV_WIDTHS = [8, 1, 6] + [8] * 32
_MPED_EQUIV_COLNAMES = [
    "DRDIFDCD", "EQUIVFLAG", "MODCODE",
    "G_TOTAL", "G_WHL", "G_NWHL",
    "V_TOTAL", "V_DRKGR", "V_DPYEL", "V_POTATO",
    "V_STARCY", "V_TOMATO", "V_OTHER",
    "F_TOTAL", "F_CITMLB", "F_OTHER",
    "D_TOTAL", "D_MILK", "D_YOGURT", "D_CHEESE",
    "M_MPF", "M_MEAT", "M_ORGAN", "M_FRANK",
    "M_POULT", "M_FISH_HI", "M_FISH_LO",
    "M_EGG", "M_SOY", "M_NUTSD",
    "LEGUMES", "DISCFAT_OIL", "DISCFAT_SOL",
    "ADD_SUG", "A_BEV",
]

# Soy milk migration food codes (move from M_SOY to D_TOTAL)
_SOY_MILK_CODES = {
    11310000: 100 * (1 / 244),
    11320000: 100 * (1 / 245),
    11321000: 100 * (1 / 240),
    11330000: 100 * (1 / 245),
}

# Food codes for pizza correction
_PIZZA_CODES = {58106210, 58106220, 58106230}

# NUTRIENT column renames (DRX/DRD prefix -> DR1 prefix for consistency)
_MPED_NUTRIENT_RENAMES = {
    "DRXTKCAL": "DR1TKCAL",
    "DRXTSFAT": "DR1TSFAT",
    "DRXTALCO": "DR1TALCO",
    "DRDTSODI": "DR1TSODI",
    "DRXTMFAT": "DR1TMFAT",
    "DRXTPFAT": "DR1TPFAT",
    "DRXTTFAT": "DR1TTFAT",
    "DRXTCHOL": "DR1TCHOL",
    "DRXTPROT": "DR1TPROT",
    "DRXTFIBE": "DR1TFIBE",
    "DRXTPOTA": "DR1TPOTA",
    "DRXTMAGN": "DR1TMAGN",
    "DRXTCALC": "DR1TCALC",
    "DRXTP182": "DR1TP182",
    "DRXTP183": "DR1TP183",
    "DRXTP184": "DR1TP184",
    "DRXTP204": "DR1TP204",
    "DRXTP205": "DR1TP205",
    "DRXTP225": "DR1TP225",
    "DRXTP226": "DR1TP226",
}

# Default WJFRT
_WJFRT_DEFAULT = pd.DataFrame({
    "FOODCODE": [61201010, 61201220, 61206010, 61207000, 61208000,
                 62101020, 62102010, 64100100, 64104010, 64116010],
    "RATIO": [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 1.0, 0.0, 0.0],
})
_WJFRT_DEFAULT["WHOLEFRT"] = _WJFRT_DEFAULT["RATIO"]
_WJFRT_DEFAULT["FRTJUICE"] = 1.0 - _WJFRT_DEFAULT["RATIO"]


def _resolve_mped_upload(file_arg):
    """Load MPED file (sas7bdat, xpt, txt, csv, or DataFrame)."""
    if file_arg is None:
        return None
    if isinstance(file_arg, pd.DataFrame):
        return file_arg

    import os
    import pyreadstat
    from io import BytesIO

    if isinstance(file_arg, (str, os.PathLike)):
        path_str = str(file_arg).lower()
        if path_str.endswith(".sas7bdat"):
            return pyreadstat.read_sas7bdat(file_arg)[0]
        elif path_str.endswith(".xpt") or path_str.endswith(".xport"):
            return pyreadstat.read_xport(file_arg)[0]
        elif path_str.endswith(".txt"):
            return _load_equiv_text(file_arg)
        else:
            return pd.read_csv(file_arg)
    else:
        content = file_arg.read()
        if hasattr(file_arg, "seek"):
            file_arg.seek(0)
        fname = getattr(file_arg, "name", "").lower()
        if "sas" in fname:
            return pyreadstat.read_sas7bdat(BytesIO(content))[0]
        elif "xpt" in fname or "xport" in fname:
            return pyreadstat.read_xport(BytesIO(content))[0]
        else:
            return _load_equiv_text(BytesIO(content))


def _load_equiv_text(file_arg):
    """Load equiv.txt fixed-width text file."""
    from io import BytesIO
    if isinstance(file_arg, (str, type(None))):
        raw = open(file_arg, "r").read() if isinstance(file_arg, str) else ""
    else:
        raw = file_arg.read() if hasattr(file_arg, "read") else str(file_arg)
        if hasattr(file_arg, "seek"):
            file_arg.seek(0)

    lines = [l for l in raw.split("\n") if l.strip()]
    widths = [8, 1, 6] + [8] * 32
    colnames = _MPED_EQUIV_COLNAMES

    data = []
    for line in lines:
        row = []
        pos = 0
        for w in widths:
            field = line[pos:pos + w].strip() if pos + w <= len(line) else ""
            row.append(field)
            pos += w
        data.append(row)

    df = pd.DataFrame(data, columns=colnames)
    for c in df.columns[3:]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    df["DRDIFDCD"] = pd.to_numeric(df["DRDIFDCD"], errors="coerce")
    return df


def _process_equiv(equiv_df):
    """Process equiv dataframe: rename V_DPYEL, handle soy milk, pizza fix."""
    if equiv_df is None:
        return None

    e = equiv_df.copy()

    if "V_DPYEL" in e.columns:
        e = e.rename(columns={"V_DPYEL": "V_ORANGE"})

    if "V_TOMATO" not in e.columns:
        e["V_TOMATO"] = 0.0
    if "V_ORANGE" not in e.columns:
        e["V_ORANGE"] = 0.0

    food_col = "DRDIFDCD" if "DRDIFDCD" in e.columns else "FOODCODE"
    if food_col in e.columns:
        for code, d_val in _SOY_MILK_CODES.items():
            mask = e[food_col] == code
            if mask.any():
                e.loc[mask, "M_SOY"] = 0.0
                e.loc[mask, "D_TOTAL"] = round(d_val, 3)

    if "FOODCODE" not in e.columns:
        e["FOODCODE"] = e[food_col].astype(int)

    e["MODCODE"] = e.get("MODCODE", pd.Series("", index=e.index))

    return e


def _merge_wjfrt(equiv_df, wjfrt_df):
    """Merge WJFRT with equiv to add WHOLEFRT and FRTJUICE columns."""
    if equiv_df is None or wjfrt_df is None:
        return equiv_df

    wj = wjfrt_df.copy()

    for col_map in [("FRTJUICE", "RATIO"), ("WHOLEFRT", "RATIO")]:
        target, source = col_map
        if target not in wj.columns:
            if source in wj.columns:
                wj[target] = wj[source]
            elif "frtjuice" in wj.columns:
                wj[target] = v
                wj = wj.rename(columns={"frtjuice": "FRTJUICE", "wholefrt": "WHOLEFRT"})

    has_mod = "MODCODE" in equiv_df.columns and "MODCODE" in wj.columns
    if "MODCODE" in wj.columns:
        wj["MODCODE"] = wj["MODCODE"].astype(str)
    if "MODCODE" in equiv_df.columns:
        equiv_df["MODCODE"] = equiv_df["MODCODE"].astype(str)

    if has_mod and equiv_df["MODCODE"].notna().any():
        merged = equiv_df.merge(
            wj[["FOODCODE", "MODCODE", "WHOLEFRT", "FRTJUICE"]],
            on=["FOODCODE", "MODCODE"], how="left"
        )
    else:
        wj_cols = [c for c in ["FOODCODE", "WHOLEFRT", "FRTJUICE"] if c in wj.columns]
        merged = equiv_df.merge(wj[wj_cols], on="FOODCODE", how="left")

    for c in ["WHOLEFRT", "FRTJUICE"]:
        if c in merged.columns:
            merged[c] = merged[c].fillna(0.0)
        else:
            merged[c] = 0.0

    return merged


def _nutrient_rename(nutrient_df):
    """Rename MPED nutrient columns from DRX prefix to DR1 prefix."""
    if nutrient_df is None:
        return None
    n = nutrient_df.copy()
    for old, new in _MPED_NUTRIENT_RENAMES.items():
        if old in n.columns:
            n[new] = n[old].astype(float)
    if "DRDDRSTZ" in n.columns:
        n["DR1DRSTZ"] = n["DRDDRSTZ"]
    elif "DRDDRSTS" in n.columns:
        n["DR1DRSTZ"] = n["DRDDRSTS"]
    return n


def _process_ind_foods(nutrient_ind, equiv_processed, wjfrt_df=None):
    """Process individual food items: multiply by gram intake, group by SEQN.

    Returns a dict with per-person sum of food group servings.
    """
    if nutrient_ind is None:
        return None

    ind = nutrient_ind.copy()

    # Identify food code and gram columns
    food_col = None
    gram_col = None
    for c in ind.columns:
        if c in ("DR1IFDCD", "DRDIFDCD"):
            food_col = c
        if c in ("DR1IGRMS", "DRXIGRMS"):
            gram_col = c

    if food_col is None or gram_col is None:
        raise ValueError("NUTRIENT_IND must contain food code (DR1IFDCD/DRDIFDCD) and gram (DR1IGRMS/DRXIGRMS) columns")

    ind["FOODCODE"] = ind[food_col].astype(int)
    ind["GRAMS"] = pd.to_numeric(ind[gram_col], errors="coerce").fillna(0.0)

    # Filter reliable recall
    if "DR1DRSTZ" in ind.columns:
        ind = ind[ind["DR1DRSTZ"] == 1].copy()

    if equiv_processed is None:
        return None

    eq = equiv_processed.copy()
    join_keys = ["FOODCODE"]
    if "MODCODE" in ind.columns and "MODCODE" in eq.columns:
        ind["MODCODE"] = ind["MODCODE"].astype(str)
        eq["MODCODE"] = eq["MODCODE"].astype(str)
        join_keys = ["FOODCODE", "MODCODE"]

    # Get the food group columns from equiv
    eq_cols = join_keys + [c for c in [
        "WHOLEFRT", "FRTJUICE",
        "G_TOTAL", "G_WHL", "G_NWHL",
        "V_TOTAL", "V_DRKGR", "V_ORANGE", "V_POTATO",
        "V_STARCY", "V_TOMATO", "V_OTHER",
        "F_TOTAL", "F_CITMLB", "F_OTHER",
        "D_TOTAL", "D_MILK", "D_YOGURT", "D_CHEESE",
        "M_MPF", "M_MEAT", "M_ORGAN", "M_FRANK",
        "M_POULT", "M_FISH_HI", "M_FISH_LO",
        "M_EGG", "M_SOY", "M_NUTSD",
        "LEGUMES", "DISCFAT_OIL", "DISCFAT_SOL",
        "ADD_SUG", "A_BEV",
    ] if c in eq.columns]

    merged = ind[["SEQN", "FOODCODE", "GRAMS"] + (["MODCODE"] if "MODCODE" in join_keys else [])].merge(
        eq[eq_cols], on=join_keys, how="left"
    ).fillna(0.0)

    per100_cols = [c for c in eq_cols if c not in join_keys]
    for c in per100_cols:
        merged[c] = merged[c] * merged["GRAMS"] / 100.0

    grp = merged.groupby("SEQN", as_index=False)[per100_cols].sum()

    result = {"SEQN": grp["SEQN"].values}
    for c in per100_cols:
        result[c] = grp[c].values

    n_df = pd.DataFrame(result)

    # For indices needing nutrient totals, get from nutrient_ind
    nut_cols = {}
    for ncol in ind.columns:
        if ncol in ("DR1ISODI", "DRXISODI"):
            nut_cols["SODIUM"] = ind[ncol].values
        if ncol in ("DR1IALCO", "DRXIALCO"):
            nut_cols["ALCOHOL"] = ind[ncol].values
        if ncol in ("DR1IKCAL", "DRXIKCAL"):
            nut_cols["TOTALKCAL"] = ind[ncol].values

    if nut_cols:
        nut_grp = ind[["SEQN"]].copy()
        for name, vals in nut_cols.items():
            nut_grp[name] = pd.to_numeric(vals, errors="coerce").fillna(0.0)
        nut_sum = nut_grp.groupby("SEQN", as_index=False).sum()
        for name in nut_cols:
            n_df[name] = nut_sum[name].values

    return n_df


def _merge_day1_day2(day1, day2):
    """Merge Day1 and Day2 by averaging index score columns."""
    if day2 is None:
        return day1

    merged = pd.concat([day1, day2], ignore_index=True)
    param_cols = [c for c in merged.columns if c != "SEQN"]
    return merged.groupby("SEQN", as_index=False)[param_cols].mean()


def _merge_demo(result, demo_path):
    """Merge DEMO data into result DataFrame."""
    if demo_path is None:
        return result, None

    demo = _resolve_mped_upload(demo_path)
    if demo is None:
        return result, None

    demo["SEQN"] = demo["SEQN"].astype(int)
    demo_cols = [c for c in demo.columns if c not in result.columns and c != "SEQN"]
    if demo_cols:
        result = result.merge(demo[["SEQN"] + demo_cols], on="SEQN", how="left")

    return result, demo


# ── Public adapter functions ────────────────────────────────────────────────


def compute_hei2015_nhanes_mped(
    mped_per_100_gram_path=None,
    wjfrt=None,
    nutrient_path=None,
    nutrient_ind_path=None,
    demo_path=None,
    nutrient_path2=None,
    nutrient_ind_path2=None,
):
    """Compute HEI2015 from NHANES MPED data (1999-2004)."""
    equiv = _resolve_mped_upload(mped_per_100_gram_path)
    equiv = _process_equiv(equiv)

    if wjfrt is None:
        wjfrt = _WJFRT_DEFAULT
    elif not isinstance(wjfrt, pd.DataFrame):
        wjfrt = _resolve_mped_upload(wjfrt)

    equiv = _merge_wjfrt(equiv, wjfrt)

    nutrient = _resolve_mped_upload(nutrient_path)
    nutrient = _nutrient_rename(nutrient)

    def _process_day(nt_ind_path):
        nt_ind = _resolve_mped_upload(nt_ind_path)
        nt_ind = _nutrient_rename(nt_ind)
        return _process_ind_foods(nt_ind, equiv, wjfrt)

    day1 = _process_day(nutrient_ind_path)
    day2 = _process_day(nutrient_ind_path2) if nutrient_ind_path2 is not None else None
    merged = _merge_day1_day2(day1, day2)

    if merged is None:
        raise ValueError("No data after processing")

    # Get nutrient totals per person
    if nutrient_ind_path is not None:
        nut = _resolve_mped_upload(nutrient_ind_path)
        nut = _nutrient_rename(nut)
    else:
        nut = nutrient

    result = compute_hei2015(
        data=merged,
        respondent_id=merged["SEQN"].values,
        total_kcal=merged.get("TOTALKCAL", pd.Series(0, index=merged.index)).values,
        total_fruit=merged.get("F_TOTAL", pd.Series(0, index=merged.index)).values,
        whole_fruit=merged.get("WHOLEFRT", pd.Series(0, index=merged.index)).values,
        total_vegetable=(merged.get("V_TOTAL", pd.Series(0, index=merged.index)).fillna(0)
                         + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0)).values,
        green_and_bean=(merged.get("V_DRKGR", pd.Series(0, index=merged.index)).fillna(0)
                        + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0)).values,
        total_protein=(merged.get("M_MPF", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("M_EGG", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("M_NUTSD", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("M_SOY", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0) * 4).values,
        seafood_plant_protein=(merged.get("M_FISH_HI", pd.Series(0, index=merged.index)).fillna(0)
                               + merged.get("M_FISH_LO", pd.Series(0, index=merged.index)).fillna(0)
                               + merged.get("M_NUTSD", pd.Series(0, index=merged.index)).fillna(0)
                               + merged.get("M_SOY", pd.Series(0, index=merged.index)).fillna(0)
                               + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0) * 4).values,
        whole_grain=merged.get("G_WHL", pd.Series(0, index=merged.index)).values,
        dairy=merged.get("D_TOTAL", pd.Series(0, index=merged.index)).values,
        fatty_acid=_safe_ratio(
            merged.get("MUFA", pd.Series(np.nan, index=merged.index)),
            merged.get("PUFA", pd.Series(np.nan, index=merged.index)),
            merged.get("SATFAT", pd.Series(np.nan, index=merged.index)),
        ),
        refined_grain=merged.get("G_NWHL", pd.Series(0, index=merged.index)).values,
        sodium=_safe_val(merged.get("SODIUM", pd.Series(1000, index=merged.index))) / 1000.0,
        added_sugar=_safe_val(merged.get("ADD_SUG", pd.Series(0, index=merged.index))) * 4 * 4
            / _safe_kcal(merged.get("TOTALKCAL", pd.Series(2000, index=merged.index))) * 100,
        saturated_fat=_safe_val(merged.get("SATFAT", pd.Series(10, index=merged.index))) * 9.0
            / _safe_kcal(merged.get("TOTALKCAL", pd.Series(2000, index=merged.index))) * 100,
    )

    result["SEQN"] = merged["SEQN"].values
    result, _ = _merge_demo(result, demo_path)
    return result


def compute_hei2020_nhanes_mped(
    mped_per_100_gram_path=None,
    wjfrt=None,
    nutrient_path=None,
    nutrient_ind_path=None,
    demo_path=None,
    nutrient_path2=None,
    nutrient_ind_path2=None,
):
    """Compute HEI2020 from NHANES MPED data (1999-2004)."""
    equiv = _resolve_mped_upload(mped_per_100_gram_path)
    equiv = _process_equiv(equiv)

    if wjfrt is None:
        wjfrt = _WJFRT_DEFAULT
    elif not isinstance(wjfrt, pd.DataFrame):
        wjfrt = _resolve_mped_upload(wjfrt)

    equiv = _merge_wjfrt(equiv, wjfrt)

    def _process_day(nt_ind_path):
        nt_ind = _resolve_mped_upload(nt_ind_path)
        nt_ind = _nutrient_rename(nt_ind)
        return _process_ind_foods(nt_ind, equiv, wjfrt)

    day1 = _process_day(nutrient_ind_path)
    day2 = _process_day(nutrient_ind_path2) if nutrient_ind_path2 is not None else None
    merged = _merge_day1_day2(day1, day2)

    if merged is None:
        raise ValueError("No data after processing")

    # Get age for toddler detection
    age = None
    demo_df = None
    if demo_path is not None:
        demo_df = _resolve_mped_upload(demo_path)
        if demo_df is not None:
            demo_df["SEQN"] = demo_df["SEQN"].astype(int)
            if "RIDAGEYR" in demo_df.columns:
                age_map = dict(zip(demo_df["SEQN"], demo_df["RIDAGEYR"]))
                age = pd.Series([age_map.get(s, 2.0) for s in merged["SEQN"].values])
    if age is None:
        age = pd.Series(2.0, index=merged.index)

    result = compute_hei2020(
        data=merged,
        respondent_id=merged["SEQN"].values,
        age=age.values if hasattr(age, "values") else age,
        total_kcal=_safe_kcal(merged.get("TOTALKCAL", pd.Series(0, index=merged.index))),
        total_fruit=merged.get("F_TOTAL", pd.Series(0, index=merged.index)).values,
        whole_fruit=merged.get("WHOLEFRT", pd.Series(0, index=merged.index)).values,
        total_vegetable=(merged.get("V_TOTAL", pd.Series(0, index=merged.index)).fillna(0)
                         + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0)).values,
        green_and_bean=(merged.get("V_DRKGR", pd.Series(0, index=merged.index)).fillna(0)
                        + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0)).values,
        total_protein=(merged.get("M_MPF", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("M_EGG", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("M_NUTSD", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("M_SOY", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0) * 4).values,
        seafood_plant_protein=(merged.get("M_FISH_HI", pd.Series(0, index=merged.index)).fillna(0)
                               + merged.get("M_FISH_LO", pd.Series(0, index=merged.index)).fillna(0)
                               + merged.get("M_NUTSD", pd.Series(0, index=merged.index)).fillna(0)
                               + merged.get("M_SOY", pd.Series(0, index=merged.index)).fillna(0)
                               + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0) * 4).values,
        whole_grain=merged.get("G_WHL", pd.Series(0, index=merged.index)).values,
        dairy=merged.get("D_TOTAL", pd.Series(0, index=merged.index)).values,
        fatty_acid=_safe_ratio(
            merged.get("MUFA", pd.Series(np.nan, index=merged.index)),
            merged.get("PUFA", pd.Series(np.nan, index=merged.index)),
            merged.get("SATFAT", pd.Series(np.nan, index=merged.index)),
        ),
        refined_grain=merged.get("G_NWHL", pd.Series(0, index=merged.index)).values,
        sodium=_safe_val(merged.get("SODIUM", pd.Series(1000, index=merged.index))) / 1000.0,
        added_sugar=_safe_val(merged.get("ADD_SUG", pd.Series(0, index=merged.index))) * 4 * 4
            / _safe_kcal(merged.get("TOTALKCAL", pd.Series(2000, index=merged.index))) * 100,
        saturated_fat=_safe_val(merged.get("SATFAT", pd.Series(10, index=merged.index))) * 9.0
            / _safe_kcal(merged.get("TOTALKCAL", pd.Series(2000, index=merged.index))) * 100,
    )

    result["SEQN"] = merged["SEQN"].values
    result["RIDAGEYR"] = age.values if hasattr(age, "values") else age
    result, _ = _merge_demo(result, demo_path)
    return result


def compute_med_nhanes_mped(
    mped_per_100_gram_path=None,
    wjfrt=None,
    nutrient_path=None,
    nutrient_ind_path=None,
    demo_path=None,
    nutrient_path2=None,
    nutrient_ind_path2=None,
):
    """Compute MED from NHANES MPED data (1999-2004)."""
    equiv = _resolve_mped_upload(mped_per_100_gram_path)
    equiv = _process_equiv(equiv)

    if wjfrt is None:
        wjfrt = _WJFRT_DEFAULT
    elif not isinstance(wjfrt, pd.DataFrame):
        wjfrt = _resolve_mped_upload(wjfrt)

    equiv = _merge_wjfrt(equiv, wjfrt)

    def _process_day(nt_ind_path):
        nt_ind = _resolve_mped_upload(nt_ind_path)
        nt_ind = _nutrient_rename(nt_ind)
        return _process_ind_foods(nt_ind, equiv, wjfrt)

    day1 = _process_day(nutrient_ind_path)
    day2 = _process_day(nutrient_ind_path2) if nutrient_ind_path2 is not None else None
    merged = _merge_day1_day2(day1, day2)

    if merged is None:
        raise ValueError("No data after processing")

    result = compute_med(
        data=merged,
        respondent_id=merged["SEQN"].values,
        fruit_fruit_juice=merged.get("F_TOTAL", pd.Series(0, index=merged.index)).values,
        vegetable=(
            merged.get("V_DRKGR", pd.Series(0, index=merged.index)).fillna(0)
            + (merged.get("V_ORANGE", pd.Series(0, index=merged.index)).fillna(0) / 0.5)
            + (merged.get("V_TOMATO", pd.Series(0, index=merged.index)).fillna(0) / 0.5)
            + (merged.get("V_OTHER", pd.Series(0, index=merged.index)).fillna(0) / 0.5)
            + (merged.get("V_STARCY", pd.Series(0, index=merged.index)).fillna(0) / 0.5)
        ).values,
        whole_grain=merged.get("G_WHL", pd.Series(0, index=merged.index)).values,
        legumes=(merged.get("M_SOY", pd.Series(0, index=merged.index)).fillna(0)
                 + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0) * 4).values,
        nuts=merged.get("M_NUTSD", pd.Series(0, index=merged.index)).values,
        fish=(merged.get("M_FISH_HI", pd.Series(0, index=merged.index)).fillna(0)
              + merged.get("M_FISH_LO", pd.Series(0, index=merged.index)).fillna(0)).values,
        red_processed_meat=(
            merged.get("M_FRANK", pd.Series(0, index=merged.index)).fillna(0) / 1.5
            + (merged.get("M_MEAT", pd.Series(0, index=merged.index)).fillna(0) / 4)
            + (merged.get("M_ORGAN", pd.Series(0, index=merged.index)).fillna(0) / 4)
        ).values,
        mon_sat_fat_ratio=_safe_div(
            merged.get("MUFA", pd.Series(0, index=merged.index)),
            merged.get("SATFAT", pd.Series(1, index=merged.index)),
        ),
        alcohol=merged.get("ALCOHOL", pd.Series(0, index=merged.index)).values,
    )

    result["SEQN"] = merged["SEQN"].values
    result, _ = _merge_demo(result, demo_path)
    return result


def compute_dashi_nhanes_mped(
    nutrient_path=None,
    nutrient_path2=None,
    demo_path=None,
):
    """Compute DASHI from NHANES MPED nutrient data (1999-2004)."""
    nut1 = _resolve_mped_upload(nutrient_path) if nutrient_path is not None else None
    nut2 = _resolve_mped_upload(nutrient_path2) if nutrient_path2 is not None else None

    if nut1 is None:
        raise ValueError("NUTRIENT_PATH is required")

    def _prep_nut(n):
        n = _nutrient_rename(n)
        n["SEQN"] = n["SEQN"].astype(int)
        return n

    nut1 = _prep_nut(nut1)
    if nut2 is not None:
        nut2 = _prep_nut(nut2)
        all_nut = pd.concat([nut1, nut2], ignore_index=True)
        pcols = [c for c in all_nut.columns if c != "SEQN"]
        merged = all_nut.groupby("SEQN", as_index=False)[pcols].mean()
    else:
        merged = nut1

    result = compute_dashi(
        data=merged,
        respondent_id=merged["SEQN"].values,
        total_kcal=merged.get("DR1TKCAL", pd.Series(2000, index=merged.index)).values,
        total_fat_pct=(
            merged.get("DR1TTFAT", pd.Series(0, index=merged.index)) * 9.0
            / merged["DR1TKCAL"].replace(0, 2000) * 100
        ).values,
        sat_fat_pct=(
            merged.get("DR1TSFAT", pd.Series(0, index=merged.index)) * 9.0
            / merged["DR1TKCAL"].replace(0, 2000) * 100
        ).values,
        protein_pct=(
            merged.get("DR1TPROT", pd.Series(0, index=merged.index)) * 4.0
            / merged["DR1TKCAL"].replace(0, 2000) * 100
        ).values,
        cholesterol=(
            merged.get("DR1TCHOL", pd.Series(0, index=merged.index))
            / (merged["DR1TKCAL"].replace(0, 2000) / 2000)
        ).values,
        fiber=(
            merged.get("DR1TFIBE", pd.Series(0, index=merged.index))
            / (merged["DR1TKCAL"].replace(0, 2000) / 2000)
        ).values,
        potassium=(
            merged.get("DR1TPOTA", pd.Series(0, index=merged.index))
            / (merged["DR1TKCAL"].replace(0, 2000) / 2000)
        ).values,
        magnesium=(
            merged.get("DR1TMAGN", pd.Series(0, index=merged.index))
            / (merged["DR1TKCAL"].replace(0, 2000) / 2000)
        ).values,
        calcium=(
            merged.get("DR1TCALC", pd.Series(0, index=merged.index))
            / (merged["DR1TKCAL"].replace(0, 2000) / 2000)
        ).values,
        sodium=(
            merged.get("DR1TSODI", pd.Series(0, index=merged.index))
            / (merged["DR1TKCAL"].replace(0, 2000) / 2000)
        ).values,
    )

    result["SEQN"] = merged["SEQN"].values
    result, _ = _merge_demo(result, demo_path)
    return result


def compute_ahei_nhanes_mped(
    mped_per_100_gram_path=None,
    wjfrt=None,
    nutrient_path=None,
    nutrient_ind_path=None,
    demo_path=None,
    nutrient_path2=None,
    nutrient_ind_path2=None,
    ssb_code=None,
):
    """Compute AHEI from NHANES MPED data (1999-2004).

    Requires DEMO for gender (RIAGENDR).
    """
    from dietaryindex.adapters.nhanes_fped_ind import _SSB_CODES_DEFAULT

    if ssb_code is None:
        ssb_code = _SSB_CODES_DEFAULT

    equiv = _resolve_mped_upload(mped_per_100_gram_path)
    equiv = _process_equiv(equiv)

    if wjfrt is None:
        wjfrt = _WJFRT_DEFAULT
    elif not isinstance(wjfrt, pd.DataFrame):
        wjfrt = _resolve_mped_upload(wjfrt)

    equiv = _merge_wjfrt(equiv, wjfrt)

    def _process_day(nt_ind_path, add_ssb=False):
        nt_ind = _resolve_mped_upload(nt_ind_path)
        nt_ind = _nutrient_rename(nt_ind)
        result = _process_ind_foods(nt_ind, equiv, wjfrt)
        if result is not None and add_ssb and "FOODCODE" in nt_ind.columns:
            # Compute SSB added sugar
            ssb_mask = nt_ind["FOODCODE"].isin(ssb_code) if "FOODCODE" in nt_ind.columns else pd.Series(False, index=nt_ind.index)
            if ssb_mask.any():
                ssb_df = nt_ind[ssb_mask].copy()
                ssb_df = ssb_df.merge(equiv[["FOODCODE", "ADD_SUG"]], on="FOODCODE", how="left")
                ssb_df["ADDED_SUGAR_SSB"] = ssb_df["ADD_SUG"].fillna(0) * ssb_df.get("DR1IGRMS", ssb_df.get("DRXIGRMS", 0)).fillna(0) / 100
                ssb_sum = ssb_df.groupby("SEQN", as_index=False)["ADDED_SUGAR_SSB"].sum()
                result = result.merge(ssb_sum, on="SEQN", how="left").fillna(0)
            else:
                result["ADDED_SUGAR_SSB"] = 0.0

        # Add PUFA fatty acids from nutrient_ind
        if result is not None:
            fa_cols = {}
            for c in nt_ind.columns:
                if c in ("DR1TP182", "DR1TP183", "DR1TP184", "DR1TP204", "DR1TP205", "DR1TP225", "DR1TP226"):
                    fa_cols[c] = nt_ind[c].values
            if fa_cols:
                fa_df = nt_ind[["SEQN"]].copy()
                for name, vals in fa_cols.items():
                    fa_df[name] = pd.to_numeric(vals, errors="coerce").fillna(0.0)
                fa_sum = fa_df.groupby("SEQN", as_index=False).sum()
                for c in fa_cols:
                    result[c] = fa_sum[c].values
        return result

    day1 = _process_day(nutrient_ind_path, add_ssb=True)
    day2 = _process_day(nutrient_ind_path2, add_ssb=True) if nutrient_ind_path2 is not None else None
    merged = _merge_day1_day2(day1, day2)

    if merged is None:
        raise ValueError("No data after processing")

    # Get gender from DEMO
    gender = pd.Series(2, index=merged.index)
    demo_df = None
    if demo_path is not None:
        demo_df = _resolve_mped_upload(demo_path)
        if demo_df is not None:
            demo_df["SEQN"] = demo_df["SEQN"].astype(int)
            if "RIAGENDR" in demo_df.columns:
                gmap = dict(zip(demo_df["SEQN"], demo_df["RIAGENDR"]))
                gender = pd.Series([gmap.get(s, 2) for s in merged["SEQN"].values])

    kcal = _safe_kcal(merged.get("TOTALKCAL", pd.Series(2000, index=merged.index)))

    pufa_pct = np.zeros(len(merged))
    fa_bases = ["DR1TP182", "DR1TP183", "DR1TP184", "DR1TP204", "DR1TP225"]
    for fa in fa_bases:
        if fa in merged.columns:
            pufa_pct += merged[fa].fillna(0).values * 9.0 / kcal * 100

    n3fat = np.zeros(len(merged))
    for fa in ["DR1TP205", "DR1TP226"]:
        if fa in merged.columns:
            n3fat += merged[fa].fillna(0).values * 1000

    ssb_servings = np.zeros(len(merged))
    if "ADDED_SUGAR_SSB" in merged.columns:
        ssb_servings = merged["ADDED_SUGAR_SSB"].fillna(0).values * 4 / 26

    result = compute_ahei(
        data=merged,
        respondent_id=merged["SEQN"].values,
        gender=gender.values,
        total_kcal=kcal,
        vegetable=(
            merged.get("V_DRKGR", pd.Series(0, index=merged.index)).fillna(0)
            + (merged.get("V_ORANGE", pd.Series(0, index=merged.index)).fillna(0) / 0.5)
            + (merged.get("V_TOMATO", pd.Series(0, index=merged.index)).fillna(0) / 0.5)
            + (merged.get("V_OTHER", pd.Series(0, index=merged.index)).fillna(0) / 0.5)
            + (merged.get("V_STARCY", pd.Series(0, index=merged.index)).fillna(0) / 0.5)
        ).values,
        fruit=merged.get("WHOLEFRT", pd.Series(0, index=merged.index)).values,
        whole_grain=merged.get("G_WHL", pd.Series(0, index=merged.index)).values / 0.035274,
        nut_legume=(merged.get("M_NUTSD", pd.Series(0, index=merged.index)).fillna(0)
                    + merged.get("M_SOY", pd.Series(0, index=merged.index)).fillna(0)
                    + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0) * 4).values,
        n3_fat=n3fat,
        pufa=pufa_pct,
        ssb_fruit_juice=ssb_servings,
        red_processed_meat=(
            merged.get("M_FRANK", pd.Series(0, index=merged.index)).fillna(0) / 1.5
            + (merged.get("M_MEAT", pd.Series(0, index=merged.index)).fillna(0) / 4)
            + (merged.get("M_ORGAN", pd.Series(0, index=merged.index)).fillna(0) / 4)
        ).values,
        trans_fat=pd.Series(np.nan, index=merged.index).values,
        sodium=_safe_val(merged.get("SODIUM", pd.Series(1000, index=merged.index)))
            / (kcal / 2000),
        alcohol=merged.get("A_BEV", pd.Series(0, index=merged.index)).values,
    )

    result["SEQN"] = merged["SEQN"].values
    result, _ = _merge_demo(result, demo_path)
    return result


def compute_medi_nhanes_mped(
    mped_per_100_gram_path=None,
    wjfrt=None,
    nutrient_path=None,
    nutrient_ind_path=None,
    demo_path=None,
    nutrient_path2=None,
    nutrient_ind_path2=None,
    olive_oil_code=None,
    sweets_code=None,
    fat_oil_code=None,
    ssb_code=None,
    version="v1",
):
    """Compute MEDI from NHANES MPED data (1999-2004)."""
    from dietaryindex.adapters.nhanes_fped_ind import (
        _OLIVE_OIL_CODES_DEFAULT, _SWEETS_CODES_DEFAULT,
        _FAT_OIL_CODES_DEFAULT, _SSB_CODES_DEFAULT,
    )

    if olive_oil_code is None:
        olive_oil_code = _OLIVE_OIL_CODES_DEFAULT
    if sweets_code is None:
        sweets_code = _SWEETS_CODES_DEFAULT
    if fat_oil_code is None:
        fat_oil_code = _FAT_OIL_CODES_DEFAULT
    if ssb_code is None:
        ssb_code = _SSB_CODES_DEFAULT

    equiv = _resolve_mped_upload(mped_per_100_gram_path)
    equiv = _process_equiv(equiv)

    if wjfrt is None:
        wjfrt = _WJFRT_DEFAULT
    elif not isinstance(wjfrt, pd.DataFrame):
        wjfrt = _resolve_mped_upload(wjfrt)

    equiv = _merge_wjfrt(equiv, wjfrt)

    def _process_day(nt_ind_path):
        nt_ind = _resolve_mped_upload(nt_ind_path)
        nt_ind = _nutrient_rename(nt_ind)
        result = _process_ind_foods(nt_ind, equiv, wjfrt)
        if result is None:
            return None

        # Compute special food servings
        gram_col = "DR1IGRMS" if "DR1IGRMS" in nt_ind.columns else "DRXIGRMS"
        food_col = "FOODCODE"
        if food_col not in nt_ind.columns:
            if "DR1IFDCD" in nt_ind.columns:
                nt_ind["FOODCODE"] = nt_ind["DR1IFDCD"].astype(int)
            elif "DRDIFDCD" in nt_ind.columns:
                nt_ind["FOODCODE"] = nt_ind["DRDIFDCD"].astype(int)

        grams = pd.to_numeric(nt_ind[gram_col], errors="coerce").fillna(0) if gram_col in nt_ind.columns else 0

        for name, codes, divisor in [
            ("OLIVE_OIL_SERV", olive_oil_code, 10),
            ("SWEETS_SERV", sweets_code, 50),
            ("FAT_OIL_SERV", fat_oil_code, 10),
        ]:
            mask = nt_ind[food_col].isin(codes) if food_col in nt_ind.columns else pd.Series(False, index=nt_ind.index)
            nt_ind[f"_{name}"] = np.where(mask, grams / divisor, 0.0)
            spec = nt_ind[mask].groupby("SEQN", as_index=False)[f"_{name}"].sum()
            result = result.merge(spec, on="SEQN", how="left").fillna(0) if not spec.empty else result
            if f"_{name}" not in result.columns:
                result[f"_{name}"] = 0.0

        # SSB added sugar
        ssb_mask = nt_ind[food_col].isin(ssb_code) if food_col in nt_ind.columns else pd.Series(False, index=nt_ind.index)
        if ssb_mask.any() and "ADD_SUG" in equiv.columns:
            ssb_df = nt_ind[ssb_mask].copy()
            ssb_df = ssb_df.merge(equiv[["FOODCODE", "ADD_SUG"]], on="FOODCODE", how="left")
            ssb_df["_SSB_ADD_SUG"] = ssb_df["ADD_SUG"].fillna(0) * grams[ssb_mask].values / 100
            ssb_sum = ssb_df.groupby("SEQN", as_index=False)["_SSB_ADD_SUG"].sum()
            result = result.merge(ssb_sum, on="SEQN", how="left").fillna(0)
            result["ADDED_SUGAR_SSB"] = result.get("_SSB_ADD_SUG", 0.0)
        else:
            result["ADDED_SUGAR_SSB"] = result.get("_SSB_ADD_SUG", 0.0)

        return result

    day1 = _process_day(nutrient_ind_path)
    day2 = _process_day(nutrient_ind_path2) if nutrient_ind_path2 is not None else None
    merged = _merge_day1_day2(day1, day2)

    if merged is None:
        raise ValueError("No data after processing")

    if version.lower() == "v2":
        from dietaryindex.core.medi import compute_medi_v2
        medi_fn = compute_medi_v2
    else:
        medi_fn = compute_medi

    result = medi_fn(
        data=merged,
        respondent_id=merged["SEQN"].values,
        olive_oil=merged.get("OLIVE_OIL_SERV", pd.Series(0, index=merged.index)).values,
        fruit=merged.get("WHOLEFRT", pd.Series(0, index=merged.index)).values,
        vegetable=(merged.get("V_DRKGR", pd.Series(0, index=merged.index)).fillna(0) / 2
                   + merged.get("V_ORANGE", pd.Series(0, index=merged.index)).fillna(0)
                   + merged.get("V_TOMATO", pd.Series(0, index=merged.index)).fillna(0)
                   + merged.get("V_OTHER", pd.Series(0, index=merged.index)).fillna(0)
                   + merged.get("V_STARCY", pd.Series(0, index=merged.index)).fillna(0)).values,
        legumes=((merged.get("M_SOY", pd.Series(0, index=merged.index)).fillna(0)
                  + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0) * 4) / 1.5).values,
        nuts=merged.get("M_NUTSD", pd.Series(0, index=merged.index)).values,
        fish_seafood=((merged.get("M_FISH_HI", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("M_FISH_LO", pd.Series(0, index=merged.index)).fillna(0)) / 4).values,
        alcohol=merged.get("A_BEV", pd.Series(0, index=merged.index)).values,
        ssb=(merged.get("ADDED_SUGAR_SSB", pd.Series(0, index=merged.index)) * 4 / 26).values,
        sweets=merged.get("SWEETS_SERV", pd.Series(0, index=merged.index)).values,
        discret_fat=merged.get("FAT_OIL_SERV", pd.Series(0, index=merged.index)).values,
        red_processed_meat=((merged.get("M_FRANK", pd.Series(0, index=merged.index)).fillna(0)
                              + merged.get("M_MEAT", pd.Series(0, index=merged.index)).fillna(0)
                              + merged.get("M_ORGAN", pd.Series(0, index=merged.index)).fillna(0)) / 5).values,
    )

    result["SEQN"] = merged["SEQN"].values
    result, _ = _merge_demo(result, demo_path)
    return result


# ── Utility helpers ────────────────────────────────────────────────────────

def _safe_val(series):
    return np.asarray(series, dtype=float)

def _safe_kcal(series):
    vals = np.asarray(series, dtype=float)
    return np.where(vals > 0, vals, 2000.0)

def _safe_ratio(pufa_series, mufa_series, sfa_series):
    p = np.asarray(pufa_series, dtype=float)
    m = np.asarray(mufa_series, dtype=float)
    s = np.asarray(sfa_series, dtype=float)
    denom = np.where(s > 0, s, np.nan)
    return (m + p) / denom

def _safe_div(num, denom):
    n = np.asarray(num, dtype=float)
    d = np.asarray(denom, dtype=float)
    return np.where(d > 0, n / d, 0.0)


# ── DASH NHANES MPED ────────────────────────────────────────────────────────

# FNDDS 17-18 SSB codes for DASH MPED
_DASH_MPED_SSB_CODES = [
    11511100, 11511200, 11511300, 11511400, 11511550, 11511600, 11511610,
    11511700, 11512010, 11512020, 11512030, 11512100, 11512110, 11512120,
    11553130, 11560000, 64134030, 67260000, 75200700, 91301130,
    12200100, 12210200, 12210210, 12210260, 12210270, 12210280, 12210310,
    12210400, 12210420, 12210430, 12210440, 12210505, 12210520,
    53246000,
    91703600,
    92100000, 92100500, 92101000, 92101500, 92101600, 92101610, 92101630,
    92101700, 92101800, 92101810, 92101820, 92101850, 92101851,
    92101900, 92101901, 92101903, 92101904, 92101905, 92101906,
    92101910, 92101911, 92101913, 92101917, 92101918, 92101919,
    92101920, 92101921, 92101923, 92101925, 92101926, 92101928,
    92101930, 92101931, 92101933, 92101935, 92101936, 92101938,
    92101950, 92101955, 92101960, 92101965, 92101970, 92101975,
    92102000, 92102010, 92102020, 92102030, 92102040, 92102050,
    92102060, 92102070, 92102080, 92102090, 92102100, 92102110,
    92102400, 92102401, 92102450,
    92102500, 92102501, 92102502, 92102503, 92102504, 92102505,
    92102510, 92102511, 92102512, 92102513, 92102514, 92102515,
    92102600, 92102601, 92102602, 92102610, 92102611, 92102612,
    92103000, 92104000, 92111000, 92111010, 92114000,
    92121000, 92121001, 92121010, 92121020, 92121030, 92121040, 92121041, 92121050,
    92130000, 92130001, 92130005, 92130006, 92130010, 92130011,
    92130020, 92130021, 92130030, 92130031,
    92152000, 92152010,
    92161000, 92161001, 92161002,
    92162000, 92162001, 92162002,
    92171000, 92171010,
    92191100, 92191105, 92191200, 92191400,
    92192000, 92192030, 92192040,
    92193000, 92193005, 92193020, 92193025,
    92201010, 92291300, 93202000, 93301400,
    92302000, 92302500, 92303010, 92303100, 92304100,
    92305010, 92305040, 92305050, 92305090, 92305110, 92305180,
    92305900, 92305910, 92305920,
    92306000, 92306090, 92306700, 92306800, 92307000, 92307400,
    92307500, 92307510, 92307520,
    92308000, 92308010, 92308020, 92308030, 92308040, 92308050,
    92308500, 92308510, 92308520, 92308530, 92308540, 92308550,
    92309000, 92309010, 92309020, 92309030, 92309040, 92309050,
    92309500, 92309510, 92309520,
    92400000, 92400100,
    92410310, 92410315, 92410320, 92410340, 92410350, 92410360,
    92410370, 92410390, 92410400, 92410410, 92410420,
    92410510, 92410520, 92410550, 92410560,
    92410610, 92410620, 92410710, 92410720, 92410810, 92410820,
    92411510, 92411520, 92411610, 92411620,
    92432000, 92433000,
    92510610, 92510650, 92510955, 92510960, 92511015,
    92513000, 92513010,
    92530410, 92530510, 92530610, 92530950, 92531030,
    92541010, 92542000,
    92550030, 92550035, 92550040, 92550110, 92550200,
    92550370, 92550400, 92550405, 92550610, 92550620,
    92552000, 92552010, 92552020, 92552030,
    92582100, 92582110,
    92900100, 92900110, 92900200, 92900300,
    93301216,
    95101000, 95101010, 95102000, 95103000, 95103010,
    95104000, 95105000, 95106000, 95106010,
    95110000, 95110010, 95110020,
    95120000, 95120010, 95120020, 95120050,
    95310200, 95310400, 95310500, 95310550, 95310555, 95310560,
    95310600, 95310700, 95310750, 95310800, 95311000,
    95312400, 95312410, 95312500, 95312550, 95312555, 95312560,
    95312600, 95312700, 95312800, 95312900, 95312905, 95313200,
    95320200, 95320500, 95321000, 95322200, 95322500, 95323000,
]

_DASH_MPED_SKIM_MILK_CODES = [11111170, 11113000, 11114320, 11115000, 11120000, 11121300, 11212050]

_DASH_MPED_LOWF_CHEESE_CODES = [14204010, 14204020, 14206010, 14207010]


def compute_dash_nhanes_mped(
    mped_per_100_gram_path=None,
    wjfrt=None,
    nutrient_path=None,
    nutrient_ind_path=None,
    demo_path=None,
    nutrient_path2=None,
    nutrient_ind_path2=None,
    skim_milk_code=None,
    lowf_cheese_code=None,
    ssb_code=None,
):
    """Compute DASH from NHANES MPED data (1999-2004).

    Identifies SSB, skim milk, low-fat cheese by food code in iff data.
    Uses quintile-based scoring via core compute_dash.
    """
    if ssb_code is None:
        ssb_code = _DASH_MPED_SSB_CODES
    if skim_milk_code is None:
        skim_milk_code = _DASH_MPED_SKIM_MILK_CODES
    if lowf_cheese_code is None:
        lowf_cheese_code = _DASH_MPED_LOWF_CHEESE_CODES

    equiv = _resolve_mped_upload(mped_per_100_gram_path)
    equiv = _process_equiv(equiv)

    if wjfrt is None:
        wjfrt = _WJFRT_DEFAULT
    elif not isinstance(wjfrt, pd.DataFrame):
        wjfrt = _resolve_mped_upload(wjfrt)

    equiv = _merge_wjfrt(equiv, wjfrt)

    def _process_day(nt_ind_path):
        nt_ind = _resolve_mped_upload(nt_ind_path)
        nt_ind = _nutrient_rename(nt_ind)
        result = _process_ind_foods(nt_ind, equiv, wjfrt)
        if result is None:
            return None

        food_col = "FOODCODE"
        if food_col not in nt_ind.columns:
            for c in ["DR1IFDCD", "DRDIFDCD"]:
                if c in nt_ind.columns:
                    nt_ind["FOODCODE"] = nt_ind[c].astype(int)
                    break

        if food_col in nt_ind.columns:
            result["ADDED_SUGAR_SSB_SERV"] = np.where(
                nt_ind[food_col].isin(ssb_code),
                nt_ind.get("ADD_SUG", pd.Series(0, index=nt_ind.index)) * nt_ind.get(
                    "DR1IGRMS", nt_ind.get("DRXIGRMS", pd.Series(0, index=nt_ind.index))
                ).fillna(0) / 100,
                0.0
            )
            result["SKIM_MILK_SERV"] = np.where(
                nt_ind[food_col].isin(skim_milk_code),
                nt_ind.get("D_MILK", pd.Series(0, index=nt_ind.index)),
                0.0
            )
            result["LOWF_CHEESECREAM_SERV"] = np.where(
                nt_ind[food_col].isin(lowf_cheese_code),
                nt_ind.get("D_CHEESE", pd.Series(0, index=nt_ind.index)) * 4,
                0.0
            )

        return result

    day1 = _process_day(nutrient_ind_path)
    day2 = _process_day(nutrient_ind_path2) if nutrient_ind_path2 is not None else None
    merged = _merge_day1_day2(day1, day2)

    if merged is None:
        raise ValueError("No data after processing")

    for col in ["ADDED_SUGAR_SSB_SERV", "SKIM_MILK_SERV", "LOWF_CHEESECREAM_SERV"]:
        if col not in merged.columns:
            merged[col] = 0.0

    v_orange = merged.get("V_ORANGE", pd.Series(0, index=merged.index)).fillna(0)
    v_tomato = merged.get("V_TOMATO", pd.Series(0, index=merged.index)).fillna(0)
    v_other = merged.get("V_OTHER", pd.Series(0, index=merged.index)).fillna(0)
    v_starcy = merged.get("V_STARCY", pd.Series(0, index=merged.index)).fillna(0)

    result = compute_dash(
        data=merged,
        respondent_id=merged["SEQN"].values,
        total_kcal=_safe_kcal(merged.get("TOTALKCAL", pd.Series(2000, index=merged.index))),
        fruit_fruit_juice=merged.get("F_TOTAL", pd.Series(0, index=merged.index)).values,
        vegetable=(merged.get("V_DRKGR", pd.Series(0, index=merged.index)).fillna(0)
                   + (v_orange + v_tomato + v_other + v_starcy) / 0.5).values,
        nut_legume=(merged.get("M_NUTSD", pd.Series(0, index=merged.index)).fillna(0)
                    + merged.get("M_SOY", pd.Series(0, index=merged.index)).fillna(0)
                    + merged.get("LEGUMES", pd.Series(0, index=merged.index)).fillna(0) * 4).values,
        whole_grain=merged.get("G_WHL", pd.Series(0, index=merged.index)).values,
        low_fat_dairy=(merged.get("SKIM_MILK_SERV", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("LOWF_CHEESECREAM_SERV", pd.Series(0, index=merged.index)).fillna(0)
                       + merged.get("D_YOGURT", pd.Series(0, index=merged.index)).fillna(0)).values,
        sodium=(merged.get("SODIUM", pd.Series(1000, index=merged.index)).values
                / (_safe_kcal(merged.get("TOTALKCAL", pd.Series(2000, index=merged.index))) / 2000)),
        red_processed_meat=(merged.get("M_FRANK", pd.Series(0, index=merged.index)).fillna(0) / 1.5
                            + (merged.get("M_MEAT", pd.Series(0, index=merged.index)).fillna(0)
                               + merged.get("M_ORGAN", pd.Series(0, index=merged.index)).fillna(0)) / 4).values,
        ssb_fruit_juice=(merged.get("ADDED_SUGAR_SSB_SERV", pd.Series(0, index=merged.index)).fillna(0) * 4 / 26).values,
    )

    result["SEQN"] = merged["SEQN"].values
    result, _ = _merge_demo(result, demo_path)
    return result


# ── DI_GM NHANES MPED ───────────────────────────────────────────────────────

# FNDDS 17-18 food codes for DI_GM (same as FPED defaults)
_DIGM_MPED_AVOCADO = [63105010]
_DIGM_MPED_BROCCOLI = [
    72103000, 72103030, 72201100, 72201190, 72201211, 72201212, 72201220,
    72201221, 72201222, 72201223, 72201224, 72201226, 72201227, 72203000, 72203070,
]
_DIGM_MPED_CHICKPEA = [41301990, 41302010, 41302020, 41302040, 41302080, 41302110]
_DIGM_MPED_COFFEE = [
    92100000, 92100500, 92101000, 92101500, 92101600, 92101610, 92101630,
    92101700, 92101800, 92101810, 92101820, 92101850, 92101851,
    92101900, 92101901, 92101903, 92101904, 92101905, 92101906,
    92101910, 92101911, 92101913, 92101917, 92101918, 92101919,
    92101920, 92101921, 92101923, 92101925, 92101926, 92101928,
    92101930, 92101931, 92101933, 92101935, 92101936, 92101938,
    92101950, 92101955, 92101960, 92101965, 92101970, 92101975,
    92102000, 92102010, 92102020, 92102030, 92102040, 92102050,
    92102060, 92102070, 92102080, 92102090, 92102100, 92102110,
    92102400, 92102401, 92102450, 92102500, 92102501, 92102502, 92102503,
    92102504, 92102505, 92102510, 92102511, 92102512, 92102513, 92102514, 92102515,
    92102600, 92102601, 92102602, 92102610, 92102611, 92102612,
    92103000, 92104000, 92111000, 92111010, 92114000,
    92121000, 92121001, 92121010, 92121020, 92121030, 92121040, 92121041, 92121050,
    92130000, 92130001, 92130005, 92130006, 92130010, 92130011,
    92130020, 92130021, 92130030, 92130031,
    92152000, 92152010,
    92161000, 92161001, 92161002,
    92162000, 92162001, 92162002,
    92171000, 92171010, 92201010,
]
_DIGM_MPED_CRANBERRY = [62109100, 63207010, 63207110]
_DIGM_MPED_FERMENTED_DAIRY = [
    11400000, 11400010, 11410000, 11411010, 11411100, 11411200, 11411300,
    11411390, 11411400, 11411410, 11411420, 11430000, 11431000, 11432000,
    11433000, 11433990, 11434000, 11434010, 11434020, 11434090,
    11434100, 11434200, 11434300, 11435000, 11435010, 11435020, 11435030, 11435100,
    11436000, 11446000, 11480010, 11480020, 11480030, 11480040,
    42401100, 67250100, 67250150, 67404070, 67404300, 67404500,
    67408500, 67413700, 67430500,
    14010000, 14101010, 14102010, 14103010, 14103020,
    14104100, 14104110, 14104115, 14104200, 14104250, 14104400, 14104600, 14104700,
    14105010, 14105200, 14106010, 14106200, 14106500,
    14107010, 14107030, 14107040, 14107060, 14107200, 14107250,
    14108010, 14108015, 14108020, 14108060, 14108200, 14108400, 14108420,
    14109010, 14109020, 14109030, 14109040,
    14110010, 14120010, 14120020, 14131000,
    14200100, 14201010, 14201200, 14201500,
    14202010, 14202020, 14203010, 14203020, 14203510,
    14204010, 14204020, 14206010, 14207010,
    14410100, 14410110, 14410120, 14410130, 14410210, 14410330, 14410500,
    14410600, 14410620, 14420100, 14420160, 14420300,
    14502000, 14610200, 14610210, 14610250, 14610520,
    11115400, 12310100, 12310350, 12310370, 12320100,
    11115000, 11115100, 11115200, 11115300,
]
_DIGM_MPED_GREEN_TEA = [
    92303010, 92303100, 92305900, 92305910, 92305920,
    92308500, 92308510, 92308520, 92308530, 92308540, 92308550,
    92309500, 92309510, 92309520,
]
_DIGM_MPED_SOYBEAN = [11320000, 11320100, 11320200, 11321000, 11321100, 11321200, 41107010, 41410010]


def compute_di_gm_nhanes_mped(
    mped_per_100_gram_path=None,
    wjfrt=None,
    nutrient_path=None,
    nutrient_ind_path=None,
    demo_path=None,
    nutrient_path2=None,
    nutrient_ind_path2=None,
    avocado_code=None,
    broccoli_code=None,
    chickpea_code=None,
    coffee_code=None,
    cranberry_code=None,
    fermented_dairy_code=None,
    green_tea_code=None,
    soybean_code=None,
):
    """Compute DI_GM from NHANES MPED data (1999-2004).

    Identifies 8 special food types by FNDDS food code.
    Uses sex-specific median ranking via core compute_di_gm.
    """
    if avocado_code is None:
        avocado_code = _DIGM_MPED_AVOCADO
    if broccoli_code is None:
        broccoli_code = _DIGM_MPED_BROCCOLI
    if chickpea_code is None:
        chickpea_code = _DIGM_MPED_CHICKPEA
    if coffee_code is None:
        coffee_code = _DIGM_MPED_COFFEE
    if cranberry_code is None:
        cranberry_code = _DIGM_MPED_CRANBERRY
    if fermented_dairy_code is None:
        fermented_dairy_code = _DIGM_MPED_FERMENTED_DAIRY
    if green_tea_code is None:
        green_tea_code = _DIGM_MPED_GREEN_TEA
    if soybean_code is None:
        soybean_code = _DIGM_MPED_SOYBEAN

    equiv = _resolve_mped_upload(mped_per_100_gram_path)
    equiv = _process_equiv(equiv)

    if wjfrt is None:
        wjfrt = _WJFRT_DEFAULT
    elif not isinstance(wjfrt, pd.DataFrame):
        wjfrt = _resolve_mped_upload(wjfrt)

    equiv = _merge_wjfrt(equiv, wjfrt)

    def _process_day(nt_ind_path):
        nt_ind = _resolve_mped_upload(nt_ind_path)
        nt_ind = _nutrient_rename(nt_ind)
        result = _process_ind_foods(nt_ind, equiv, wjfrt)
        if result is None:
            return None

        food_col = "FOODCODE"
        if food_col not in nt_ind.columns:
            for c in ["DR1IFDCD", "DRDIFDCD"]:
                if c in nt_ind.columns:
                    nt_ind["FOODCODE"] = nt_ind[c].astype(int)
                    break

        gram_col = None
        for c in ["DR1IGRMS", "DRXIGRMS"]:
            if c in nt_ind.columns:
                gram_col = c
                break

        grams = pd.to_numeric(nt_ind[gram_col], errors="coerce").fillna(0) if gram_col else 0

        if food_col in nt_ind.columns:
            special_foods = [
                ("AVOCADO_SERV", avocado_code),
                ("BROCCOLI_SERV", broccoli_code),
                ("CHICKPEA_SERV", chickpea_code),
                ("COFFEE_SERV", coffee_code),
                ("CRANBERRY_SERV", cranberry_code),
                ("FERMENTED_DAIRY_SERV", fermented_dairy_code),
                ("GREEN_TEA_SERV", green_tea_code),
                ("SOYBEAN_SERV", soybean_code),
            ]
            for name, codes in special_foods:
                mask = nt_ind[food_col].isin(codes)
                nt_ind[f"_{name}"] = np.where(mask, grams, 0.0)
                spec_sum = nt_ind[mask].groupby("SEQN", as_index=False)[f"_{name}"].sum()
                if not spec_sum.empty:
                    result = result.merge(spec_sum, on="SEQN", how="left").fillna(0)
                if f"_{name}" not in result.columns:
                    result[f"_{name}"] = 0.0

        return result

    day1 = _process_day(nutrient_ind_path)
    day2 = _process_day(nutrient_ind_path2) if nutrient_ind_path2 is not None else None
    merged = _merge_day1_day2(day1, day2)

    if merged is None:
        raise ValueError("No data after processing")

    for col in ["AVOCADO_SERV", "BROCCOLI_SERV", "CHICKPEA_SERV", "COFFEE_SERV",
                "CRANBERRY_SERV", "FERMENTED_DAIRY_SERV", "GREEN_TEA_SERV", "SOYBEAN_SERV"]:
        if col not in merged.columns:
            merged[col] = 0.0

    gender = pd.Series(2, index=merged.index)
    demo_df = None
    if demo_path is not None:
        demo_df = _resolve_mped_upload(demo_path)
        if demo_df is not None and "RIAGENDR" in demo_df.columns:
            demo_df["SEQN"] = demo_df["SEQN"].astype(int)
            gmap = dict(zip(demo_df["SEQN"], demo_df["RIAGENDR"]))
            gender = pd.Series([gmap.get(s, 2) for s in merged["SEQN"].values])

    kcal = _safe_kcal(merged.get("TOTALKCAL", pd.Series(2000, index=merged.index)))
    tfat = _safe_val(merged.get("TOTALFAT", merged.get("DR1TTFAT", pd.Series(0, index=merged.index))))

    result = compute_di_gm(
        data=merged,
        respondent_id=merged["SEQN"].values,
        gender=gender.values if hasattr(gender, "values") else gender,
        avocado=merged["AVOCADO_SERV"].values,
        broccoli=merged["BROCCOLI_SERV"].values,
        chickpea=merged["CHICKPEA_SERV"].values,
        coffee=merged["COFFEE_SERV"].values,
        cranberry=merged["CRANBERRY_SERV"].values,
        fermented_dairy=merged["FERMENTED_DAIRY_SERV"].values,
        fiber=merged.get("FIBER", merged.get("DR1TFIBE", pd.Series(0, index=merged.index))).values,
        green_tea=merged["GREEN_TEA_SERV"].values,
        soybean=merged["SOYBEAN_SERV"].values,
        whole_grain=merged.get("G_WHL", pd.Series(0, index=merged.index)).values,
        total_fat_pct=(tfat * 9 / kcal) * 100,
        processed_meat=merged.get("M_FRANK", pd.Series(0, index=merged.index)).values,
        red_meat=merged.get("M_MEAT", pd.Series(0, index=merged.index)).values,
        refined_grain=merged.get("G_NWHL", pd.Series(0, index=merged.index)).values,
    )

    result["SEQN"] = merged["SEQN"].values
    result, _ = _merge_demo(result, demo_path)
    return result
