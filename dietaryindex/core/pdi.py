"""Plant-based diet indices: PDI, hPDI, and uPDI.

Primary source:
Satija A, Bhupathiraju SN, Rimm EB, et al. Plant-Based Dietary Patterns and
Incidence of Type 2 Diabetes in US Men and Women: Results From Three
Prospective Cohort Studies. PLoS Med. 2016;13(6):e1002039.

The original papers score 18 food groups into quintiles. Higher quintiles
receive 5 points for positively scored groups and 1 point for reversely scored
groups. Energy-adjusted intakes are preferred when reproducing the published
analyses, but the implementation itself accepts any internally consistent
continuous intake unit and ranks the sample by quintiles.
"""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd

from dietaryindex.core._scoring import fit_reference_cutoffs, score_series_with_reference


HEALTHY_PLANT_GROUPS = (
    "whole_grain",
    "fruit",
    "vegetable",
    "nuts",
    "legumes",
    "vegetable_oil",
    "tea_coffee",
)

LESS_HEALTHY_PLANT_GROUPS = (
    "fruit_juice",
    "refined_grain",
    "potatoes",
    "ssb",
    "sweets_desserts",
)

ANIMAL_GROUPS = (
    "animal_fat",
    "dairy",
    "eggs",
    "fish_seafood",
    "meat",
    "misc_animal_based",
)

PDI_FOOD_GROUPS = HEALTHY_PLANT_GROUPS + LESS_HEALTHY_PLANT_GROUPS + ANIMAL_GROUPS

PDI_SCHEME_DEFINITIONS = {
    "pdi": {
        "prefix": "PDI",
        "positive_groups": HEALTHY_PLANT_GROUPS + LESS_HEALTHY_PLANT_GROUPS,
        "negative_groups": ANIMAL_GROUPS,
    },
    "hpdi": {
        "prefix": "HPDI",
        "positive_groups": HEALTHY_PLANT_GROUPS,
        "negative_groups": LESS_HEALTHY_PLANT_GROUPS + ANIMAL_GROUPS,
    },
    "updi": {
        "prefix": "UPDI",
        "positive_groups": LESS_HEALTHY_PLANT_GROUPS,
        "negative_groups": HEALTHY_PLANT_GROUPS + ANIMAL_GROUPS,
    },
}

PDI_COMPONENT_OUTPUT_NAMES = {
    "whole_grain": "WHOLE_GRAIN",
    "fruit": "FRUIT",
    "vegetable": "VEGETABLE",
    "nuts": "NUTS",
    "legumes": "LEGUMES",
    "vegetable_oil": "VEGETABLE_OIL",
    "tea_coffee": "TEA_COFFEE",
    "fruit_juice": "FRUIT_JUICE",
    "refined_grain": "REFINED_GRAIN",
    "potatoes": "POTATOES",
    "ssb": "SSB",
    "sweets_desserts": "SWEETS_DESSERTS",
    "animal_fat": "ANIMAL_FAT",
    "dairy": "DAIRY",
    "eggs": "EGGS",
    "fish_seafood": "FISH_SEAFOOD",
    "meat": "MEAT",
    "misc_animal_based": "MISC_ANIMAL",
}


def _normalize_group_input(strata, length: int):
    if strata is None:
        return None
    if isinstance(strata, pd.Series):
        return strata.reset_index(drop=True)
    if isinstance(strata, pd.DataFrame):
        return strata.reset_index(drop=True)
    if isinstance(strata, Mapping):
        return pd.DataFrame(strata).reset_index(drop=True)

    arr = np.asarray(strata)
    if arr.ndim == 1:
        if len(arr) != length:
            raise ValueError("Length of strata must match the number of observations.")
        return pd.Series(arr, name="strata")
    if arr.ndim == 2:
        if arr.shape[0] != length:
            raise ValueError("Number of rows in strata must match the number of observations.")
        cols = [f"strata_{i + 1}" for i in range(arr.shape[1])]
        return pd.DataFrame(arr, columns=cols)
    raise TypeError("strata must be None, a Series, a DataFrame, a mapping, or a 1D/2D array.")


