"""Diet Balance Index-07 (adult 2000-kcal standard release)."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _to_series(values) -> pd.Series:
    return pd.to_numeric(pd.Series(values), errors="coerce")


def _select(series: pd.Series, conditions, scores) -> pd.Series:
    values = np.select(conditions, scores, default=np.nan).astype(float)
    return pd.Series(values, index=series.index)


def _fill_missing_or_default(scored: pd.Series, source: pd.Series, default: float) -> pd.Series:
    out = scored.copy()
    out.loc[~source.isna() & out.isna()] = default
    return out


def _score_cereals(values) -> pd.Series:
    series = _to_series(values)
    score = pd.Series(0.0, index=series.index)
    negative_steps = np.ceil((275.0 - series) / 50.0)
    positive_steps = np.ceil((series - 325.0) / 50.0)
    score = pd.Series(
        np.where(
            series < 275.0,
            -2.0 * np.clip(negative_steps, 0.0, 6.0),
            np.where(series > 325.0, 2.0 * np.clip(positive_steps, 0.0, 6.0), 0.0),
        ),
        index=series.index,
        dtype=float,
    )
    score[series.isna()] = np.nan
    return score


def _score_vegetables(values) -> pd.Series:
    series = _to_series(values)
    return _fill_missing_or_default(
        _select(
            series,
            [series >= 350.0, series >= 175.0, series > 0.0],
            [0.0, -2.0, -4.0],
        ),
        series,
        -6.0,
    )


def _score_fruits(values) -> pd.Series:
    series = _to_series(values)
    return _fill_missing_or_default(
        _select(
            series,
            [series >= 300.0, series >= 150.0, series > 0.0],
            [0.0, -2.0, -4.0],
        ),
        series,
        -6.0,
    )


def _score_dairy(values) -> pd.Series:
    series = _to_series(values)
    return _fill_missing_or_default(
        _select(
            series,
            [series >= 300.0, series >= 200.0, series >= 100.0],
            [0.0, -2.0, -4.0],
        ),
        series,
        -6.0,
    )


def _score_soybean(values) -> pd.Series:
    series = _to_series(values)
    return _fill_missing_or_default(
        _select(
            series,
            [series >= 40.0, series >= 20.0, series >= 1.0],
            [0.0, -2.0, -4.0],
        ),
        series,
        -6.0,
    )


def _score_meat(values) -> pd.Series:
    series = _to_series(values)
    return _select(
        series,
        [series < 1.0, series < 25.0, series <= 75.0, series < 125.0, series >= 125.0],
        [-4.0, -2.0, 0.0, 2.0, 4.0],
    )


def _score_fish_shrimp(values) -> pd.Series:
    series = _to_series(values)
    return _select(
        series,
        [series >= 75.0, series >= 60.0, series >= 45.0, series >= 30.0, series < 30.0],
        [0.0, -1.0, -2.0, -3.0, -4.0],
    )


def _score_egg(values) -> pd.Series:
    series = _to_series(values)
    return _select(
        series,
        [series < 1.0, series < 25.0, series <= 50.0, series < 75.0, series >= 75.0],
        [-4.0, -2.0, 0.0, 2.0, 4.0],
    )


def _score_oil(values) -> pd.Series:
    series = _to_series(values)
    return _select(
        series,
        [series <= 25.0, series <= 50.0, series > 50.0],
        [0.0, 2.0, 4.0],
    )


def _score_salt(values) -> pd.Series:
    series = _to_series(values)
    return _select(
        series,
        [series <= 6.0, series <= 12.0, series > 12.0],
        [0.0, 2.0, 4.0],
    )


def _score_alcohol(values, gender) -> pd.Series:
    alcohol = _to_series(values)
    gender_series = _to_series(gender)

    score = pd.Series(np.nan, index=alcohol.index, dtype=float)
    male_mask = gender_series == 1
    female_mask = gender_series == 2

    score.loc[male_mask] = np.select(
        [
            alcohol.loc[male_mask] <= 25.0,
            alcohol.loc[male_mask] <= 50.0,
            alcohol.loc[male_mask] <= 75.0,
            alcohol.loc[male_mask] <= 100.0,
            alcohol.loc[male_mask] > 100.0,
        ],
        [0.0, 1.0, 2.0, 3.0, 4.0],
        default=np.nan,
    ).astype(float)
    score.loc[female_mask] = np.select(
        [
            alcohol.loc[female_mask] <= 15.0,
            alcohol.loc[female_mask] <= 30.0,
            alcohol.loc[female_mask] <= 45.0,
            alcohol.loc[female_mask] <= 60.0,
            alcohol.loc[female_mask] > 60.0,
        ],
        [0.0, 1.0, 2.0, 3.0, 4.0],
        default=np.nan,
    ).astype(float)
    return score


def _score_water(values) -> pd.Series:
    series = _to_series(values)
    deficit_steps = np.ceil(np.maximum(0.0, 1200.0 - series) / 100.0)
    score = np.where(series >= 1200.0, 0.0, -np.clip(deficit_steps, 0.0, 12.0))
    out = pd.Series(score, index=series.index, dtype=float)
    out[series.isna()] = np.nan
    return out


def _variety_flag(values, threshold: float) -> pd.Series:
    series = _to_series(values)
    out = pd.Series(np.where(series > threshold, 0.0, -1.0), index=series.index, dtype=float)
    out[series.isna()] = np.nan
    return out


def compute_dbi(
    data,
    respondent_id,
    gender,
    cereals,
    vegetables,
    fruits,
    dairy,
    soybean,
    meat,
    fish_shrimp,
    egg,
    oil,
    salt,
    alcohol,
    water,
    rice_products,
    wheat_products,
    coarse_grains_tubers,
    dark_vegetables,
    light_vegetables,
    red_meat_products,
    poultry_game,
):
    """Compute DBI-07 using the published adult 2000-kcal standard table.

    Expected units:
    - all food groups except water: g/day
    - water: mL/day
    - alcohol: g/day
    - gender: 1=male, 2=female
    """

    ids = pd.Series(np.asarray(respondent_id), name="RESPONDENTID")
    out = pd.DataFrame({"RESPONDENTID": ids})

    out["DBI_CEREALS"] = _score_cereals(cereals)
    out["DBI_VEGETABLES"] = _score_vegetables(vegetables)
    out["DBI_FRUITS"] = _score_fruits(fruits)
    out["DBI_DAIRY"] = _score_dairy(dairy)
    out["DBI_SOYBEAN"] = _score_soybean(soybean)
    out["DBI_MEAT"] = _score_meat(meat)
    out["DBI_FISH_SHRIMP"] = _score_fish_shrimp(fish_shrimp)
    out["DBI_EGG"] = _score_egg(egg)
    out["DBI_OIL"] = _score_oil(oil)
    out["DBI_SALT"] = _score_salt(salt)
    out["DBI_ALCOHOL"] = _score_alcohol(alcohol, gender)
    out["DBI_WATER"] = _score_water(water)

    variety_parts = pd.concat(
        [
            _variety_flag(rice_products, 25.0).rename("RICE"),
            _variety_flag(wheat_products, 25.0).rename("WHEAT"),
            _variety_flag(coarse_grains_tubers, 25.0).rename("COARSE_GRAINS_TUBERS"),
            _variety_flag(dark_vegetables, 25.0).rename("DARK_VEGETABLES"),
            _variety_flag(light_vegetables, 25.0).rename("LIGHT_VEGETABLES"),
            _variety_flag(fruits, 25.0).rename("FRUITS"),
            _variety_flag(soybean, 5.0).rename("SOYBEAN"),
            _variety_flag(dairy, 25.0).rename("DAIRY"),
            _variety_flag(red_meat_products, 25.0).rename("RED_MEAT_PRODUCTS"),
            _variety_flag(poultry_game, 25.0).rename("POULTRY_GAME"),
            _variety_flag(egg, 25.0).rename("EGG"),
            _variety_flag(fish_shrimp, 25.0).rename("FISH_SHRIMP"),
        ],
        axis=1,
    )
    out["DBI_DIET_VARIETY"] = variety_parts.sum(axis=1, min_count=variety_parts.shape[1])

    component_cols = [
        "DBI_CEREALS",
        "DBI_VEGETABLES",
        "DBI_FRUITS",
        "DBI_DAIRY",
        "DBI_SOYBEAN",
        "DBI_MEAT",
        "DBI_FISH_SHRIMP",
        "DBI_EGG",
        "DBI_OIL",
        "DBI_SALT",
        "DBI_ALCOHOL",
        "DBI_DIET_VARIETY",
        "DBI_WATER",
    ]

    component_frame = out[component_cols]
    out["DBI_TS"] = component_frame.sum(axis=1, min_count=len(component_cols))
    out["DBI_HBS"] = component_frame.clip(lower=0.0).sum(axis=1, min_count=len(component_cols))
    out["DBI_LBS"] = (-component_frame.clip(upper=0.0)).sum(axis=1, min_count=len(component_cols))
    out["DBI_DQD"] = component_frame.abs().sum(axis=1, min_count=len(component_cols))
    return out
