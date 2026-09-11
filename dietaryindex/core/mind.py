"""MIND diet scoring."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _score_beneficial(values, low, high, *, low_inclusive=True, high_inclusive=True):
    v = pd.to_numeric(pd.Series(values), errors="coerce")
    high_match = v >= high if high_inclusive else v > high
    low_match = v >= low if low_inclusive else v > low
    res = np.select(
        [high_match, low_match],
        [1.0, 0.5],
        default=0.0,
    )
    return pd.Series(np.where(v.isna(), np.nan, res), dtype=float)


def _score_limited(values, low, high):
    v = pd.to_numeric(pd.Series(values), errors="coerce")
    res = np.select(
        [v < low, v < high],
        [1.0, 0.5],
        default=0.0,
    )
    return pd.Series(np.where(v.isna(), np.nan, res), dtype=float)


def compute_mind(
    data,
    respondent_id,
    green_leafy_vegetables,
    other_vegetables,
    nuts,
    berries,
    beans,
    whole_grains,
    fish,
    poultry,
    olive_oil_primary,
    wine,
    red_meats,
    butter_margarine,
    cheese,
    pastries_sweets,
    fried_fast_food,
):
    """Compute the 15-component MIND diet score.

    Expected units:
    - `other_vegetables`, `whole_grains`, `wine`: servings or glasses per day
    - all other food-frequency variables: servings per week
    - `olive_oil_primary`: 1 if olive oil is the primary cooking oil, else 0
    """

    ids = pd.Series(np.asarray(respondent_id), name="RESPONDENTID")
    out = pd.DataFrame({"RESPONDENTID": ids})

    # Morris et al. (2015), Table 1: <=2/wk scores 0 and >2 to <6/wk
    # scores 0.5.  Exact equality therefore belongs to the lower category.
    out["MIND_GREEN_LEAFY_VEG"] = _score_beneficial(
        green_leafy_vegetables,
        low=2.0,
        high=6.0,
        low_inclusive=False,
    )
    out["MIND_OTHER_VEG"] = _score_beneficial(other_vegetables, low=5.0 / 7.0, high=1.0)
    # The published middle band starts at one serving per month.  Inputs are
    # weekly frequencies, so the operationalized lower boundary is 0.25/wk.
    out["MIND_NUTS"] = _score_beneficial(nuts, low=0.25, high=5.0)
    out["MIND_BERRIES"] = _score_beneficial(berries, low=1.0, high=2.0)
    out["MIND_BEANS"] = _score_beneficial(
        beans,
        low=1.0,
        high=3.0,
        high_inclusive=False,
    )
    out["MIND_WHOLE_GRAINS"] = _score_beneficial(whole_grains, low=1.0, high=3.0)
    out["MIND_FISH"] = _score_beneficial(fish, low=0.25, high=1.0)
    out["MIND_POULTRY"] = _score_beneficial(poultry, low=1.0, high=2.0)

    olive = pd.to_numeric(pd.Series(olive_oil_primary), errors="coerce")
    out["MIND_OLIVE_OIL"] = pd.Series(np.where(olive.isna(), np.nan, np.where(olive >= 1, 1.0, 0.0)), dtype=float)

    wine_series = pd.to_numeric(pd.Series(wine), errors="coerce")
    # Wine is entered as glasses/day.  The original table awards 1 point only
    # at exactly one glass/day, 0.5 for one glass/month through six/week, and
    # 0 for rarer intake, abstention, or more than one glass/day.
    one_glass_per_month_daily = 1.0 / 28.0
    res_wine = np.select(
        [wine_series == 1.0, (wine_series >= one_glass_per_month_daily) & (wine_series < 1.0)],
        [1.0, 0.5],
        default=0.0,
    )
    out["MIND_WINE"] = pd.Series(np.where(wine_series.isna(), np.nan, res_wine), dtype=float)

    out["MIND_RED_MEATS"] = _score_limited(red_meats, low=4.0, high=7.0)
    butter = pd.to_numeric(pd.Series(butter_margarine), errors="coerce")
    butter_score = np.select(
        [butter < 1.0, butter <= 2.0],
        [1.0, 0.5],
        default=0.0,
    )
    out["MIND_BUTTER_MARGARINE"] = pd.Series(
        np.where(butter.isna(), np.nan, butter_score),
        dtype=float,
    )
    out["MIND_CHEESE"] = _score_limited(cheese, low=1.0, high=7.0)
    out["MIND_PASTRIES_SWEETS"] = _score_limited(pastries_sweets, low=5.0, high=7.0)
    out["MIND_FRIED_FAST_FOOD"] = _score_limited(fried_fast_food, low=1.0, high=4.0)

    comp_cols = [col for col in out.columns if col.startswith("MIND_")]
    # MIND is a fixed 15-component score.  A partial sum is not comparable to
    # the published 0-15 scale, so keep the total missing until every
    # component is available.
    out["MIND_ALL"] = out[comp_cols].sum(axis=1, min_count=len(comp_cols))
    return out
