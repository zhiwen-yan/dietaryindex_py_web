"""
HEI2015 - Healthy Eating Index 2015

精确翻译自 dietaryindex R 包 HEI2015.R 源码。
总分范围: 0-100 (13个组分, 满分100)
"""

import numpy as np
import pandas as pd
from dietaryindex.core._scoring import score_healthy, score_unhealthy


def compute_hei2015(
    data,
    respondent_id,
    total_kcal,
    total_fruit,
    whole_fruit,
    total_vegetable,
    green_and_bean,
    total_protein,
    seafood_plant_protein,
    whole_grain,
    dairy,
    fatty_acid,
    refined_grain,
    sodium,
    added_sugar,
    saturated_fat,
):
    """
    计算 HEI2015 (Healthy Eating Index 2015)

    Parameters
    ----------
    data : pd.DataFrame
    respondent_id : array-like
    total_kcal : array-like, 总热量 kcal
    total_fruit : array-like, 总水果 cup eq.
    whole_fruit : array-like, 完整水果 cup eq.
    total_vegetable : array-like, 总蔬菜 cup eq.
    green_and_bean : array-like, 深绿蔬菜+豆类 cup eq.
    total_protein : array-like, 总蛋白质 oz eq.
    seafood_plant_protein : array-like, 海鲜+植物蛋白 oz eq.
    whole_grain : array-like, 全谷物 oz eq.
    dairy : array-like, 乳制品 cup eq.
    fatty_acid : array-like, (MUFA+PUFA)/SFA 比值
    refined_grain : array-like, 精制谷物 oz eq.
    sodium : array-like, 钠 mg
    added_sugar : array-like, 添加糖 tsp
    saturated_fat : array-like, 饱和脂肪 g

    Returns
    -------
    pd.DataFrame
    """
    def _to_array(val):
        val = np.asarray(val, dtype=float)
        return val

    rid = _to_array(respondent_id)
    kcal = _to_array(total_kcal)

    with np.errstate(divide='ignore', invalid='ignore'):
        density_divider = kcal / 1000.0

        tfruit = _to_array(total_fruit) / density_divider
        wfruit = _to_array(whole_fruit) / density_divider
        tveg = _to_array(total_vegetable) / density_divider
        gbean = _to_array(green_and_bean) / density_divider
        tpro = _to_array(total_protein) / density_divider
        spro = _to_array(seafood_plant_protein) / density_divider
        wgrain = _to_array(whole_grain) / density_divider
        dair = _to_array(dairy) / density_divider
        fa = _to_array(fatty_acid)
        rgrain = _to_array(refined_grain) / density_divider
        
        na_g = _to_array(sodium) / 1000.0
        na_density = na_g / density_divider

        asugar_tsp = _to_array(added_sugar)
        asugar_pct = (asugar_tsp * 16.0) / kcal * 100.0

        sfat_g = _to_array(saturated_fat)
        sfat_pct = (sfat_g * 9.0) / kcal * 100.0

    s_tfruit = score_healthy(tfruit, 0, 0.8, 0, 5)
    s_wfruit = score_healthy(wfruit, 0, 0.4, 0, 5)
    s_tveg = score_healthy(tveg, 0, 1.1, 0, 5)
    s_gbean = score_healthy(gbean, 0, 0.2, 0, 5)
    s_tpro = score_healthy(tpro, 0, 2.5, 0, 5)
    s_spro = score_healthy(spro, 0, 0.8, 0, 5)
    s_wgrain = score_healthy(wgrain, 0, 1.5, 0, 10)
    s_dair = score_healthy(dair, 0, 1.3, 0, 10)
    s_fa = score_healthy(fa, 1.2, 2.5, 0, 10)
    s_rgrain = score_unhealthy(rgrain, 4.3, 1.8, 0, 10)
    s_na = score_unhealthy(na_density, 2.0, 1.1, 0, 10)
    s_asugar = score_unhealthy(asugar_pct, 26, 6.5, 0, 10)
    s_sfat = score_unhealthy(sfat_pct, 16, 8, 0, 10)

    hei_all = s_tfruit + s_wfruit + s_tveg + s_gbean + s_tpro + s_spro + \
        s_wgrain + s_dair + s_fa + s_rgrain + s_na + s_asugar + s_sfat

    zero_mask = (kcal == 0) & (~np.isnan(kcal))
    if zero_mask.any():
        s_tfruit[zero_mask] = 0.0
        s_wfruit[zero_mask] = 0.0
        s_tveg[zero_mask] = 0.0
        s_gbean[zero_mask] = 0.0
        s_tpro[zero_mask] = 0.0
        s_spro[zero_mask] = 0.0
        s_wgrain[zero_mask] = 0.0
        s_dair[zero_mask] = 0.0
        s_fa[zero_mask] = 0.0
        s_rgrain[zero_mask] = 0.0
        s_asugar[zero_mask] = 0.0
        hei_all[zero_mask] = 0.0

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "TOTALKCAL_HEI2015": kcal,
        "HEI2015_ALL": hei_all,
        "HEI2015_TOTALFRT": s_tfruit,
        "HEI2015_FRT": s_wfruit,
        "HEI2015_VEG": s_tveg,
        "HEI2015_GREENNBEAN": s_gbean,
        "HEI2015_TOTALPRO": s_tpro,
        "HEI2015_SEAPLANTPRO": s_spro,
        "HEI2015_WHOLEGRAIN": s_wgrain,
        "HEI2015_DAIRY": s_dair,
        "HEI2015_FATTYACID": s_fa,
        "HEI2015_REFINEDGRAIN": s_rgrain,
        "HEI2015_SODIUM": s_na,
        "HEI2015_ADDEDSUGAR": s_asugar,
        "HEI2015_SATFAT": s_sfat,
    })
