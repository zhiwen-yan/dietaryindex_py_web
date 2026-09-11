"""Oxidative Balance Score (OBS).

Implementation choice:
This module implements a published NHANES-style 20-component OBS that combines
16 dietary factors with 4 lifestyle factors. Dietary, BMI, and cotinine
components are scored by sex-specific tertiles, while physical activity and
alcohol use follow the explicit category rules described in the source paper.

Primary source:
Chen X, Wu Z, Hou X, et al. Association of the oxidative balance score and
chronic kidney disease: insights from the National Health and Nutrition
Examination Survey 2009-2018. Front Nutr. 2024;11:1429191.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from dietaryindex.core._scoring import fit_reference_cutoffs, score_series_with_reference


OBS_ANTIOX_TERTILE_COMPONENTS = (
    "fiber",
    "carotene_re",
    "vitamin_b2",
    "niacin",
    "total_folate",
    "calcium",
    "zinc",
    "magnesium",
    "copper",
    "selenium",
    "vitamin_b6",
    "vitamin_b12",
    "vitamin_c",
    "vitamin_e",
)

OBS_DIET_PROOX_TERTILE_COMPONENTS = (
    "iron",
    "total_fat",
)

OBS_LIFESTYLE_TERTILE_COMPONENTS = (
    "bmi",
    "cotinine",
)

OBS_COMPONENT_OUTPUT_NAMES = {
    "fiber": "FIBER",
    "carotene_re": "CAROTENE_RE",
    "vitamin_b2": "VITAMIN_B2",
    "niacin": "NIACIN",
    "total_folate": "TOTAL_FOLATE",
    "calcium": "CALCIUM",
    "zinc": "ZINC",
    "magnesium": "MAGNESIUM",
    "copper": "COPPER",
    "selenium": "SELENIUM",
    "vitamin_b6": "VITAMIN_B6",
    "vitamin_b12": "VITAMIN_B12",
    "vitamin_c": "VITAMIN_C",
    "vitamin_e": "VITAMIN_E",
    "iron": "IRON",
    "total_fat": "TOTAL_FAT",
    "bmi": "BMI",
    "cotinine": "COTININE",
    "physical_activity_met": "PHYSICAL_ACTIVITY",
    "alcohol": "ALCOHOL",
}


def _score_physical_activity(values) -> np.ndarray:
    arr = pd.to_numeric(pd.Series(values), errors="coerce").to_numpy(dtype=float)
    # Published categories: <600, 600-<3,000, and >=3,000 MET-min/week.
    score = np.where(arr >= 3000.0, 2.0, np.where(arr >= 600.0, 1.0, 0.0))
    score[np.isnan(arr)] = np.nan
    return score


def _score_alcohol(gender, drinks_per_day, drinks_per_year) -> np.ndarray:
    sex = pd.to_numeric(pd.Series(gender), errors="coerce").to_numpy(dtype=float)
    day = pd.to_numeric(pd.Series(drinks_per_day), errors="coerce").to_numpy(dtype=float)
    year = pd.to_numeric(pd.Series(drinks_per_year), errors="coerce").to_numpy(dtype=float)

    score = np.full(len(sex), np.nan, dtype=float)
    valid = ~np.isnan(sex) & ~np.isnan(day) & ~np.isnan(year)

    non_drinker = valid & (year < 12.0)
    male_non_heavy = valid & (sex == 1) & (year >= 12.0) & (day < 2.0)
    female_non_heavy = valid & (sex == 2) & (year >= 12.0) & (day < 1.0)
    heavy = valid & ~(non_drinker | male_non_heavy | female_non_heavy)

    score[non_drinker] = 2.0
    score[male_non_heavy | female_non_heavy] = 1.0
    score[heavy] = 0.0
    return score


def compute_obs(
    data,
    respondent_id,
    gender,
    fiber,
    carotene_re,
    vitamin_b2,
    niacin,
    total_folate,
    calcium,
    zinc,
    magnesium,
    copper,
    selenium,
    vitamin_b6,
    vitamin_b12,
    vitamin_c,
    vitamin_e,
    iron,
    total_fat,
    bmi,
    cotinine,
    physical_activity_met,
    alcohol_drinks_per_day,
    alcohol_drinks_per_year,
    reference=None,
):
    """Compute a 20-component oxidative balance score."""

    gender_series = pd.Series(np.asarray(gender), name="gender")
    tertile_df = pd.DataFrame(
        {
            "fiber": np.asarray(fiber, dtype=float),
            "carotene_re": np.asarray(carotene_re, dtype=float),
            "vitamin_b2": np.asarray(vitamin_b2, dtype=float),
            "niacin": np.asarray(niacin, dtype=float),
            "total_folate": np.asarray(total_folate, dtype=float),
            "calcium": np.asarray(calcium, dtype=float),
            "zinc": np.asarray(zinc, dtype=float),
            "magnesium": np.asarray(magnesium, dtype=float),
            "copper": np.asarray(copper, dtype=float),
            "selenium": np.asarray(selenium, dtype=float),
            "vitamin_b6": np.asarray(vitamin_b6, dtype=float),
            "vitamin_b12": np.asarray(vitamin_b12, dtype=float),
            "vitamin_c": np.asarray(vitamin_c, dtype=float),
            "vitamin_e": np.asarray(vitamin_e, dtype=float),
            "iron": np.asarray(iron, dtype=float),
            "total_fat": np.asarray(total_fat, dtype=float),
            "bmi": np.asarray(bmi, dtype=float),
            "cotinine": np.asarray(cotinine, dtype=float),
        }
    )

    if reference is None:
        reference_input = pd.concat([gender_series.reset_index(drop=True), tertile_df], axis=1)
        reference = fit_reference_cutoffs(
            reference_input,
            columns=list(
                OBS_ANTIOX_TERTILE_COMPONENTS
                + OBS_DIET_PROOX_TERTILE_COMPONENTS
                + OBS_LIFESTYLE_TERTILE_COMPONENTS
            ),
            method="tertile",
            probs=(0.0, 1.0 / 3.0, 2.0 / 3.0, 1.0),
            groupby="gender",
        )

    result = pd.DataFrame({"RESPONDENTID": np.asarray(respondent_id)})
    total = np.zeros(len(tertile_df), dtype=float)
    diet_total = np.zeros(len(tertile_df), dtype=float)

    for component in OBS_ANTIOX_TERTILE_COMPONENTS:
        scores = score_series_with_reference(
            tertile_df[component],
            reference,
            variable=component,
            scores=(0.0, 1.0, 2.0),
            group=gender_series,
        )
        scores[gender_series.isna().to_numpy()] = np.nan
        output_name = f"OBS_{OBS_COMPONENT_OUTPUT_NAMES[component]}"
        result[output_name] = scores
        total += np.asarray(scores, dtype=float)
        diet_total += np.asarray(scores, dtype=float)

    for component in OBS_DIET_PROOX_TERTILE_COMPONENTS:
        scores = score_series_with_reference(
            tertile_df[component],
            reference,
            variable=component,
            scores=(2.0, 1.0, 0.0),
            group=gender_series,
        )
        scores[gender_series.isna().to_numpy()] = np.nan
        output_name = f"OBS_{OBS_COMPONENT_OUTPUT_NAMES[component]}"
        result[output_name] = scores
        total += np.asarray(scores, dtype=float)
        diet_total += np.asarray(scores, dtype=float)

    lifestyle_total = np.zeros(len(tertile_df), dtype=float)

    for component in OBS_LIFESTYLE_TERTILE_COMPONENTS:
        scores = score_series_with_reference(
            tertile_df[component],
            reference,
            variable=component,
            scores=(2.0, 1.0, 0.0),
            group=gender_series,
        )
        scores[gender_series.isna().to_numpy()] = np.nan
        output_name = f"OBS_{OBS_COMPONENT_OUTPUT_NAMES[component]}"
        result[output_name] = scores
        total += np.asarray(scores, dtype=float)
        lifestyle_total += np.asarray(scores, dtype=float)

    activity_scores = _score_physical_activity(physical_activity_met)
    alcohol_scores = _score_alcohol(gender, alcohol_drinks_per_day, alcohol_drinks_per_year)

    result["OBS_PHYSICAL_ACTIVITY"] = activity_scores
    result["OBS_ALCOHOL"] = alcohol_scores

    lifestyle_total += np.asarray(activity_scores, dtype=float) + np.asarray(alcohol_scores, dtype=float)
    total += np.asarray(activity_scores, dtype=float) + np.asarray(alcohol_scores, dtype=float)

    result["OBS_DIET"] = diet_total
    result["OBS_LIFESTYLE"] = lifestyle_total
    result["OBS_ALL"] = total
    return result
