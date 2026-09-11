"""Adapters for Food Inflammatory Score Index (FISI/FII)."""

from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd

from dietaryindex.core.fisi import (
    FISI26_COMPONENTS,
    FISI34_COMPONENTS,
    compute_fisi,
)
from dietaryindex.reference.fisi_nrv import (
    FISI_FLAVONOID_COMPONENTS,
    load_fisi_nrv,
)


FISI_NHANES_PATTERNS = {
    "Protein": ("DR1TPROT", "DRXTPROT", "DR2TPROT"),
    "Total_fat": ("DR1TTFAT", "DRXTTFAT", "DR2TTFAT"),
    "Carbohydrate": ("DR1TCARB", "DRXTCARB", "DR2TCARB"),
    "Energy": ("DR1TKCAL", "DRXTKCAL", "DR2TKCAL"),
    "Alcohol": ("DR1TALCO", "DRXTALCO", "DR2TALCO"),
    "Caffeine": ("DR1TCAFF", "DRXTCAFF", "DR2TCAFF"),
    "Fiber": ("DR1TFIBE", "DRXTFIBE", "DR2TFIBE"),
    "Iron": ("DR1TIRON", "DRXTIRON", "DR2TIRON"),
    "Magnesium": ("DR1TMAGN", "DRXTMAGN", "DR2TMAGN"),
    "Zinc": ("DR1TZINC", "DRXTZINC", "DR2TZINC"),
    "Selenium": ("DR1TSELE", "DRXTSELE", "DR2TSELE"),
    "Vitamin_A": ("DR1TVARA", "DRXTVARA", "DR2TVARA"),
    "Carotene_alpha": ("DR1TACAR", "DRXTACAR", "DR2TACAR"),
    "Vitamin_E": ("DR1TATOC", "DRXTATOC", "DR2TATOC"),
    "Vitamin_D": ("DR1TVD", "DRXTVD", "DR2TVD"),
    "Vitamin_C": ("DR1TVC", "DRXTVC", "DR2TVC"),
    "Thiamin": ("DR1TVB1", "DRXTVB1", "DR2TVB1"),
    "Riboflavin": ("DR1TVB2", "DRXTVB2", "DR2TVB2"),
    "Niacin": ("DR1TNIAC", "DRXTNIAC", "DR2TNIAC"),
    "Vitamin_B6": ("DR1TVB6", "DRXTVB6", "DR2TVB6"),
    "Vitamin_B12": ("DR1TVB12", "DRXTVB12", "DR2TVB12"),
    "Folic_acid": ("DR1TFOLA", "DR1TFA", "DRXTFOLA", "DR2TFOLA", "DR2TFA"),
    "Vitamin_E_added": ("DR1TATOA", "DRXTATOA", "DR2TATOA"),
    "Vitamin_B_12_added": ("DR1TB12A", "DRXTB12A", "DR2TB12A"),
    "Cholesterol": ("DR1TCHOL", "DRXTCHOL", "DR2TCHOL"),
    "Saturated_fat": ("DR1TSFAT", "DRXTSFAT", "DR2TSFAT"),
    "PUFA_18_2": ("DR1TP182", "DRXTP182", "DR2TP182"),
    "PUFA_18_3": ("DR1TP183", "DRXTP183", "DR2TP183"),
    "PUFA_20_4": ("DR1TP204", "DRXTP204", "DR2TP204"),
    "DHA": ("DR1TP226", "DRXTP226", "DR2TP226"),
    "EPA": ("DR1TP205", "DRXTP205", "DR2TP205"),
    "DPA": ("DR1TP225", "DRXTP225", "DR2TP225"),
    "total_monounsaturated": ("DR1TMFAT", "DRXTMFAT", "DR2TMFAT"),
    "total_polyunsaturated": ("DR1TPFAT", "DRXTPFAT", "DR2TPFAT"),
}


def _normalize_fdcd(values):
    """Normalize NHANES food codes read as integers, floats, or strings."""
    text = values.astype(str).str.strip()
    return text.str.replace(r"\.0+$", "", regex=True)

