"""
HEI2020 - Healthy Eating Index 2020 + HEI2020 TODDLERS

精确翻译自 dietaryindex R 包 HEI2020.R 源码。
总分范围: 0-100，支持成人(>=2岁)和幼儿(1-2岁)标准。
"""

import numpy as np
import pandas as pd
from dietaryindex.core._scoring import score_healthy, score_unhealthy


# 成人标准 (age >= 2)
ADULT_THRESHOLDS = {
    "TOTALFRT":       (0, 0.8),
    "FRT":            (0, 0.4),
    "VEG":            (0, 1.1),
    "GREENNBEAN":     (0, 0.2),
    "TOTALPRO":       (0, 2.5),
    "SEAPLANTPRO":    (0, 0.8),
    "WHOLEGRAIN":     (0, 1.5),
    "DAIRY":          (0, 1.3),
    "FATTYACID":      (1.2, 2.5),
    "REFINEDGRAIN":   (4.3, 1.8),
    "SODIUM":         (2.0, 1.1),
    "ADDEDSUGAR":     (26, 6.5),
    "SATFAT":         (16, 8),
}

# 幼儿标准 (1 <= age < 2)
TODDLER_THRESHOLDS = {
    "TOTALFRT":       (0, 0.7),
    "FRT":            (0, 0.3),
    "VEG":            (0, 0.9),
    "GREENNBEAN":     (0, 0.1),
    "TOTALPRO":       (0, 2.0),
    "SEAPLANTPRO":    (0, 0.5),
    "WHOLEGRAIN":     (0, 1.5),
    "DAIRY":          (0, 2.0),
    "FATTYACID":      (0.9, 1.5),
    "REFINEDGRAIN":   (3.4, 1.5),
    "SODIUM":         (1.7, 1.1),
    "ADDEDSUGAR":     (13.8, 0),
    "SATFAT":         (18.2, 12.2),
}


