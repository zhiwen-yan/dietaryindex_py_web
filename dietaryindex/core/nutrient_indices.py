"""Nutrient-density, acid-load, and antioxidant composite indices."""

from __future__ import annotations

import numpy as np
import pandas as pd

from dietaryindex.reference.nutrient_benchmarks import (
    NRF9_3_DEFAULT_VERSION,
    NRF9_3_UNCAPPED_LIM_VERSION,
    get_benchmark_lookup,
    get_nrf_benchmark_lookup,
    normalize_nrf_version,
)


NRF_POSITIVE_NUTRIENTS = (
    "Protein",
    "Fiber",
    "Vitamin_A",
    "Vitamin_C",
    "Vitamin_E",
    "Calcium",
    "Iron",
    "Magnesium",
    "Potassium",
)

NRF_LIMIT_NUTRIENTS = (
    "Saturated_fat",
    "Added_sugar",
    "Sodium",
)

ADEQUACY_NUTRIENTS = (
    "Protein",
    "Fiber",
    "Vitamin_A",
    "Vitamin_C",
    "Vitamin_E",
    "Calcium",
    "Iron",
    "Magnesium",
    "Potassium",
)


def _as_series(values, name: str, length: int | None = None) -> pd.Series:
    if values is None:
        if length is None:
            raise ValueError(f"{name} is required to establish row count.")
        return pd.Series([np.nan] * length, name=name, dtype=float)

    series = pd.Series(np.asarray(values), name=name)
    if length is not None and len(series) != length:
        raise ValueError(f"{name} length does not match the expected number of rows.")
    return pd.to_numeric(series, errors="coerce")


def _resolve_ids(respondent_id, length: int) -> pd.Series:
    if respondent_id is None:
        return pd.Series(np.arange(1, length + 1), name="RESPONDENTID")
    series = pd.Series(np.asarray(respondent_id), name="RESPONDENTID")
    if len(series) != length:
        raise ValueError("respondent_id length must match the number of rows.")
    return series.reset_index(drop=True)


def _build_frame(respondent_id=None, **kwargs) -> tuple[pd.Series, pd.DataFrame]:
    first = None
    for key, values in kwargs.items():
        if values is not None:
            first = _as_series(values, key)
            break
    if first is None:
        raise ValueError("At least one nutrient input is required.")

    n = len(first)
    ids = _resolve_ids(respondent_id, n)
    frame = pd.DataFrame(index=np.arange(n))
    for key, values in kwargs.items():
        frame[key] = _as_series(values, key, n)
    return ids, frame


def _score_density_percent(intake: pd.Series, energy: pd.Series, benchmark: float, reference_energy_kcal: float) -> pd.Series:
    denom = benchmark * energy / reference_energy_kcal
    return np.where(
        pd.notna(intake) & pd.notna(energy) & (energy > 0) & (denom > 0),
        intake / denom * 100.0,
        np.nan,
    )


def compute_nrf(
    data,
    respondent_id=None,
    energy=None,
    protein=None,
    fiber=None,
    vitamin_a=None,
    vitamin_c=None,
    vitamin_e=None,
    calcium=None,
    iron=None,
    magnesium=None,
    potassium=None,
    saturated_fat=None,
    added_sugar=None,
    sodium=None,
    reference_energy_kcal: float = 2000.0,
    version: str = NRF9_3_DEFAULT_VERSION,
):
    """Compute a diet-level, 2,000-kcal adaptation of published NRF9.3.

    All nine beneficial nutrients and all three limiting nutrients are
    required for the fixed-panel total. Vitamin A is expected in ug RAE and
    vitamin E in mg alpha-tocopherol. The v0.2.1 default caps every component
    at 100% of its DV/MRV, yielding a -300 to 900 total range. The earlier
    uncapped-LIM behavior is available only as the explicit
    ``nrf9.3_2009_metric_uncapped_lim`` variant.
    """

    ids, df = _build_frame(
        respondent_id=respondent_id,
        Energy=energy,
        Protein=protein,
        Fiber=fiber,
        Vitamin_A=vitamin_a,
        Vitamin_C=vitamin_c,
        Vitamin_E=vitamin_e,
        Calcium=calcium,
        Iron=iron,
        Magnesium=magnesium,
        Potassium=potassium,
        Saturated_fat=saturated_fat,
        Added_sugar=added_sugar,
        Sodium=sodium,
    )

    normalized_version = normalize_nrf_version(version)
    refs = get_nrf_benchmark_lookup(normalized_version)
    out = pd.DataFrame({"RESPONDENTID": ids})

    pos_cols = []
    for nutrient in NRF_POSITIVE_NUTRIENTS:
        if nutrient not in df:
            continue
        score = _score_density_percent(df[nutrient], df["Energy"], refs[nutrient], reference_energy_kcal)
        capped = np.clip(score, 0.0, 100.0)
        col = f"NRF_{nutrient.upper()}"
        out[col] = capped
        pos_cols.append(col)

    lim_cols = []
    for nutrient in NRF_LIMIT_NUTRIENTS:
        score = _score_density_percent(df[nutrient], df["Energy"], refs[nutrient], reference_energy_kcal)
        # v0.2.1 makes the cap policy part of the version identifier.  The
        # bounded profile is the audited default; the historical uncapped LIM
        # behavior remains available for explicit sensitivity analyses.
        upper = None if normalized_version == NRF9_3_UNCAPPED_LIM_VERSION else 100.0
        capped = np.clip(score, 0.0, upper)
        col = f"NRF_{nutrient.upper()}"
        out[col] = capped
        lim_cols.append(col)

    out["NRF_NR9_SUM"] = out[pos_cols].sum(axis=1, min_count=len(NRF_POSITIVE_NUTRIENTS))
    out["NRF_LIM3_SUM"] = out[lim_cols].sum(axis=1, min_count=len(NRF_LIMIT_NUTRIENTS))
    out["NRF_ALL"] = out["NRF_NR9_SUM"] - out["NRF_LIM3_SUM"]
    return out