FLAVONOID_PATTERNS = {
    "Flavan_3_ols": ("DR1T_FL_3_OLS", "DRXTF3OL", "DR2T_FL_3_OLS", "DR1IF3OL", "DR2IF3OL"),
    "Flavanones": ("DR1T_FL_NONES", "DRXTFLNO", "DR2T_FL_NONES", "DR1IFLNO", "DR2IFLNO"),
    "Flavones": ("DR1T_FL_ONES", "DRXTFONE", "DR2T_FL_ONES", "DR1IFONE", "DR2IFONE"),
    "Flavonols": ("DR1T_FL_OLS", "DRXTFOLS", "DR2T_FL_OLS", "DR1IFOLS", "DR2IFOLS"),
    "Isoflavones": ("DR1T_FL_ISO", "DRXTFISO", "DR2T_FL_ISO", "DR1IFISO", "DR2IFISO"),
    "Anthocyanidins": ("DR1T_FL_ANT", "DRXTFANT", "DR2T_FL_ANT", "DR1IFANT", "DR2IFANT"),
    "Proanthocyanidins": ("DR1T_FL_PAN", "DRXTFPAN", "DR2T_FL_PAN", "DR1IFPAN", "DR2IFPAN"),
    "Total_flavonoids": ("DR1T_FL_TOT", "DRXTFTOT", "DR2T_FL_TOT", "DR1IFTOT", "DR2IFTOT"),
}


def compute_fisi_nhanes(
    nutrient_path1,
    nutrient_path2=None,
    demo_path=None,
    exclude_extremes=True,
    include_flavonoids=False,
):
    """Calculate USDA-version FISI from NHANES total nutrient files."""
    return compute_fisi26_nhanes(
        nutrient_path1=nutrient_path1,
        nutrient_path2=nutrient_path2,
        demo_path=demo_path,
        version="usda",
        components=FISI34_COMPONENTS,
        exclude_extremes=exclude_extremes,
        include_flavonoids=include_flavonoids,
    )


def compute_fisi26_nhanes(
    nutrient_path1,
    nutrient_path2=None,
    demo_path=None,
    version="china",
    components=FISI26_COMPONENTS,
    exclude_extremes=True,
    include_flavonoids=False,
):
    """Calculate FISI from NHANES 24-hour recall total nutrient files."""
    day1 = _prepare_nhanes_nutrient_day(nutrient_path1, FISI_NHANES_PATTERNS)
    day2 = (
        _prepare_nhanes_nutrient_day(nutrient_path2, FISI_NHANES_PATTERNS)
        if nutrient_path2 is not None
        else None
    )
    nutrient = _combine_day_frames(day1, day2, id_col="SEQN")

    if exclude_extremes and "Energy" in nutrient.columns:
        energy = pd.to_numeric(nutrient["Energy"], errors="coerce")
        nutrient = nutrient[(energy > 500) & (energy < 5000)].copy()
        if "Alcohol" in nutrient.columns:
            alcohol = pd.to_numeric(nutrient["Alcohol"], errors="coerce")
            nutrient = nutrient[alcohol.isna() | (alcohol <= 40)].copy()

    result = compute_fisi(
        nutrient,
        id_col="SEQN",
        version=version,
        include_flavonoids=include_flavonoids,
        components=components,
        quiet=True,
    )
    result = result.rename(columns={"ID": "SEQN", "Components_Used": "Components_Count"})

    demo = _prepare_demo(demo_path)
    if demo is not None:
        result = result.merge(demo, on="SEQN", how="left")
    return result


