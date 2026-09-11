"""World Index for Sustainability and Health (WISH)."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _to_series(values) -> pd.Series:
    return pd.to_numeric(pd.Series(values), errors="coerce")


def _score_protective_no_upper(values, lower_threshold: float, recommended: float) -> pd.Series:
    series = _to_series(values)
    score = pd.Series(np.nan, index=series.index, dtype=float)

    valid = series.notna()
    score.loc[valid & (series < lower_threshold)] = 0.0

    ramp = valid & (series >= lower_threshold) & (series < recommended)
    if recommended > lower_threshold:
        score.loc[ramp] = (series.loc[ramp] - lower_threshold) / (recommended - lower_threshold) * 10.0

    score.loc[valid & (series >= recommended)] = 10.0
    return score


def _score_protective_with_upper(
    values,
    lower_threshold: float,
    recommended: float,
    upper_limit: float,
) -> pd.Series:
    series = _to_series(values)
    score = pd.Series(np.nan, index=series.index, dtype=float)

    valid = series.notna()
    score.loc[valid & (series < lower_threshold)] = 0.0

    ramp = valid & (series >= lower_threshold) & (series < recommended)
    if recommended > lower_threshold:
        score.loc[ramp] = (series.loc[ramp] - lower_threshold) / (recommended - lower_threshold) * 10.0

    plateau = valid & (series >= recommended) & (series <= upper_limit)
    score.loc[plateau] = 10.0
    score.loc[valid & (series > upper_limit)] = 0.0
    return score


def _score_neutral(values, recommended: float, upper_limit: float) -> pd.Series:
    series = _to_series(values)
    score = pd.Series(np.nan, index=series.index, dtype=float)

    valid = series.notna()
    score.loc[valid & (series <= recommended)] = 10.0

    decline = valid & (series > recommended) & (series < upper_limit)
    if upper_limit > recommended:
        score.loc[decline] = (upper_limit - series.loc[decline]) / (upper_limit - recommended) * 10.0

    score.loc[valid & (series >= upper_limit)] = 0.0
    return score


def _score_limit(values, max_recommended: float, upper_limit: float) -> pd.Series:
    series = _to_series(values)
    score = pd.Series(np.nan, index=series.index, dtype=float)

    valid = series.notna()
    score.loc[valid & (series <= max_recommended)] = 10.0

    decline = valid & (series > max_recommended) & (series < upper_limit)
    if upper_limit > max_recommended:
        score.loc[decline] = (upper_limit - series.loc[decline]) / (upper_limit - max_recommended) * 10.0

    score.loc[valid & (series >= upper_limit)] = 0.0
    return score


def _score_binary_limit(values, max_recommended: float) -> pd.Series:
    series = _to_series(values)
    score = pd.Series(np.where(series <= max_recommended, 10.0, 0.0), index=series.index, dtype=float)
    score.loc[series.isna()] = np.nan
    return score


def compute_wish(
    data,
    respondent_id,
    whole_grains,
    vegetables,
    fruit,
    legumes,
    unsaturated_oils,
    fish,
    dairy,
    nuts,
    poultry,
    eggs,
    red_meat,
    saturated_oils,
    added_sugars,
):
    """Compute WISH from food-group intakes expressed in g/day."""

    ids = pd.Series(np.asarray(respondent_id), name="RESPONDENTID")
    out = pd.DataFrame({"RESPONDENTID": ids})

    out["WISH_WHOLE_GRAINS"] = _score_protective_no_upper(whole_grains, 100.0, 125.0)
    out["WISH_VEGETABLES"] = _score_protective_no_upper(vegetables, 200.0, 300.0)
    out["WISH_FRUIT"] = _score_protective_no_upper(fruit, 100.0, 200.0)
    out["WISH_LEGUMES"] = _score_protective_no_upper(legumes, 0.0, 75.0)
    out["WISH_UNSATURATED_OILS"] = _score_protective_with_upper(unsaturated_oils, 20.0, 40.0, 80.0)
    out["WISH_FISH"] = _score_protective_with_upper(fish, 0.0, 28.0, 100.0)
    out["WISH_DAIRY"] = _score_protective_with_upper(dairy, 0.0, 250.0, 500.0)
    out["WISH_NUTS"] = _score_protective_with_upper(nuts, 0.0, 50.0, 75.0)
    out["WISH_POULTRY"] = _score_neutral(poultry, 29.0, 58.0)
    out["WISH_EGGS"] = _score_neutral(eggs, 13.0, 25.0)
    out["WISH_RED_MEAT"] = _score_limit(red_meat, 14.0, 28.0)
    out["WISH_SATURATED_OILS"] = _score_binary_limit(saturated_oils, 11.8)
    out["WISH_ADDED_SUGARS"] = _score_binary_limit(added_sugars, 31.0)

    healthy_cols = [
        "WISH_WHOLE_GRAINS",
        "WISH_VEGETABLES",
        "WISH_FRUIT",
        "WISH_LEGUMES",
        "WISH_UNSATURATED_OILS",
        "WISH_FISH",
        "WISH_DAIRY",
        "WISH_NUTS",
        "WISH_POULTRY",
        "WISH_EGGS",
    ]
    less_healthy_cols = [
        "WISH_RED_MEAT",
        "WISH_SATURATED_OILS",
        "WISH_ADDED_SUGARS",
    ]
    low_env_cols = [
        "WISH_WHOLE_GRAINS",
        "WISH_VEGETABLES",
        "WISH_FRUIT",
        "WISH_LEGUMES",
        "WISH_UNSATURATED_OILS",
        "WISH_ADDED_SUGARS",
    ]
    high_env_cols = [
        "WISH_FISH",
        "WISH_DAIRY",
        "WISH_POULTRY",
        "WISH_RED_MEAT",
        "WISH_SATURATED_OILS",
        "WISH_EGGS",
        "WISH_NUTS",
    ]

    out["WISH_HEALTHY"] = out[healthy_cols].sum(axis=1, min_count=len(healthy_cols))
    out["WISH_LESS_HEALTHY"] = out[less_healthy_cols].sum(axis=1, min_count=len(less_healthy_cols))
    out["WISH_LOW_ENV"] = out[low_env_cols].sum(axis=1, min_count=len(low_env_cols))
    out["WISH_HIGH_ENV"] = out[high_env_cols].sum(axis=1, min_count=len(high_env_cols))
    out["WISH_ALL"] = out["WISH_HEALTHY"] + out["WISH_LESS_HEALTHY"]
    return out
