"""Empirical Dietary Inflammatory Index (EDII).

Primary source:
Tabung FK, Smith-Warner SA, Chavarro JE, et al. Development and Validation of
an Empirical Dietary Inflammatory Index. J Nutr. 2016;146(8):1560-1570.

The published EDII is a food-based score:
1. Multiply each of 18 food-group intakes by its published coefficient.
2. Sum the weighted values.
3. Divide the total by 1000 for interpretability.

Inputs are expected as servings/day aligned to the paper's food-group
definitions.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from dietaryindex.reference.edii_reference import (
    EDII_COMPONENT_OUTPUT_NAMES,
    EDII_REFERENCE,
    EDII_VARIABLE_ORDER,
)


def _to_series(values, *, length: int | None = None) -> pd.Series:
    series = pd.Series(values, dtype="float64").reset_index(drop=True)
    if length is not None and len(series) != length:
        raise ValueError("All EDII input arrays must have the same length.")
    return series


def compute_edii(
    data,
    respondent_id,
    processed_meat,
    red_meat,
    organ_meat,
    other_fish,
    other_vegetables,
    refined_grains,
    high_energy_beverages,
    low_energy_beverages,
    tomatoes,
    beer,
    wine,
    tea,
    coffee,
    dark_yellow_vegetables,
    leafy_green_vegetables,
    snacks,
    fruit_juice,
    pizza,
):
    """Compute the empirical dietary inflammatory index (EDII)."""

    values_df = pd.DataFrame(
        {
            "processed_meat": _to_series(processed_meat),
            "red_meat": _to_series(red_meat),
            "organ_meat": _to_series(organ_meat),
            "other_fish": _to_series(other_fish),
            "other_vegetables": _to_series(other_vegetables),
            "refined_grains": _to_series(refined_grains),
            "high_energy_beverages": _to_series(high_energy_beverages),
            "low_energy_beverages": _to_series(low_energy_beverages),
            "tomatoes": _to_series(tomatoes),
            "beer": _to_series(beer),
            "wine": _to_series(wine),
            "tea": _to_series(tea),
            "coffee": _to_series(coffee),
            "dark_yellow_vegetables": _to_series(dark_yellow_vegetables),
            "leafy_green_vegetables": _to_series(leafy_green_vegetables),
            "snacks": _to_series(snacks),
            "fruit_juice": _to_series(fruit_juice),
            "pizza": _to_series(pizza),
        }
    )

    result = pd.DataFrame({"RESPONDENTID": np.asarray(respondent_id)})
    contribution_cols: list[str] = []

    for component in EDII_VARIABLE_ORDER:
        output_name = f"EDII_{EDII_COMPONENT_OUTPUT_NAMES[component]}"
        result[output_name] = values_df[component] * EDII_REFERENCE[component]["weight"] / 1000.0
        contribution_cols.append(output_name)

    # E-DII has a fixed 18-food-group definition.  Do not silently rescale a
    # partial row by treating missing groups as zero intake.
    result["EDII_ALL"] = result[contribution_cols].sum(
        axis=1, min_count=len(contribution_cols)
    )
    ordered_cols = ["RESPONDENTID", "EDII_ALL"] + contribution_cols
    return result[ordered_cols]


__all__ = ["compute_edii"]