def compute_fisi1_nhanes(
    iff_day1,
    tot_day1,
    fii_csv,
    iff_day2=None,
    tot_day2=None,
    demo_path=None,
    exclude_extremes=True,
):
    """Calculate food-level FISI-1 from NHANES individual-foods files."""
    food_fii = _load_table(fii_csv).copy()
    if not {"FDCD", "FII"}.issubset(food_fii.columns):
        raise ValueError("fii_csv must contain FDCD and FII columns.")
    food_fii["FDCD"] = _normalize_fdcd(food_fii["FDCD"])
    food_fii["FII"] = pd.to_numeric(food_fii["FII"], errors="coerce")

    day1_iff = _prepare_food_day(iff_day1, day=1)
    day1_tot = _prepare_tot_qc(tot_day1, day=1)
    day1_score = _score_food_day(day1_iff, food_fii, grams_col="Grams1")

    has_day2 = iff_day2 is not None and tot_day2 is not None
    if has_day2:
        day2_iff = _prepare_food_day(iff_day2, day=2)
        day2_tot = _prepare_tot_qc(tot_day2, day=2)
        day2_score = _score_food_day(day2_iff, food_fii, grams_col="Grams2")
        combined = day1_score.merge(day2_score, on="SEQN", how="outer", suffixes=("_1", "_2"))
        combined["FISI1"] = combined[["FISI_day_1", "FISI_day_2"]].mean(axis=1, skipna=True)
        result = combined[["SEQN", "FISI1"]].merge(day1_tot, on="SEQN", how="left")
        result = result.merge(day2_tot, on="SEQN", how="left")
    else:
        result = day1_score.rename(columns={"FISI_day_1": "FISI1"}).merge(
            day1_tot, on="SEQN", how="left"
        )

    demo = _prepare_demo(demo_path, rename_age_gender=True)
    if demo is not None:
        result = result.merge(demo, on="SEQN", how="left")

    if exclude_extremes:
        result = _filter_fisi1_qc(result, has_day2=has_day2)

    first_cols = [c for c in ["SEQN", "FISI1", "Age", "Gender"] if c in result.columns]
    other_cols = [c for c in result.columns if c not in first_cols]
    return result[first_cols + other_cols].sort_values("SEQN").reset_index(drop=True)


def compute_flav_fisi_nhanes(
    flav_path1,
    flav_path2=None,
    include_flavonoids=True,
):
    """Calculate flavonoid-specific FISI from NHANES flavonoid files."""
    day1 = _prepare_nhanes_nutrient_day(flav_path1, FLAVONOID_PATTERNS)
    day2 = (
        _prepare_nhanes_nutrient_day(flav_path2, FLAVONOID_PATTERNS)
        if flav_path2 is not None
        else None
    )
    flav = _combine_day_frames(day1, day2, id_col="SEQN")
    if not include_flavonoids:
        cols = ["SEQN"] + [c for c in FISI_FLAVONOID_COMPONENTS if c in flav.columns]
        flav = flav[cols]

    available = [c for c in flav.columns if c != "SEQN"]
    if not available:
        raise ValueError("No flavonoid variables found in the data.")

    nrv = load_fisi_nrv("usda")
    allowed = set(nrv[nrv["Variable"].isin(FISI_FLAVONOID_COMPONENTS)]["Variable"])
    usable = [c for c in available if c in allowed]
    if not usable:
        raise ValueError("No flavonoid variables have NRV values for FLAV_FISI.")

    result = compute_fisi(
        flav[["SEQN"] + usable],
        id_col="SEQN",
        version="usda",
        include_flavonoids=True,
        quiet=True,
    ).rename(columns={"ID": "SEQN"})

    result = result.rename(
        columns={
            "FISI_Total": "FLAV_FISI",
            "Components_Used": "Flavonoids_Count",
        }
    )
    result = result.rename(
        columns={
            col: col.replace("FISI_", "FLAV_", 1)
            for col in result.columns
            if col.startswith("FISI_")
        }
    )
    return result