def compute_nar(
    data,
    respondent_id=None,
    protein=None,
    fiber=None,
    vitamin_a=None,
    vitamin_c=None,
    vitamin_e=None,
    calcium=None,
    iron=None,
    magnesium=None,
    potassium=None,
    version: str = "usda",
):
    """Compute nutrient adequacy ratios (NAR) using capped intake/reference ratios."""

    ids, df = _build_frame(
        respondent_id=respondent_id,
        Protein=protein,
        Fiber=fiber,
        Vitamin_A=vitamin_a,
        Vitamin_C=vitamin_c,
        Vitamin_E=vitamin_e,
        Calcium=calcium,
        Iron=iron,
        Magnesium=magnesium,
        Potassium=potassium,
    )

    refs = get_benchmark_lookup(version)
    out = pd.DataFrame({"RESPONDENTID": ids})
    comp_cols = []
    for nutrient in ADEQUACY_NUTRIENTS:
        if nutrient not in df:
            continue
        ratio = np.where(
            pd.notna(df[nutrient]) & (refs[nutrient] > 0),
            df[nutrient] / refs[nutrient],
            np.nan,
        )
        ratio = np.clip(ratio, 0.0, 1.0)
        col = f"NAR_{nutrient.upper()}"
        out[col] = ratio
        comp_cols.append(col)

    out["NAR_ALL"] = out[comp_cols].mean(axis=1, skipna=True) if comp_cols else np.nan
    return out


def compute_mar(
    data,
    respondent_id=None,
    protein=None,
    fiber=None,
    vitamin_a=None,
    vitamin_c=None,
    vitamin_e=None,
    calcium=None,
    iron=None,
    magnesium=None,
    potassium=None,
    version: str = "usda",
):
    """Compute mean adequacy ratio (MAR) as the mean of capped NAR values."""

    nar = compute_nar(
        data=data,
        respondent_id=respondent_id,
        protein=protein,
        fiber=fiber,
        vitamin_a=vitamin_a,
        vitamin_c=vitamin_c,
        vitamin_e=vitamin_e,
        calcium=calcium,
        iron=iron,
        magnesium=magnesium,
        potassium=potassium,
        version=version,
    )
    comp_cols = [col for col in nar.columns if col.startswith("NAR_") and col != "NAR_ALL"]
    out = pd.DataFrame({"RESPONDENTID": nar["RESPONDENTID"]})
    for col in comp_cols:
        out[col.replace("NAR_", "MAR_")] = nar[col]
    out["MAR_ALL"] = nar[comp_cols].mean(axis=1, skipna=True) * 100.0 if comp_cols else np.nan
    return out


