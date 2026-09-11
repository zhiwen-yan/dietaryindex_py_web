"""Global Diet Quality Score (GDQS)."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _to_series(values) -> pd.Series:
    return pd.to_numeric(pd.Series(values), errors="coerce")


def _score_positive(values, low_cut: float, high_cut: float, low_points: float, high_points: float) -> pd.Series:
    series = _to_series(values)
    out = pd.Series(
        np.select(
            [
                series < low_cut,
                series <= high_cut,
                series > high_cut,
            ],
            [0.0, low_points, high_points],
            default=np.nan,
        ),
        index=series.index,
        dtype=float,
    )
    out[series.isna()] = np.nan
    return out


def _score_reverse(values, low_cut: float, high_cut: float) -> pd.Series:
    series = _to_series(values)
    out = pd.Series(
        np.select(
            [
                series < low_cut,
                series <= high_cut,
                series > high_cut,
            ],
            [2.0, 1.0, 0.0],
            default=np.nan,
        ),
        index=series.index,
        dtype=float,
    )
    out[series.isna()] = np.nan
    return out


def _score_high_fat_dairy(values) -> pd.Series:
    series = _to_series(values)
    out = pd.Series(
        np.select(
            [
                series < 35.0,
                series <= 142.0,
                series <= 734.0,
                series > 734.0,
            ],
            [0.0, 1.0, 2.0, 0.0],
            default=np.nan,
        ),
        index=series.index,
        dtype=float,
    )
    out[series.isna()] = np.nan
    return out


def _score_red_meat(values) -> pd.Series:
    series = _to_series(values)
    out = pd.Series(
        np.select(
            [
                series < 9.0,
                series <= 46.0,
                series > 46.0,
            ],
            [0.0, 1.0, 0.0],
            default=np.nan,
        ),
        index=series.index,
        dtype=float,
    )
    out[series.isna()] = np.nan
    return out


def compute_gdqs(
    data,
    respondent_id,
    citrus_fruits,
    deep_orange_fruits,
    other_fruits,
    dark_green_leafy_vegetables,
    cruciferous_vegetables,
    deep_orange_vegetables,
    other_vegetables,
    legumes,
    deep_orange_tubers,
    nuts_seeds,
    whole_grains,
    liquid_oils,
    fish_shellfish,
    poultry_game_meat,
    low_fat_dairy,
    eggs,
    high_fat_dairy,
    red_meat,
    processed_meat,
    refined_grains_baked_goods,
    sweets_ice_cream,
    sugar_sweetened_beverages,
    juice,
    white_roots_tubers,
    purchased_deep_fried_foods,
):
    """Compute the Global Diet Quality Score from daily food-group intakes in g/day."""

    ids = pd.Series(np.asarray(respondent_id), name="RESPONDENTID")
    out = pd.DataFrame({"RESPONDENTID": ids})

    out["GDQS_CITRUS_FRUITS"] = _score_positive(citrus_fruits, 24.0, 69.0, 1.0, 2.0)
    out["GDQS_DEEP_ORANGE_FRUITS"] = _score_positive(deep_orange_fruits, 25.0, 123.0, 1.0, 2.0)
    out["GDQS_OTHER_FRUITS"] = _score_positive(other_fruits, 27.0, 107.0, 1.0, 2.0)
    out["GDQS_DARK_GREEN_LEAFY_VEGETABLES"] = _score_positive(
        dark_green_leafy_vegetables, 13.0, 37.0, 2.0, 4.0
    )
    out["GDQS_CRUCIFEROUS_VEGETABLES"] = _score_positive(cruciferous_vegetables, 13.0, 36.0, 0.25, 0.5)
    out["GDQS_DEEP_ORANGE_VEGETABLES"] = _score_positive(deep_orange_vegetables, 9.0, 45.0, 0.25, 0.5)
    out["GDQS_OTHER_VEGETABLES"] = _score_positive(other_vegetables, 23.0, 114.0, 0.25, 0.5)
    out["GDQS_LEGUMES"] = _score_positive(legumes, 9.0, 42.0, 2.0, 4.0)
    out["GDQS_DEEP_ORANGE_TUBERS"] = _score_positive(deep_orange_tubers, 12.0, 63.0, 0.25, 0.5)
    out["GDQS_NUTS_SEEDS"] = _score_positive(nuts_seeds, 7.0, 13.0, 2.0, 4.0)
    out["GDQS_WHOLE_GRAINS"] = _score_positive(whole_grains, 8.0, 13.0, 1.0, 2.0)
    out["GDQS_LIQUID_OILS"] = _score_positive(liquid_oils, 2.0, 7.5, 1.0, 2.0)
    out["GDQS_FISH_SHELLFISH"] = _score_positive(fish_shellfish, 14.0, 71.0, 1.0, 2.0)
    out["GDQS_POULTRY_GAME_MEAT"] = _score_positive(poultry_game_meat, 16.0, 44.0, 1.0, 2.0)
    out["GDQS_LOW_FAT_DAIRY"] = _score_positive(low_fat_dairy, 33.0, 132.0, 1.0, 2.0)
    out["GDQS_EGGS"] = _score_positive(eggs, 6.0, 32.0, 1.0, 2.0)

    out["GDQS_HIGH_FAT_DAIRY"] = _score_high_fat_dairy(high_fat_dairy)
    out["GDQS_RED_MEAT"] = _score_red_meat(red_meat)
    out["GDQS_PROCESSED_MEAT"] = _score_reverse(processed_meat, 9.0, 30.0)
    out["GDQS_REFINED_GRAINS_BAKED_GOODS"] = _score_reverse(refined_grains_baked_goods, 7.0, 33.0)
    out["GDQS_SWEETS_ICE_CREAM"] = _score_reverse(sweets_ice_cream, 13.0, 37.0)
    out["GDQS_SUGAR_SWEETENED_BEVERAGES"] = _score_reverse(sugar_sweetened_beverages, 57.0, 180.0)
    out["GDQS_JUICE"] = _score_reverse(juice, 36.0, 144.0)
    out["GDQS_WHITE_ROOTS_TUBERS"] = _score_reverse(white_roots_tubers, 27.0, 107.0)
    out["GDQS_PURCHASED_DEEP_FRIED_FOODS"] = _score_reverse(purchased_deep_fried_foods, 9.0, 45.0)

    pos_cols = [
        "GDQS_CITRUS_FRUITS",
        "GDQS_DEEP_ORANGE_FRUITS",
        "GDQS_OTHER_FRUITS",
        "GDQS_DARK_GREEN_LEAFY_VEGETABLES",
        "GDQS_CRUCIFEROUS_VEGETABLES",
        "GDQS_DEEP_ORANGE_VEGETABLES",
        "GDQS_OTHER_VEGETABLES",
        "GDQS_LEGUMES",
        "GDQS_DEEP_ORANGE_TUBERS",
        "GDQS_NUTS_SEEDS",
        "GDQS_WHOLE_GRAINS",
        "GDQS_LIQUID_OILS",
        "GDQS_FISH_SHELLFISH",
        "GDQS_POULTRY_GAME_MEAT",
        "GDQS_LOW_FAT_DAIRY",
        "GDQS_EGGS",
    ]
    neg_cols = [
        "GDQS_HIGH_FAT_DAIRY",
        "GDQS_RED_MEAT",
        "GDQS_PROCESSED_MEAT",
        "GDQS_REFINED_GRAINS_BAKED_GOODS",
        "GDQS_SWEETS_ICE_CREAM",
        "GDQS_SUGAR_SWEETENED_BEVERAGES",
        "GDQS_JUICE",
        "GDQS_WHITE_ROOTS_TUBERS",
        "GDQS_PURCHASED_DEEP_FRIED_FOODS",
    ]

    out["GDQS_POS"] = out[pos_cols].sum(axis=1, min_count=len(pos_cols))
    out["GDQS_NEG"] = out[neg_cols].sum(axis=1, min_count=len(neg_cols))
    out["GDQS_ALL"] = out["GDQS_POS"] + out["GDQS_NEG"]
    return out