def _load_table(file_arg):
    if isinstance(file_arg, pd.DataFrame):
        return file_arg.reset_index(drop=True).copy()

    if isinstance(file_arg, (str, Path)):
        path = Path(file_arg)
        ext = path.suffix.lower()
        if ext == ".csv":
            return pd.read_csv(path)
        if ext in {".xlsx", ".xls"}:
            return pd.read_excel(path)
        if ext == ".xpt":
            import pyreadstat

            return pyreadstat.read_xport(path)[0]
        if ext == ".sas7bdat":
            import pyreadstat

            return pyreadstat.read_sas7bdat(path)[0]
        raise ValueError(f"Unsupported file format: {file_arg}")

    if isinstance(file_arg, BytesIO):
        import pyreadstat

        file_arg.seek(0)
        raw = file_arg.read()
        bio = BytesIO(raw)
        try:
            return pyreadstat.read_sas7bdat(bio)[0]
        except Exception:
            bio.seek(0)
            return pyreadstat.read_xport(bio)[0]

    raise ValueError(f"Unsupported file type: {type(file_arg)}")


def _series(df, col, default=np.nan):
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series(default, index=df.index, dtype=float)


def _find_column(df, patterns):
    cols = list(df.columns)
    upper_lookup = {str(col).upper(): col for col in cols}
    for pattern in patterns:
        if pattern in df.columns:
            return pattern
        found = upper_lookup.get(str(pattern).upper())
        if found is not None:
            return found
    for pattern in patterns:
        pattern_upper = str(pattern).upper()
        for col in cols:
            if pattern_upper in str(col).upper():
                return col
    return None


def _prepare_nhanes_nutrient_day(file_arg, patterns):
    df = _load_table(file_arg).copy()
    if "SEQN" not in df.columns:
        raise ValueError("NHANES data must contain SEQN.")
    result = pd.DataFrame({"SEQN": pd.to_numeric(df["SEQN"], errors="coerce")})
    result = result.dropna(subset=["SEQN"]).copy()
    result["SEQN"] = result["SEQN"].astype(int)

    valid_idx = result.index
    source = df.loc[valid_idx].reset_index(drop=True)
    result = result.reset_index(drop=True)

    status_col = _find_column(source, ("DR1DRSTZ", "DR2DRSTZ", "DRDDRSTS", "DRDDRSTZ"))
    if status_col is not None:
        keep = _series(source, status_col) == 1
        source = source[keep].reset_index(drop=True)
        result = result[keep.to_numpy()].reset_index(drop=True)

    for variable, candidates in patterns.items():
        col = _find_column(source, candidates)
        result[variable] = _series(source, col) if col is not None else np.nan

    if "Energy" in result.columns:
        energy = pd.to_numeric(result["Energy"], errors="coerce")
        result = result[energy.isna() | (energy > 0)].copy()
    return result.sort_values("SEQN").reset_index(drop=True)


def _combine_day_frames(day1, day2, id_col="SEQN"):
    if day2 is None:
        return day1.copy()
    merged = day1.merge(day2, on=id_col, how="outer", suffixes=("", "_DAY2"))
    result = pd.DataFrame({id_col: merged[id_col]})
    for col in [c for c in day1.columns if c != id_col]:
        c2 = f"{col}_DAY2"
        if c2 in merged.columns:
            result[col] = np.where(
                merged[c2].notna(),
                (pd.to_numeric(merged[col], errors="coerce") + pd.to_numeric(merged[c2], errors="coerce")) / 2.0,
                pd.to_numeric(merged[col], errors="coerce"),
            )
        else:
            result[col] = pd.to_numeric(merged[col], errors="coerce")
    return result.sort_values(id_col).reset_index(drop=True)


def _prepare_demo(demo_path, rename_age_gender=False):
    if demo_path is None:
        return None
    demo = _load_table(demo_path).copy()
    if "SEQN" not in demo.columns:
        return None
    demo["SEQN"] = pd.to_numeric(demo["SEQN"], errors="coerce")
    demo = demo.dropna(subset=["SEQN"]).copy()
    demo["SEQN"] = demo["SEQN"].astype(int)
    if "RIDAGEYR" in demo.columns:
        demo = demo[pd.to_numeric(demo["RIDAGEYR"], errors="coerce") >= 2].copy()
    cols = ["SEQN"] + [c for c in ("RIDAGEYR", "RIAGENDR", "SDDSRVYR") if c in demo.columns]
    demo = demo[cols].drop_duplicates("SEQN")
    if rename_age_gender:
        demo = demo.rename(columns={"RIDAGEYR": "Age", "RIAGENDR": "Gender"})
    return demo


