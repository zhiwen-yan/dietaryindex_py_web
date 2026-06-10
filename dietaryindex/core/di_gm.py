"""
DI_GM - Dietary Index for Gut Microbiota

精确翻译自 dietaryindex R 包 DI_GM.R 源码。
性别分层中位数评分，总分范围 0-14。
"""

import numpy as np
import pandas as pd


def compute_di_gm(
    data,
    respondent_id,
    gender,
    avocado,
    broccoli,
    chickpea,
    coffee,
    cranberry,
    fermented_dairy,
    fiber,
    green_tea,
    soybean,
    whole_grain,
    total_fat_pct,
    processed_meat,
    red_meat,
    refined_grain,
):
    """
    计算 DI_GM (膳食指数-肠道微生物)
    """
    rid = np.asarray(respondent_id)
    gend = np.asarray(gender, dtype=float)

    foods = {
        "AVOCADO": np.asarray(avocado, dtype=float),
        "BROCCOLI": np.asarray(broccoli, dtype=float),
        "CHICKPEA": np.asarray(chickpea, dtype=float),
        "COFFEE": np.asarray(coffee, dtype=float),
        "CRANBERRY": np.asarray(cranberry, dtype=float),
        "FERMENTED_DAIRY": np.asarray(fermented_dairy, dtype=float),
        "FIBER": np.asarray(fiber, dtype=float),
        "GREEN_TEA": np.asarray(green_tea, dtype=float),
        "SOYBEAN": np.asarray(soybean, dtype=float),
        "WHOLE_GRAIN": np.asarray(whole_grain, dtype=float),
    }
    tfat_pct = np.asarray(total_fat_pct, dtype=float)
    proc_meat = np.asarray(processed_meat, dtype=float)
    rmeat = np.asarray(red_meat, dtype=float)
    rgr = np.asarray(refined_grain, dtype=float)

    n = len(rid)
    is_female = gend == 2
    is_male = gend == 1

    scores = {}

    for name, values in foods.items():
        s = np.full(n, np.nan)
        for gid, mask in [(2, is_female), (1, is_male)]:
            if not mask.any():
                continue
            g_vals = values[mask]
            med = np.nanmedian(g_vals)
            s[mask] = np.where(np.isnan(g_vals), np.nan, np.where((g_vals < med) | (g_vals == 0), 0.0, 1.0))
        scores[f"DI_GM_{name}"] = s

    s_tfat = np.where(np.isnan(tfat_pct), np.nan, np.where(tfat_pct >= 40, 0.0, 1.0))

    unhealthy = {"PROCESSED_MEAT": proc_meat, "RED_MEAT": rmeat, "REFINED_GRAIN": rgr}
    for name, values in unhealthy.items():
        s = np.full(n, np.nan)
        for gid, mask in [(2, is_female), (1, is_male)]:
            if not mask.any():
                continue
            g_vals = values[mask]
            med = np.nanmedian(g_vals)
            s[mask] = np.where(np.isnan(g_vals), np.nan, np.where((g_vals < med) | (g_vals == 0), 1.0, 0.0))
        scores[f"DI_GM_{name}"] = s

    di_gm_total = sum(scores.values()) + s_tfat

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "GENDER": gend,
        "DI_GM_TOTAL": di_gm_total,
        "DI_GM_AVOCADO": scores["DI_GM_AVOCADO"],
        "DI_GM_BROCCOLI": scores["DI_GM_BROCCOLI"],
        "DI_GM_CHICKPEA": scores["DI_GM_CHICKPEA"],
        "DI_GM_COFFEE": scores["DI_GM_COFFEE"],
        "DI_GM_CRANBERRY": scores["DI_GM_CRANBERRY"],
        "DI_GM_FERMENTED_DAIRY": scores["DI_GM_FERMENTED_DAIRY"],
        "DI_GM_FIBER": scores["DI_GM_FIBER"],
        "DI_GM_GREEN_TEA": scores["DI_GM_GREEN_TEA"],
        "DI_GM_SOYBEAN": scores["DI_GM_SOYBEAN"],
        "DI_GM_WHOLE_GRAIN": scores["DI_GM_WHOLE_GRAIN"],
        "DI_GM_TOTAL_FAT_PERCENTAGE": s_tfat,
        "DI_GM_PROCESSED_MEAT": scores["DI_GM_PROCESSED_MEAT"],
        "DI_GM_RED_MEAT": scores["DI_GM_RED_MEAT"],
        "DI_GM_REFINED_GRAIN": scores["DI_GM_REFINED_GRAIN"],
    })
