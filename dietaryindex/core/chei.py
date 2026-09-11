"""Chinese Healthy Eating Index (CHEI)."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _score_linear_positive(values, max_points, target):
    values = pd.to_numeric(pd.Series(values), errors="coerce")
    return np.clip(values / target * max_points, 0.0, max_points)


def _score_linear_moderation(values, max_points, best, worst):
    values = pd.to_numeric(pd.Series(values), errors="coerce")
    score = np.where(
        values <= best,
        max_points,
        np.where(
            values >= worst,
            0.0,
            (worst - values) / (worst - best) * max_points,
        ),
    )
    return score


def compute_chei(
    data,
    respondent_id,
    gender,
    total_grains,
    whole_grains_mixed_beans,
    tubers,
    total_vegetables,
    dark_vegetables,
    fruits,
    dairy,
    soybeans,
    fish_seafood,
    poultry,
    eggs,
    seeds_nuts,
    red_meat,
    cooking_oils,
    sodium,
    added_sugars_pct_energy,
    alcohol,
):
    """Compute CHEI from density-standardized component inputs.

    Expected units:
    - food groups: standard portions per 1000 kcal
    - cooking oils: g per 1000 kcal
    - sodium: mg per 1000 kcal
    - added_sugars_pct_energy: percent of total energy
    - alcohol: g/day
    """

    ids = pd.Series(np.asarray(respondent_id), name="RESPONDENTID")
    gender_series = pd.to_numeric(pd.Series(gender), errors="coerce")
    out = pd.DataFrame({"RESPONDENTID": ids})

    out["CHEI_TOTAL_GRAINS"] = _score_linear_positive(total_grains, 5.0, 2.5)
    out["CHEI_WHOLE_GRAINS_MIXED_BEANS"] = _score_linear_positive(whole_grains_mixed_beans, 5.0, 0.6)
    out["CHEI_TUBERS"] = _score_linear_positive(tubers, 5.0, 0.3)
    out["CHEI_TOTAL_VEGETABLES"] = _score_linear_positive(total_vegetables, 5.0, 1.9)
    out["CHEI_DARK_VEGETABLES"] = _score_linear_positive(dark_vegetables, 5.0, 0.9)
    out["CHEI_FRUITS"] = _score_linear_positive(fruits, 10.0, 1.1)
    out["CHEI_DAIRY"] = _score_linear_positive(dairy, 5.0, 0.5)
    out["CHEI_SOYBEANS"] = _score_linear_positive(soybeans, 5.0, 0.4)
    out["CHEI_FISH_SEAFOOD"] = _score_linear_positive(fish_seafood, 5.0, 0.6)
    out["CHEI_POULTRY"] = _score_linear_positive(poultry, 5.0, 0.3)
    out["CHEI_EGGS"] = _score_linear_positive(eggs, 5.0, 0.5)
    out["CHEI_SEEDS_NUTS"] = _score_linear_positive(seeds_nuts, 5.0, 0.4)

    out["CHEI_RED_MEAT"] = _score_linear_moderation(red_meat, 5.0, 0.4, 3.5)
    out["CHEI_COOKING_OILS"] = _score_linear_moderation(cooking_oils, 10.0, 15.6, 32.6)
    out["CHEI_SODIUM"] = _score_linear_moderation(sodium, 10.0, 1000.0, 3608.0)
    out["CHEI_ADDED_SUGARS"] = _score_linear_moderation(added_sugars_pct_energy, 5.0, 10.0, 20.0)

    alcohol_series = pd.to_numeric(pd.Series(alcohol), errors="coerce")
    alcohol_best = np.where(gender_series == 1, 25.0, 15.0)
    alcohol_worst = np.where(gender_series == 1, 60.0, 40.0)
    alcohol_score = np.where(
        alcohol_series <= alcohol_best,
        5.0,
        np.where(
            alcohol_series >= alcohol_worst,
            0.0,
            (alcohol_worst - alcohol_series) / (alcohol_worst - alcohol_best) * 5.0,
        ),
    )
    out["CHEI_ALCOHOL"] = np.where(
        alcohol_series.isna() | ~gender_series.isin([1, 2]),
        np.nan,
        alcohol_score,
    )

    comp_cols = [col for col in out.columns if col.startswith("CHEI_")]
    # CHEI is a fixed 17-component score; partial sums are not on the same
    # 0-100 scale and therefore must remain missing.
    out["CHEI_ALL"] = out[comp_cols].sum(axis=1, min_count=len(comp_cols))
    return out