def compute_inq(
    data,
    respondent_id=None,
    energy=None,
    protein=None,
    fiber=None,
    vitamin_a=None,
    vitamin_c=None,
    vitamin_e=None,
    calcium=None,
    iron=None,
    magnesium=None,
    potassium=None,
    reference_energy_kcal: float = 2000.0,
    version: str = "usda",
):
    """Compute the Index of Nutritional Quality (INQ)."""

    ids, df = _build_frame(
        respondent_id=respondent_id,
        Energy=energy,
        Protein=protein,
        Fiber=fiber,
        Vitamin_A=vitamin_a,
        Vitamin_C=vitamin_c,
        Vitamin_E=vitamin_e,
        Calcium=calcium,
        Iron=iron,
        Magnesium=magnesium,
        Potassium=potassium,
    )

    refs = get_benchmark_lookup(version)
    out = pd.DataFrame({"RESPONDENTID": ids})
    comp_cols = []
    for nutrient in ADEQUACY_NUTRIENTS:
        if nutrient not in df:
            continue
        inq = _score_density_percent(df[nutrient], df["Energy"], refs[nutrient], reference_energy_kcal) / 100.0
        col = f"INQ_{nutrient.upper()}"
        out[col] = inq
        comp_cols.append(col)
    out["INQ_ALL"] = out[comp_cols].mean(axis=1, skipna=True) if comp_cols else np.nan
    return out


def compute_pral(
    data,
    respondent_id,
    protein,
    phosphorus,
    potassium,
    magnesium,
    calcium,
):
    """Compute potential renal acid load (PRAL).

    Formula:
    PRAL = 0.49 * protein + 0.037 * phosphorus - 0.021 * potassium
           - 0.026 * magnesium - 0.013 * calcium
    """

    ids, df = _build_frame(
        respondent_id=respondent_id,
        Protein=protein,
        Phosphorus=phosphorus,
        Potassium=potassium,
        Magnesium=magnesium,
        Calcium=calcium,
    )

    out = pd.DataFrame({"RESPONDENTID": ids})
    out["PRAL_PROTEIN"] = 0.49 * df["Protein"]
    out["PRAL_PHOSPHORUS"] = 0.037 * df["Phosphorus"]
    out["PRAL_POTASSIUM"] = -0.021 * df["Potassium"]
    out["PRAL_MAGNESIUM"] = -0.026 * df["Magnesium"]
    out["PRAL_CALCIUM"] = -0.013 * df["Calcium"]
    out["PRAL_ALL"] = out[
        ["PRAL_PROTEIN", "PRAL_PHOSPHORUS", "PRAL_POTASSIUM", "PRAL_MAGNESIUM", "PRAL_CALCIUM"]
    ].sum(axis=1, min_count=5)
    return out


def compute_neap(
    data,
    respondent_id,
    protein,
    potassium,
):
    """Compute net endogenous acid production (NEAP).

    Potassium is expected in mg/day and is internally converted to mEq/day
    using 39.0983 mg per mEq of potassium.
    """

    ids, df = _build_frame(
        respondent_id=respondent_id,
        Protein=protein,
        Potassium=potassium,
    )
    out = pd.DataFrame({"RESPONDENTID": ids})
    potassium_meq = df["Potassium"] / 39.0983
    out["NEAP_RATIO"] = np.where(
        pd.notna(df["Protein"]) & pd.notna(potassium_meq) & (potassium_meq > 0),
        df["Protein"] / potassium_meq,
        np.nan,
    )
    out["NEAP_ALL"] = 54.5 * out["NEAP_RATIO"] - 10.2
    return out


def compute_cdai(
    data,
    respondent_id,
    zinc,
    selenium,
    total_carotenoids,
    vitamin_a,
    vitamin_c,
    vitamin_e,
):
    """Compute the Composite Dietary Antioxidant Index (CDAI).

    CDAI is calculated as the sum of sample-standardized z scores across the
    six antioxidant nutrients most commonly used in the literature.
    """

    ids, df = _build_frame(
        respondent_id=respondent_id,
        Zinc=zinc,
        Selenium=selenium,
        Total_carotenoids=total_carotenoids,
        Vitamin_A=vitamin_a,
        Vitamin_C=vitamin_c,
        Vitamin_E=vitamin_e,
    )

    out = pd.DataFrame({"RESPONDENTID": ids})
    comp_cols = []
    for nutrient in ("Zinc", "Selenium", "Total_carotenoids", "Vitamin_A", "Vitamin_C", "Vitamin_E"):
        series = df[nutrient]
        mean = series.mean(skipna=True)
        std = series.std(skipna=True, ddof=0)
        z = (
            (series - mean) / std
            if pd.notna(std) and std > 0
            else pd.Series(np.where(series.notna(), 0.0, np.nan), dtype=float)
        )
        col = f"CDAI_{nutrient.upper()}"
        out[col] = z
        comp_cols.append(col)

    out["CDAI_ALL"] = out[comp_cols].sum(axis=1, min_count=len(comp_cols))
    return out
