"""
AHEIP - Alternative Healthy Eating Index for Pregnancy

精确翻译自 dietaryindex R 包 AHEIP.R 源码。
总分范围: 0-90 (9个组分)
"""

import numpy as np
import pandas as pd
from dietaryindex.core._scoring import score_healthy, score_unhealthy


def compute_aheip(
    data,
    respondent_id,
    vegetable,
    fruit,
    white_red_ratio,
    fiber,
    trans_fat,
    poly_sat_ratio,
    calcium,
    folate,
    iron,
):
    """
    计算 AHEIP (怀孕版替代健康饮食指数)
    """
    rid = np.asarray(respondent_id)

    aheip_veg = score_healthy(np.asarray(vegetable, dtype=float), 0, 5, 0, 10)
    aheip_frt = score_healthy(np.asarray(fruit, dtype=float), 0, 4, 0, 10)
    aheip_wr = score_healthy(np.asarray(white_red_ratio, dtype=float), 0, 4, 0, 10)
    aheip_fib = score_healthy(np.asarray(fiber, dtype=float), 0, 25, 0, 10)
    aheip_trans = score_unhealthy(np.asarray(trans_fat, dtype=float), 4, 0.5, 0, 10)
    aheip_ps = score_healthy(np.asarray(poly_sat_ratio, dtype=float), 0.1, 1, 0, 10)
    aheip_ca = score_healthy(np.asarray(calcium, dtype=float), 0, 1200, 0, 10)
    aheip_fol = score_healthy(np.asarray(folate, dtype=float), 0, 600, 0, 10)
    aheip_fe = score_healthy(np.asarray(iron, dtype=float), 0, 27, 0, 10)

    aheip_all = aheip_veg + aheip_frt + aheip_wr + aheip_fib + aheip_trans + \
        aheip_ps + aheip_ca + aheip_fol + aheip_fe

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "AHEIP_ALL": aheip_all,
        "AHEIP_VEG": aheip_veg,
        "AHEIP_FRT": aheip_frt,
        "AHEIP_WHITEREAD": aheip_wr,
        "AHEIP_FIBER": aheip_fib,
        "AHEIP_TRANS": aheip_trans,
        "AHEIP_POLYSAT": aheip_ps,
        "AHEIP_CALCIUM": aheip_ca,
        "AHEIP_FOLATE": aheip_fol,
        "AHEIP_IRON": aheip_fe,
    })
