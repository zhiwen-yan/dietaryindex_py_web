"""
PHDI - Planetary Health Diet Index

精确翻译自 dietaryindex R 包 PHDI.R 源码。
总分范围: 0-140 (15个组分；豆类和大豆各最高5分)，基于 EAT-Lancet 报告。
"""

import numpy as np
import pandas as pd
from dietaryindex.core._scoring import score_healthy, score_unhealthy


def compute_phdi(
    data,
    respondent_id,
    gender,
    total_kcal,
    whole_grain,
    starchy_veg,
    vegetable,
    fruit,
    dairy,
    red_processed_meat,
    poultry,
    egg,
    fish,
    nuts,
    legumes,
    soy,
    added_fat_unsat,
    added_fat_sat_trans,
    added_sugar,
):
    """
    计算 PHDI (Planetary Health Diet Index)
    """
    rid = np.asarray(respondent_id)
    gend = np.asarray(gender, dtype=float)
    kcal = np.asarray(total_kcal, dtype=float)

    wg = np.asarray(whole_grain, dtype=float)
    sv = np.asarray(starchy_veg, dtype=float)
    veg = np.asarray(vegetable, dtype=float)
    frt = np.asarray(fruit, dtype=float)
    dair = np.asarray(dairy, dtype=float)
    rpm = np.asarray(red_processed_meat, dtype=float)
    poul = np.asarray(poultry, dtype=float)
    egg = np.asarray(egg, dtype=float)
    fish = np.asarray(fish, dtype=float)
    nuts = np.asarray(nuts, dtype=float)
    leg = np.asarray(legumes, dtype=float)
    soy = np.asarray(soy, dtype=float)
    afu = np.asarray(added_fat_unsat, dtype=float)
    afs = np.asarray(added_fat_sat_trans, dtype=float)
    asug = np.asarray(added_sugar, dtype=float)

    is_female = gend == 2
    phdi_wg = np.where(
        is_female,
        score_healthy(wg, 0, 75, 0, 10),
        score_healthy(wg, 0, 90, 0, 10),
    )
    phdi_sv = score_unhealthy(sv, 200, 50, 0, 10)
    phdi_veg = score_healthy(veg, 0, 300, 0, 10)
    phdi_frt = score_healthy(frt, 0, 200, 0, 10)
    phdi_dair = score_unhealthy(dair, 1000, 250, 0, 10)
    phdi_rpm = score_unhealthy(rpm, 100, 14, 0, 10)
    phdi_poul = score_unhealthy(poul, 100, 29, 0, 10)
    phdi_egg = score_unhealthy(egg, 120, 13, 0, 10)
    phdi_fish = score_healthy(fish, 0, 28, 0, 10)
    phdi_nuts = score_healthy(nuts, 0, 50, 0, 10)
    phdi_leg = score_healthy(leg, 0, 100, 0, 5)
    phdi_soy = score_healthy(soy, 0, 50, 0, 5)
    phdi_afu = score_healthy(afu, 3.5, 21, 0, 10)
    phdi_afs = score_unhealthy(afs, 10, 0, 0, 10)
    phdi_asug = score_unhealthy(asug, 25, 5, 0, 10)

    phdi_all = phdi_wg + phdi_sv + phdi_veg + phdi_frt + phdi_dair + phdi_rpm + \
        phdi_poul + phdi_egg + phdi_fish + phdi_nuts + phdi_leg + phdi_soy + \
        phdi_afu + phdi_afs + phdi_asug

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "GENDER": gend,
        "PHDI_ALL": phdi_all,
        "TOTALKCAL_PHDI": kcal,
        "PHDI_WGRAIN": phdi_wg,
        "PHDI_STARCHY_VEG": phdi_sv,
        "PHDI_VEG": phdi_veg,
        "PHDI_FRT": phdi_frt,
        "PHDI_DAIRY": phdi_dair,
        "PHDI_REDPROC_MEAT": phdi_rpm,
        "PHDI_POULTRY": phdi_poul,
        "PHDI_EGG": phdi_egg,
        "PHDI_FISH": phdi_fish,
        "PHDI_NUTS": phdi_nuts,
        "PHDI_LEGUMES": phdi_leg,
        "PHDI_SOY": phdi_soy,
        "PHDI_ADDED_FAT_UNSAT": phdi_afu,
        "PHDI_ADDED_FAT_SAT": phdi_afs,
        "PHDI_ADDED_SUGAR": phdi_asug,
    })


def compute_phdi_v2(
    data,
    respondent_id,
    gender,
    total_kcal,
    whole_grain,
    starchy_veg,
    vegetable,
    fruit,
    dairy,
    red_processed_meat,
    poultry,
    egg,
    fish,
    nuts,
    legumes,
    soy,
    added_fat_unsat,
    added_fat_sat_trans,
    added_sugar,
):
    """
    计算 PHDI V2 (Planetary Health Diet Index V2)
    与 V1 区别：输入的三种脂肪/糖是以克为单位，本函数自动除以 total_kcal 转换为能量占比后计算得分。
    """
    kcal = np.asarray(total_kcal, dtype=float)
    afu_g = np.asarray(added_fat_unsat, dtype=float)
    afs_g = np.asarray(added_fat_sat_trans, dtype=float)
    asug_g = np.asarray(added_sugar, dtype=float)

    # 1 gram of fat = 9 kcal, 1 gram of carbohydrate/sugar = 4 kcal
    # (grams * multiplier / total_kcal) * 100
    # Avoid division by zero by using np.where or replacing zero kcal with nan
    with np.errstate(divide='ignore', invalid='ignore'):
        afu_pct = np.where(kcal > 0, (afu_g * 9.0 / kcal) * 100.0, np.nan)
        afs_pct = np.where(kcal > 0, (afs_g * 9.0 / kcal) * 100.0, np.nan)
        asug_pct = np.where(kcal > 0, (asug_g * 4.0 / kcal) * 100.0, np.nan)

    # Handle NaN preservation
    afu_pct[np.isnan(afu_g) | np.isnan(kcal)] = np.nan
    afs_pct[np.isnan(afs_g) | np.isnan(kcal)] = np.nan
    asug_pct[np.isnan(asug_g) | np.isnan(kcal)] = np.nan

    return compute_phdi(
        data=data,
        respondent_id=respondent_id,
        gender=gender,
        total_kcal=total_kcal,
        whole_grain=whole_grain,
        starchy_veg=starchy_veg,
        vegetable=vegetable,
        fruit=fruit,
        dairy=dairy,
        red_processed_meat=red_processed_meat,
        poultry=poultry,
        egg=egg,
        fish=fish,
        nuts=nuts,
        legumes=legumes,
        soy=soy,
        added_fat_unsat=afu_pct,
        added_fat_sat_trans=afs_pct,
        added_sugar=asug_pct,
    )