def _build_reference_frame(values_df: pd.DataFrame, strata=None) -> tuple[pd.DataFrame, list[str]]:
    group_obj = _normalize_group_input(strata, len(values_df))
    if group_obj is None:
        return values_df.copy(), []
    if isinstance(group_obj, pd.Series):
        group_df = group_obj.to_frame(name=group_obj.name or "strata")
    else:
        group_df = group_obj.copy()
        if any(col is None for col in group_df.columns):
            group_df.columns = [f"strata_{i + 1}" for i in range(group_df.shape[1])]
    return pd.concat([group_df.reset_index(drop=True), values_df.reset_index(drop=True)], axis=1), list(group_df.columns)


def _compute_plant_based_index(
    scheme_key: str,
    *,
    respondent_id,
    values_df: pd.DataFrame,
    reference=None,
    strata=None,
) -> pd.DataFrame:
    scheme = PDI_SCHEME_DEFINITIONS[scheme_key]
    prefix = scheme["prefix"]

    reference_group = _normalize_group_input(strata, len(values_df))
    if reference is None:
        reference_input, group_cols = _build_reference_frame(values_df, strata=strata)
        groupby = group_cols or None
        reference = fit_reference_cutoffs(
            reference_input,
            columns=list(PDI_FOOD_GROUPS),
            method="quintile",
            groupby=groupby,
        )

    result = pd.DataFrame({"RESPONDENTID": np.asarray(respondent_id)})
    total = np.zeros(len(values_df), dtype=float)

    for group_name in PDI_FOOD_GROUPS:
        direction = "healthy" if group_name in scheme["positive_groups"] else "unhealthy"
        scores = score_series_with_reference(
            values_df[group_name],
            reference,
            variable=group_name,
            direction=direction,
            group=reference_group,
        )
        output_name = f"{prefix}_{PDI_COMPONENT_OUTPUT_NAMES[group_name]}"
        result[output_name] = scores
        total = total + np.asarray(scores, dtype=float)

    result[f"{prefix}_ALL"] = total
    ordered_cols = ["RESPONDENTID", f"{prefix}_ALL"] + [
        f"{prefix}_{PDI_COMPONENT_OUTPUT_NAMES[group_name]}" for group_name in PDI_FOOD_GROUPS
    ]
    return result[ordered_cols]


def compute_pdi(
    data,
    respondent_id,
    whole_grain,
    fruit,
    vegetable,
    nuts,
    legumes,
    vegetable_oil,
    tea_coffee,
    fruit_juice,
    refined_grain,
    potatoes,
    ssb,
    sweets_desserts,
    animal_fat,
    dairy,
    eggs,
    fish_seafood,
    meat,
    misc_animal_based,
    reference=None,
    strata=None,
):
    """Compute the overall plant-based diet index (PDI).

    Parameters
    ----------
    reference:
        Optional long-format reference-cutoff table generated by
        ``fit_reference_cutoffs``. When omitted, quintiles are estimated from
        the supplied sample.
    strata:
        Optional grouping variable(s) used to fit or apply stratified quintile
        references, for example sex-specific scoring.
    """

    values_df = pd.DataFrame(
        {
            "whole_grain": np.asarray(whole_grain, dtype=float),
            "fruit": np.asarray(fruit, dtype=float),
            "vegetable": np.asarray(vegetable, dtype=float),
            "nuts": np.asarray(nuts, dtype=float),
            "legumes": np.asarray(legumes, dtype=float),
            "vegetable_oil": np.asarray(vegetable_oil, dtype=float),
            "tea_coffee": np.asarray(tea_coffee, dtype=float),
            "fruit_juice": np.asarray(fruit_juice, dtype=float),
            "refined_grain": np.asarray(refined_grain, dtype=float),
            "potatoes": np.asarray(potatoes, dtype=float),
            "ssb": np.asarray(ssb, dtype=float),
            "sweets_desserts": np.asarray(sweets_desserts, dtype=float),
            "animal_fat": np.asarray(animal_fat, dtype=float),
            "dairy": np.asarray(dairy, dtype=float),
            "eggs": np.asarray(eggs, dtype=float),
            "fish_seafood": np.asarray(fish_seafood, dtype=float),
            "meat": np.asarray(meat, dtype=float),
            "misc_animal_based": np.asarray(misc_animal_based, dtype=float),
        }
    )
    return _compute_plant_based_index(
        "pdi",
        respondent_id=respondent_id,
        values_df=values_df,
        reference=reference,
        strata=strata,
    )