def _prepare_food_day(file_arg, day):
    df = _load_table(file_arg).copy()
    food_col = _find_column(df, (f"DR{day}IFDCD", "DRDIFDCD"))
    grams_col = _find_column(df, (f"DR{day}IGRMS", "DRXIGRMS"))
    if "SEQN" not in df.columns or food_col is None or grams_col is None:
        raise ValueError("Individual foods data must contain SEQN, food code, and grams columns.")
    out = pd.DataFrame(
        {
            "SEQN": pd.to_numeric(df["SEQN"], errors="coerce"),
            "FDCD": _normalize_fdcd(df[food_col]),
            f"Grams{day}": pd.to_numeric(df[grams_col], errors="coerce"),
        }
    )
    out = out.dropna(subset=["SEQN"]).copy()
    out["SEQN"] = out["SEQN"].astype(int)
    return out


def _prepare_tot_qc(file_arg, day):
    df = _load_table(file_arg).copy()
    if "SEQN" not in df.columns:
        raise ValueError("Total nutrient data must contain SEQN.")
    status_col = _find_column(df, (f"DR{day}DRSTZ", "DRDDRSTS", "DRDDRSTZ"))
    energy_col = _find_column(df, (f"DR{day}TKCAL", "DRXTKCAL"))
    alcohol_col = _find_column(df, (f"DR{day}TALCO", "DRXTALCO"))
    result = pd.DataFrame({"SEQN": pd.to_numeric(df["SEQN"], errors="coerce")})
    if status_col is not None and day == 1:
        result["DR1DRSTZ"] = _series(df, status_col)
    if energy_col is not None:
        result[f"Energy{day}"] = _series(df, energy_col)
    if alcohol_col is not None:
        result[f"Alcohol{day}"] = _series(df, alcohol_col)
    result = result.dropna(subset=["SEQN"]).copy()
    result["SEQN"] = result["SEQN"].astype(int)
    return result


def _score_food_day(food_day, food_fii, grams_col):
    suffix = grams_col[-1]
    result = food_day.merge(food_fii, on="FDCD", how="left")
    result["FII"] = result["FII"].fillna(0.0)
    result["FII_contrib"] = result["FII"] * pd.to_numeric(result[grams_col], errors="coerce") / 100.0
    return (
        result.groupby("SEQN", as_index=False)["FII_contrib"]
        .sum()
        .rename(columns={"FII_contrib": f"FISI_day_{suffix}" if suffix in {"1", "2"} else "FISI_day"})
    )


def _filter_fisi1_qc(result, has_day2):
    filtered = result.copy()
    if "DR1DRSTZ" in filtered.columns:
        filtered = filtered[filtered["DR1DRSTZ"] == 1].copy()
    if "Energy1" in filtered.columns:
        filtered = filtered[filtered["Energy1"].between(500, 5000, inclusive="both")].copy()
    if has_day2 and "Energy2" in filtered.columns:
        energy2 = pd.to_numeric(filtered["Energy2"], errors="coerce")
        filtered = filtered[energy2.isna() | energy2.between(500, 5000, inclusive="both")].copy()
    if "Alcohol1" in filtered.columns:
        alcohol1 = pd.to_numeric(filtered["Alcohol1"], errors="coerce")
        filtered = filtered[alcohol1.isna() | (alcohol1 <= 40)].copy()
    if has_day2 and "Alcohol2" in filtered.columns:
        alcohol2 = pd.to_numeric(filtered["Alcohol2"], errors="coerce")
        filtered = filtered[alcohol2.isna() | (alcohol2 <= 40)].copy()
    return filtered
