"""
AHEI - Alternative Healthy Eating Index

精确翻译自 dietaryindex R 包 AHEI.R 源码。
总分范围: 0-110 (11个组分)，含性别差异处理。
"""

import numpy as np
import pandas as pd
from dietaryindex.core._scoring import score_healthy, score_unhealthy, score_decile_sodium


def compute_ahei(
    data,
    respondent_id,
    gender,
    total_kcal,
    vegetable,
    fruit,
    whole_grain,
    nut_legume,
    n3_fat,
    pufa,
    ssb_fruit_juice,
    red_processed_meat,
    trans_fat,
    sodium,
    alcohol,
):
    """
    计算 AHEI (Alternative Healthy Eating Index)

    Parameters
    ----------
    gender : array-like, 1=male, 2=female
    total_kcal : array-like, kcal
    vegetable : servings/day
    fruit : servings/day
    whole_grain : g/day (female max=75, male max=90)
    nut_legume : servings/day
    n3_fat : mg/day
    pufa : % of energy
    ssb_fruit_juice : servings/day
    red_processed_meat : servings/day
    trans_fat : % of energy
    sodium : mg/day
    alcohol : drinks/day
    """
    rid = np.asarray(respondent_id)
    gender = np.asarray(gender, dtype=float)
    kcal = np.asarray(total_kcal, dtype=float)

    veg = np.asarray(vegetable, dtype=float)
    frt = np.asarray(fruit, dtype=float)
    wg = np.asarray(whole_grain, dtype=float)
    nut = np.asarray(nut_legume, dtype=float)
    n3 = np.asarray(n3_fat, dtype=float)
    pu = np.asarray(pufa, dtype=float)
    ssb = np.asarray(ssb_fruit_juice, dtype=float)
    rpm = np.asarray(red_processed_meat, dtype=float)
    trans = np.asarray(trans_fat, dtype=float)
    na = np.asarray(sodium, dtype=float)
    alc = np.asarray(alcohol, dtype=float)

    ahei_veg = score_healthy(veg, 0, 5, 0, 10)
    ahei_frt = score_healthy(frt, 0, 4, 0, 10)

    ahei_wg = np.select(
        [gender == 2, gender == 1],
        [score_healthy(wg, 0, 75, 0, 10), score_healthy(wg, 0, 90, 0, 10)],
        default=np.nan
    )

    ahei_nut = score_healthy(nut, 0, 1, 0, 10)
    ahei_n3 = score_healthy(n3, 0, 250, 0, 10)
    ahei_pu = score_healthy(pu, 2, 10, 0, 10)
    ahei_ssb = score_unhealthy(ssb, 1, 0, 0, 10)
    ahei_rpm = score_unhealthy(rpm, 1.5, 0, 0, 10)
    ahei_trans = score_unhealthy(trans, 4, 0.5, 0, 10)

    with np.errstate(divide='ignore', invalid='ignore'):
        na_per_2000 = na / (kcal / 2000.0)
    na_scores = score_decile_sodium(na_per_2000)

    # Female alcohol conditions:
    cond_f = [
        (gender == 2) & (alc >= 2.5),
        (gender == 2) & (alc < 2.5) & (alc > 1.5),
        (gender == 2) & (alc <= 1.5) & (alc >= 0.5),
        (gender == 2) & (alc < 0.5) & (alc > 0.125),
        (gender == 2) & (alc <= 0.125),
    ]
    choice_f = [
        0.0,
        0.0 + (alc - 2.5) * 10.0 / (1.5 - 2.5),
        10.0,
        0.0 + (alc - 0.0) * 10.0 / (0.5 - 0.0),
        2.5
    ]

    # Male alcohol conditions:
    cond_m = [
        (gender == 1) & (alc >= 3.5),
        (gender == 1) & (alc < 3.5) & (alc > 2.0),
        (gender == 1) & (alc <= 2.0) & (alc >= 0.5),
        (gender == 1) & (alc < 0.5) & (alc > 0.125),
        (gender == 1) & (alc <= 0.125),
    ]
    choice_m = [
        0.0,
        0.0 + (alc - 3.5) * 10.0 / (2.0 - 3.5),
        10.0,
        0.0 + (alc - 0.0) * 10.0 / (0.5 - 0.0),
        2.5
    ]

    ahei_alc = np.select(cond_f + cond_m, choice_f + choice_m, default=np.nan)

    trans_all_nan = np.all(np.isnan(ahei_trans))
    if trans_all_nan:
        ahei_all = ahei_veg + ahei_frt + ahei_wg + ahei_nut + ahei_n3 + ahei_pu + ahei_ssb + ahei_rpm + na_scores + ahei_alc
        ahei_noetoh = ahei_veg + ahei_frt + ahei_wg + ahei_nut + ahei_n3 + ahei_pu + ahei_ssb + ahei_rpm + na_scores
    else:
        ahei_all = ahei_veg + ahei_frt + ahei_wg + ahei_nut + ahei_n3 + ahei_pu + ahei_ssb + ahei_rpm + ahei_trans + na_scores + ahei_alc
        ahei_noetoh = ahei_veg + ahei_frt + ahei_wg + ahei_nut + ahei_n3 + ahei_pu + ahei_ssb + ahei_rpm + ahei_trans + na_scores

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "GENDER": gender,
        "AHEI_ALL": ahei_all,
        "AHEI_NOETOH": ahei_noetoh,
        "AHEI_VEG": ahei_veg,
        "AHEI_FRT": ahei_frt,
        "AHEI_WGRAIN": ahei_wg,
        "AHEI_NUTSLEG": ahei_nut,
        "AHEI_N3FAT": ahei_n3,
        "AHEI_PUFA": ahei_pu,
        "AHEI_SSB_FRTJ": ahei_ssb,
        "AHEI_REDPROC_MEAT": ahei_rpm,
        "AHEI_TRANS": ahei_trans,
        "AHEI_SODIUM": na_scores,
        "AHEI_ALCOHOL": ahei_alc,
    })
