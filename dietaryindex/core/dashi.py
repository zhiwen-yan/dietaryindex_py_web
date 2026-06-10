"""
DASHI - Dietary Approaches to Stop Hypertension (nutrient-based)

精确翻译自 dietaryindex R 包 DASHI.R 源码。
营养密度法，总分范围 0-9。
"""

import numpy as np
import pandas as pd
from dietaryindex.core._scoring import score_healthy, score_unhealthy


def compute_dashi(
    data,
    respondent_id,
    total_kcal,
    total_fat_pct,
    sat_fat_pct,
    protein_pct,
    cholesterol,
    fiber,
    potassium,
    magnesium,
    calcium,
    sodium,
):
    """
    计算 DASHI (营养密度版 DASH)

    所有营养素已按 /2000kcal 标准化。
    """
    rid = np.asarray(respondent_id)
    kcal = np.asarray(total_kcal, dtype=float)

    tf = np.asarray(total_fat_pct, dtype=float)
    sf = np.asarray(sat_fat_pct, dtype=float)
    prot = np.asarray(protein_pct, dtype=float)
    chol = np.asarray(cholesterol, dtype=float)
    fib = np.asarray(fiber, dtype=float)
    k = np.asarray(potassium, dtype=float)
    mg = np.asarray(magnesium, dtype=float)
    ca = np.asarray(calcium, dtype=float)
    na = np.asarray(sodium, dtype=float)

    dashi_tf = score_unhealthy(tf, 37, 27, 0, 1)
    dashi_sf = score_unhealthy(sf, 16, 6, 0, 1)
    dashi_chol = score_unhealthy(chol, 285.7, 142.8, 0, 1)
    dashi_na = score_unhealthy(na, 2857, 2286, 0, 1)
    dashi_prot = score_healthy(prot, 15, 18, 0, 1)
    dashi_fib = score_healthy(fib, 8.6, 29.5, 0, 1)
    dashi_k = score_healthy(k, 1619, 4476, 0, 1)
    dashi_mg = score_healthy(mg, 157, 476, 0, 1)
    dashi_ca = score_healthy(ca, 429, 1181, 0, 1)

    dashi_all = dashi_tf + dashi_sf + dashi_chol + dashi_na + dashi_prot + dashi_fib + dashi_k + dashi_mg + dashi_ca

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "DASHI_ALL": dashi_all,
        "TOTALKCAL_DASHI": kcal,
        "DASHI_TOTAL_FAT": dashi_tf,
        "DASHI_SAT_FAT": dashi_sf,
        "DASHI_PROTEIN": dashi_prot,
        "DASHI_CHOLESTEROL": dashi_chol,
        "DASHI_FIBER": dashi_fib,
        "DASHI_POTASSIUM": dashi_k,
        "DASHI_MAGNESIUM": dashi_mg,
        "DASHI_CALCIUM": dashi_ca,
        "DASHI_SODIUM": dashi_na,
    })
