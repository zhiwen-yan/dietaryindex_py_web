"""
MEDI - Mediterranean Diet Index (serving size, 0/1 points)

精确翻译自 dietaryindex R 包 MEDI.R / MEDI_V2.R 源码。
MEDI (V1): 基于绝对阈值的二分评分，总分 0-11。
MEDI_V2: 基于份量的 0-5 连续评分，总分 0-55。
"""

import numpy as np
import pandas as pd
from dietaryindex.core._scoring import score_healthy, score_unhealthy


def compute_medi(
    data,
    respondent_id,
    olive_oil,
    fruit,
    vegetable,
    legumes,
    nuts,
    fish_seafood,
    alcohol,
    ssb,
    sweets,
    discret_fat,
    red_processed_meat,
):
    """
    计算 MEDI V1 (地中海饮食指数改进版，0/1 二分评分)

    基于 PREDIMED 试验的绝对阈值评分。
    """
    rid = np.asarray(respondent_id)

    oo = np.asarray(olive_oil, dtype=float)
    frt = np.asarray(fruit, dtype=float)
    veg = np.asarray(vegetable, dtype=float)
    leg = np.asarray(legumes, dtype=float)
    nuts = np.asarray(nuts, dtype=float)
    fish = np.asarray(fish_seafood, dtype=float)
    alc = np.asarray(alcohol, dtype=float)
    ssb = np.asarray(ssb, dtype=float)
    sw = np.asarray(sweets, dtype=float)
    df = np.asarray(discret_fat, dtype=float)
    rpm = np.asarray(red_processed_meat, dtype=float)

    medi_oo = np.where(oo >= 5, 1, 0)
    medi_frt = np.where(frt >= 3, 1, 0)
    medi_veg = np.where(veg >= 2, 1, 0)
    medi_leg = np.where(leg >= 3 / 7, 1, 0)
    medi_nuts = np.where(nuts >= 3 / 7, 1, 0)
    medi_fish = np.where(fish >= 3 / 7, 1, 0)
    medi_alc = np.where(alc >= 1, 1, 0)
    medi_ssb = np.where(ssb < 1, 1, 0)
    medi_sw = np.where(sw < 2 / 7, 1, 0)
    medi_df = np.where(df < 1, 1, 0)
    medi_rpm = np.where(rpm < 1, 1, 0)

    medi_all = medi_oo + medi_frt + medi_veg + medi_leg + medi_nuts + medi_fish + \
        medi_alc + medi_ssb + medi_sw + medi_df + medi_rpm
    # Dietaryindex R 2.1 defines NOETOH without the olive-oil component as well
    # as without alcohol. Preserve that definition for cross-language parity.
    medi_noetoh = medi_frt + medi_veg + medi_leg + medi_nuts + medi_fish + \
        medi_ssb + medi_sw + medi_df + medi_rpm

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "MEDI_ALL": medi_all,
        "MEDI_NOETOH": medi_noetoh,
        "MEDI_OLIVE_OIL": medi_oo,
        "MEDI_FRT": medi_frt,
        "MEDI_VEG": medi_veg,
        "MEDI_LEGUMES": medi_leg,
        "MEDI_NUTS": medi_nuts,
        "MEDI_FISH": medi_fish,
        "MEDI_ALCOHOL": medi_alc,
        "MEDI_SSB": medi_ssb,
        "MEDI_SWEETS": medi_sw,
        "MEDI_DISCRET_FAT": medi_df,
        "MEDI_REDPROC_MEAT": medi_rpm,
    })


def compute_medi_v2(
    data,
    respondent_id,
    olive_oil,
    fruit,
    vegetable,
    legumes,
    nuts,
    fish_seafood,
    alcohol,
    ssb,
    sweets,
    discret_fat,
    red_processed_meat,
):
    """
    计算 MEDI V2 (地中海饮食指数改进版，0-5 连续评分)

    基于份量的线性连续评分，总分 0-55。
    与 V1 使用相同的输入参数，但评分方法不同：
    - V1: 超过阈值 → 1，否则 → 0
    - V2: 0-min 到 max-5 之间线性插值
    """
    rid = np.asarray(respondent_id)

    oo = np.asarray(olive_oil, dtype=float)
    frt = np.asarray(fruit, dtype=float)
    veg = np.asarray(vegetable, dtype=float)
    leg = np.asarray(legumes, dtype=float)
    nuts = np.asarray(nuts, dtype=float)
    fish = np.asarray(fish_seafood, dtype=float)
    alc = np.asarray(alcohol, dtype=float)
    ssb = np.asarray(ssb, dtype=float)
    sw = np.asarray(sweets, dtype=float)
    df = np.asarray(discret_fat, dtype=float)
    rpm = np.asarray(red_processed_meat, dtype=float)

    medi_oo = score_healthy(oo, 0, 5, 0, 5)
    medi_frt = score_healthy(frt, 0, 3, 0, 5)
    medi_veg = score_healthy(veg, 0, 2, 0, 5)
    medi_leg = score_healthy(leg, 0, 3 / 7, 0, 5)
    medi_nuts = score_healthy(nuts, 0, 3 / 7, 0, 5)
    medi_fish = score_healthy(fish, 0, 3 / 7, 0, 5)
    medi_alc = score_healthy(alc, 0, 1, 0, 5)
    medi_ssb = score_unhealthy(ssb, 1, 0, 0, 5)
    medi_sw = score_unhealthy(sw, 2 / 7, 0, 0, 5)
    medi_df = score_unhealthy(df, 1, 0, 0, 5)
    medi_rpm = score_unhealthy(rpm, 1, 0, 0, 5)

    medi_v2_all = medi_oo + medi_frt + medi_veg + medi_leg + medi_nuts + \
        medi_fish + medi_alc + medi_ssb + medi_sw + medi_df + medi_rpm
    # Match the corresponding Dietaryindex R 2.1 output definition.
    medi_v2_noetoh = medi_frt + medi_veg + medi_leg + medi_nuts + medi_fish + \
        medi_ssb + medi_sw + medi_df + medi_rpm

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "MEDI_V2_ALL": medi_v2_all,
        "MEDI_V2_NOETOH": medi_v2_noetoh,
        "MEDI_OLIVE_OIL": medi_oo,
        "MEDI_FRT": medi_frt,
        "MEDI_VEG": medi_veg,
        "MEDI_LEGUMES": medi_leg,
        "MEDI_NUTS": medi_nuts,
        "MEDI_FISH": medi_fish,
        "MEDI_ALCOHOL": medi_alc,
        "MEDI_SSB": medi_ssb,
        "MEDI_SWEETS": medi_sw,
        "MEDI_DISCRET_FAT": medi_df,
        "MEDI_REDPROC_MEAT": medi_rpm,
    })