def _compute_hei2020_core(
    age,
    total_kcal,
    total_fruit, whole_fruit,
    total_vegetable, green_and_bean,
    total_protein, seafood_plant_protein,
    whole_grain, dairy, fatty_acid,
    refined_grain, sodium, added_sugar, saturated_fat,
    version="v1",
):
    """
    HEI2020 核心计算逻辑，支持 V1 (% energy) 和 V2 (tsp/g → convert).
    """
    age = np.asarray(age, dtype=float)
    kcal = np.asarray(total_kcal, dtype=float)

    with np.errstate(divide='ignore', invalid='ignore'):
        density_divider = kcal / 1000.0

        tfruit = np.asarray(total_fruit, dtype=float) / density_divider
        wfruit = np.asarray(whole_fruit, dtype=float) / density_divider
        tveg = np.asarray(total_vegetable, dtype=float) / density_divider
        gbean = np.asarray(green_and_bean, dtype=float) / density_divider
        tpro = np.asarray(total_protein, dtype=float) / density_divider
        spro = np.asarray(seafood_plant_protein, dtype=float) / density_divider
        wgrain = np.asarray(whole_grain, dtype=float) / density_divider
        dair = np.asarray(dairy, dtype=float) / density_divider
        fa = np.asarray(fatty_acid, dtype=float)
        rgrain = np.asarray(refined_grain, dtype=float) / density_divider

        if version == "v1":
            asugar_pct = np.asarray(added_sugar, dtype=float)
            sfat_pct = np.asarray(saturated_fat, dtype=float)
            na_g = np.asarray(sodium, dtype=float)
        else:
            asugar_tsp = np.asarray(added_sugar, dtype=float)
            asugar_pct = (asugar_tsp * 16.0) / kcal * 100.0
            sfat_g = np.asarray(saturated_fat, dtype=float)
            sfat_pct = (sfat_g * 9.0) / kcal * 100.0
            na_mg = np.asarray(sodium, dtype=float)
            na_g = na_mg / 1000.0

        na_density = na_g / density_divider

    is_adult = age >= 2
    is_toddler = (age >= 1) & (age < 2)

    def _apply_thresholds(values, key, score_fn, max_score):
        adult_min, adult_max = ADULT_THRESHOLDS[key]
        toddler_min, toddler_max = TODDLER_THRESHOLDS[key]
        adult_scores = score_fn(values, adult_min, adult_max, 0, max_score)
        toddler_scores = score_fn(values, toddler_min, toddler_max, 0, max_score)
        # Check if age is nan or neither
        result = np.where(is_adult, adult_scores, np.where(is_toddler, toddler_scores, 0.0))
        # Propagate nan when age or value is nan
        result[np.isnan(age) | np.isnan(values)] = np.nan
        return result

    s_tfruit = _apply_thresholds(tfruit, "TOTALFRT", score_healthy, 5)
    s_wfruit = _apply_thresholds(wfruit, "FRT", score_healthy, 5)
    s_tveg = _apply_thresholds(tveg, "VEG", score_healthy, 5)
    s_gbean = _apply_thresholds(gbean, "GREENNBEAN", score_healthy, 5)
    s_tpro = _apply_thresholds(tpro, "TOTALPRO", score_healthy, 5)
    s_spro = _apply_thresholds(spro, "SEAPLANTPRO", score_healthy, 5)
    s_wgrain = _apply_thresholds(wgrain, "WHOLEGRAIN", score_healthy, 10)
    s_dair = _apply_thresholds(dair, "DAIRY", score_healthy, 10)
    s_fa = _apply_thresholds(fa, "FATTYACID", score_healthy, 10)
    s_rgrain = _apply_thresholds(rgrain, "REFINEDGRAIN", score_unhealthy, 10)
    s_na = _apply_thresholds(na_density, "SODIUM", score_unhealthy, 10)
    s_asugar = _apply_thresholds(asugar_pct, "ADDEDSUGAR", score_unhealthy, 10)
    s_sfat = _apply_thresholds(sfat_pct, "SATFAT", score_unhealthy, 10)

    hei_all = s_tfruit + s_wfruit + s_tveg + s_gbean + s_tpro + s_spro + \
        s_wgrain + s_dair + s_fa + s_rgrain + s_na + s_asugar + s_sfat

    zero_mask = (kcal == 0) & (~np.isnan(kcal))
    if zero_mask.any():
        for arr in [s_tfruit, s_wfruit, s_tveg, s_gbean, s_tpro, s_spro,
                    s_wgrain, s_dair, s_fa, s_rgrain, s_asugar]:
            arr[zero_mask] = 0.0
        hei_all[zero_mask] = 0.0

    return {
        "HEI2020_ALL": hei_all,
        "HEI2020_TOTALFRT": s_tfruit,
        "HEI2020_FRT": s_wfruit,
        "HEI2020_VEG": s_tveg,
        "HEI2020_GREENNBEAN": s_gbean,
        "HEI2020_TOTALPRO": s_tpro,
        "HEI2020_SEAPLANTPRO": s_spro,
        "HEI2020_WHOLEGRAIN": s_wgrain,
        "HEI2020_DAIRY": s_dair,
        "HEI2020_FATTYACID": s_fa,
        "HEI2020_REFINEDGRAIN": s_rgrain,
        "HEI2020_SODIUM": s_na,
        "HEI2020_ADDEDSUGAR": s_asugar,
        "HEI2020_SATFAT": s_sfat,
        "TOTALKCAL_HEI2020": kcal,
    }


