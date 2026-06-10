"""
DASH - Dietary Approaches to Stop Hypertension

精确翻译自 dietaryindex R 包 DASH.R 源码。
基于五等分排名的饮食评分，总分 8-40。
"""

import numpy as np
import pandas as pd
from dietaryindex.core._scoring import score_quintile_healthy, score_quintile_unhealthy


def compute_dash(
    data,
    respondent_id,
    total_kcal,
    fruit_fruit_juice,
    vegetable,
    nut_legume,
    whole_grain,
    low_fat_dairy,
    sodium,
    red_processed_meat,
    ssb_fruit_juice,
):
    """
    计算 DASH 指数
    """
    rid = np.asarray(respondent_id)
    kcal = np.asarray(total_kcal, dtype=float)

    dash_frt = score_quintile_healthy(np.asarray(fruit_fruit_juice, dtype=float))
    dash_veg = score_quintile_healthy(np.asarray(vegetable, dtype=float))
    dash_nut = score_quintile_healthy(np.asarray(nut_legume, dtype=float))
    dash_wg = score_quintile_healthy(np.asarray(whole_grain, dtype=float))
    dash_dair = score_quintile_healthy(np.asarray(low_fat_dairy, dtype=float))

    with np.errstate(divide='ignore', invalid='ignore'):
        sodium_per_2000 = np.asarray(sodium, dtype=float) / (kcal / 2000.0)
    dash_na = score_quintile_unhealthy(sodium_per_2000)
    dash_rpm = score_quintile_unhealthy(np.asarray(red_processed_meat, dtype=float))
    dash_ssb = score_quintile_unhealthy(np.asarray(ssb_fruit_juice, dtype=float))

    dash_all = dash_frt + dash_veg + dash_nut + dash_wg + dash_dair + dash_na + dash_rpm + dash_ssb

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "DASH_ALL": dash_all,
        "DASH_FRT": dash_frt,
        "DASH_VEG": dash_veg,
        "DASH_NUTSLEG": dash_nut,
        "DASH_WGRAIN": dash_wg,
        "DASH_LOWF_DAIRY": dash_dair,
        "DASH_SODIUM": dash_na,
        "DASH_REDPROC_MEAT": dash_rpm,
        "DASH_SSB_FRTJ": dash_ssb,
    })