def compute_hpdi(
    data,
    respondent_id,
    whole_grain,
    fruit,
    vegetable,
    nuts,
    legumes,
    vegetable_oil,
    tea_coffee,
    fruit_juice,
    refined_grain,
    potatoes,
    ssb,
    sweets_desserts,
    animal_fat,
    dairy,
    eggs,
    fish_seafood,
    meat,
    misc_animal_based,
    reference=None,
    strata=None,
):
    """Compute the healthy plant-based diet index (hPDI)."""

    values_df = pd.DataFrame(
        {
            "whole_grain": np.asarray(whole_grain, dtype=float),
            "fruit": np.asarray(fruit, dtype=float),
            "vegetable": np.asarray(vegetable, dtype=float),
            "nuts": np.asarray(nuts, dtype=float),
            "legumes": np.asarray(legumes, dtype=float),
            "vegetable_oil": np.asarray(vegetable_oil, dtype=float),
            "tea_coffee": np.asarray(tea_coffee, dtype=float),
            "fruit_juice": np.asarray(fruit_juice, dtype=float),
            "refined_grain": np.asarray(refined_grain, dtype=float),
            "potatoes": np.asarray(potatoes, dtype=float),
            "ssb": np.asarray(ssb, dtype=float),
            "sweets_desserts": np.asarray(sweets_desserts, dtype=float),
            "animal_fat": np.asarray(animal_fat, dtype=float),
            "dairy": np.asarray(dairy, dtype=float),
            "eggs": np.asarray(eggs, dtype=float),
            "fish_seafood": np.asarray(fish_seafood, dtype=float),
            "meat": np.asarray(meat, dtype=float),
            "misc_animal_based": np.asarray(misc_animal_based, dtype=float),
        }
    )
    return _compute_plant_based_index(
        "hpdi",
        respondent_id=respondent_id,
        values_df=values_df,
        reference=reference,
        strata=strata,
    )


def compute_updi(
    data,
    respondent_id,
    whole_grain,
    fruit,
    vegetable,
    nuts,
    legumes,
    vegetable_oil,
    tea_coffee,
    fruit_juice,
    refined_grain,
    potatoes,
    ssb,
    sweets_desserts,
    animal_fat,
    dairy,
    eggs,
    fish_seafood,
    meat,
    misc_animal_based,
    reference=None,
    strata=None,
):
    """Compute the unhealthy plant-based diet index (uPDI)."""

    values_df = pd.DataFrame(
        {
            "whole_grain": np.asarray(whole_grain, dtype=float),
            "fruit": np.asarray(fruit, dtype=float),
            "vegetable": np.asarray(vegetable, dtype=float),
            "nuts": np.asarray(nuts, dtype=float),
            "legumes": np.asarray(legumes, dtype=float),
            "vegetable_oil": np.asarray(vegetable_oil, dtype=float),
            "tea_coffee": np.asarray(tea_coffee, dtype=float),
            "fruit_juice": np.asarray(fruit_juice, dtype=float),
            "refined_grain": np.asarray(refined_grain, dtype=float),
            "potatoes": np.asarray(potatoes, dtype=float),
            "ssb": np.asarray(ssb, dtype=float),
            "sweets_desserts": np.asarray(sweets_desserts, dtype=float),
            "animal_fat": np.asarray(animal_fat, dtype=float),
            "dairy": np.asarray(dairy, dtype=float),
            "eggs": np.asarray(eggs, dtype=float),
            "fish_seafood": np.asarray(fish_seafood, dtype=float),
            "meat": np.asarray(meat, dtype=float),
            "misc_animal_based": np.asarray(misc_animal_based, dtype=float),
        }
    )
    return _compute_plant_based_index(
        "updi",
        respondent_id=respondent_id,
        values_df=values_df,
        reference=reference,
        strata=strata,
    )