def compute_hei2020(
    data,
    respondent_id,
    age,
    total_kcal,
    total_fruit, whole_fruit,
    total_vegetable, green_and_bean,
    total_protein, seafood_plant_protein,
    whole_grain, dairy, fatty_acid,
    refined_grain, sodium,
    added_sugar, saturated_fat,
):
    """
    计算 HEI2020 V1 (% energy for added sugar and saturated fat)

    added_sugar: % of total energy
    saturated_fat: % of total energy
    sodium: g/1000 kcal
    """
    scores = _compute_hei2020_core(
        age, total_kcal,
        total_fruit, whole_fruit,
        total_vegetable, green_and_bean,
        total_protein, seafood_plant_protein,
        whole_grain, dairy, fatty_acid,
        refined_grain, sodium, added_sugar, saturated_fat,
        version="v1",
    )
    rid = np.asarray(respondent_id)
    age_arr = np.asarray(age, dtype=float)
    return pd.DataFrame({
        "RESPONDENTID": rid,
        "AGE": age_arr,
        "TOTALKCAL_HEI2020": scores["TOTALKCAL_HEI2020"],
        "HEI2020_ALL": scores["HEI2020_ALL"],
        "HEI2020_TOTALFRT": scores["HEI2020_TOTALFRT"],
        "HEI2020_FRT": scores["HEI2020_FRT"],
        "HEI2020_VEG": scores["HEI2020_VEG"],
        "HEI2020_GREENNBEAN": scores["HEI2020_GREENNBEAN"],
        "HEI2020_TOTALPRO": scores["HEI2020_TOTALPRO"],
        "HEI2020_SEAPLANTPRO": scores["HEI2020_SEAPLANTPRO"],
        "HEI2020_WHOLEGRAIN": scores["HEI2020_WHOLEGRAIN"],
        "HEI2020_DAIRY": scores["HEI2020_DAIRY"],
        "HEI2020_FATTYACID": scores["HEI2020_FATTYACID"],
        "HEI2020_REFINEDGRAIN": scores["HEI2020_REFINEDGRAIN"],
        "HEI2020_SODIUM": scores["HEI2020_SODIUM"],
        "HEI2020_ADDEDSUGAR": scores["HEI2020_ADDEDSUGAR"],
        "HEI2020_SATFAT": scores["HEI2020_SATFAT"],
    })


def compute_hei2020_v2(
    data,
    respondent_id,
    age,
    total_kcal,
    total_fruit, whole_fruit,
    total_vegetable, green_and_bean,
    total_protein, seafood_plant_protein,
    whole_grain, dairy, fatty_acid,
    refined_grain, sodium,
    added_sugar, saturated_fat,
):
    """
    计算 HEI2020 V2 (tsp for added sugar, g for saturated fat, auto-convert to % energy)
    """
    scores = _compute_hei2020_core(
        age, total_kcal,
        total_fruit, whole_fruit,
        total_vegetable, green_and_bean,
        total_protein, seafood_plant_protein,
        whole_grain, dairy, fatty_acid,
        refined_grain, sodium, added_sugar, saturated_fat,
        version="v2",
    )
    rid = np.asarray(respondent_id)
    age_arr = np.asarray(age, dtype=float)
    return pd.DataFrame({
        "RESPONDENTID": rid,
        "AGE": age_arr,
        "TOTALKCAL_HEI2020": scores["TOTALKCAL_HEI2020"],
        "HEI2020_ALL": scores["HEI2020_ALL"],
        "HEI2020_TOTALFRT": scores["HEI2020_TOTALFRT"],
        "HEI2020_FRT": scores["HEI2020_FRT"],
        "HEI2020_VEG": scores["HEI2020_VEG"],
        "HEI2020_GREENNBEAN": scores["HEI2020_GREENNBEAN"],
        "HEI2020_TOTALPRO": scores["HEI2020_TOTALPRO"],
        "HEI2020_SEAPLANTPRO": scores["HEI2020_SEAPLANTPRO"],
        "HEI2020_WHOLEGRAIN": scores["HEI2020_WHOLEGRAIN"],
        "HEI2020_DAIRY": scores["HEI2020_DAIRY"],
        "HEI2020_FATTYACID": scores["HEI2020_FATTYACID"],
        "HEI2020_REFINEDGRAIN": scores["HEI2020_REFINEDGRAIN"],
        "HEI2020_SODIUM": scores["HEI2020_SODIUM"],
        "HEI2020_ADDEDSUGAR": scores["HEI2020_ADDEDSUGAR"],
        "HEI2020_SATFAT": scores["HEI2020_SATFAT"],
    })
