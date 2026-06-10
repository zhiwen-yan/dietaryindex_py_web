"""
MED - Mediterranean Diet Index

精确翻译自 dietaryindex R 包 MED.R 源码。
基于中位数排名的饮食评分，总分范围 0-9。
"""

import numpy as np
import pandas as pd
from dietaryindex.core._scoring import score_median_healthy, score_median_unhealthy


def compute_med(
    data,
    respondent_id,
    fruit_fruit_juice,
    vegetable,
    whole_grain,
    legumes,
    nuts,
    fish,
    red_processed_meat,
    mon_sat_fat_ratio,
    alcohol,
):
    """
    计算 MED (地中海饮食指数)
    """
    rid = np.asarray(respondent_id)

    med_frt = score_median_healthy(np.asarray(fruit_fruit_juice, dtype=float))
    med_veg = score_median_healthy(np.asarray(vegetable, dtype=float))
    med_wg = score_median_healthy(np.asarray(whole_grain, dtype=float))
    med_leg = score_median_healthy(np.asarray(legumes, dtype=float))
    med_nuts = score_median_healthy(np.asarray(nuts, dtype=float))
    med_fish = score_median_healthy(np.asarray(fish, dtype=float))
    med_rpm = score_median_unhealthy(np.asarray(red_processed_meat, dtype=float))
    med_ms = score_median_healthy(np.asarray(mon_sat_fat_ratio, dtype=float))

    alc = np.asarray(alcohol, dtype=float)
    med_alc = np.where((alc <= 25) & (alc >= 10), 1, 0)

    med_all = med_frt + med_veg + med_wg + med_leg + med_nuts + med_fish + med_rpm + med_ms + med_alc
    med_noetoh = med_frt + med_veg + med_wg + med_leg + med_nuts + med_fish + med_rpm + med_ms

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "MED_ALL": med_all,
        "MED_NOETOH": med_noetoh,
        "MED_FRT": med_frt,
        "MED_VEG": med_veg,
        "MED_WGRAIN": med_wg,
        "MED_LEGUMES": med_leg,
        "MED_NUTS": med_nuts,
        "MED_FISH": med_fish,
        "MED_REDPROC_MEAT": med_rpm,
        "MED_MONSATFAT": med_ms,
        "MED_ALCOHOL": med_alc,
    })
