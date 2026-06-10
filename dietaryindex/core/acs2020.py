"""
ACS2020 - American Cancer Society 2020 Dietary Index

精确翻译自 dietaryindex R 包 ACS2020_V1.R 与 ACS2020_V2.R 源码。
V1: 基于四等分的饮食评分，总分 0-15。
V2: 使用 %能量 计算高加工食品和精制谷物组分，且包括蔬菜和水果评分。
"""

import numpy as np
import pandas as pd


def _compute_acs2020_components(
    gender,
    vegetable,
    vegetable_items,
    fruit,
    fruit_items,
    whole_grain,
    red_processed_meat,
    hpf_rg_val,
    ssb_fruit_juice,
):
    gend = np.asarray(gender, dtype=float)
    veg_s = np.asarray(vegetable, dtype=float)
    veg_i = np.asarray(vegetable_items, dtype=float)
    frt_s = np.asarray(fruit, dtype=float)
    frt_i = np.asarray(fruit_items, dtype=float)
    wg = np.asarray(whole_grain, dtype=float)
    rpm = np.asarray(red_processed_meat, dtype=float)
    hpf = np.asarray(hpf_rg_val, dtype=float)
    ssb = np.asarray(ssb_fruit_juice, dtype=float)

    n = len(gend)
    unique_genders = pd.Series(gend).unique()

    def _quartile_healthy(values, scores):
        result = np.full(n, np.nan)
        for g in unique_genders:
            if pd.isna(g):
                mask = pd.Series(gend).isna().values
            else:
                mask = gend == g
            if not mask.any():
                continue
            g_vals = values[mask]
            with np.errstate(divide='ignore', invalid='ignore'):
                q = np.nanquantile(g_vals, np.linspace(0, 1, 5))
            
            # R uses right-closed, left-open intervals except for the first one:
            # actual <= quintile[5] & actual > quintile[4] ~ 0.75
            # actual <= quintile[4] & actual > quintile[3] ~ 0.5
            # actual <= quintile[3] & actual > quintile[2] ~ 0.25
            # actual <= quintile[2] & actual >= quintile[1] ~ 0
            conditions = [
                (g_vals > q[3]),
                (g_vals > q[2]) & (g_vals <= q[3]),
                (g_vals > q[1]) & (g_vals <= q[2]),
                (g_vals >= q[0]) & (g_vals <= q[1])
            ]
            choices = list(reversed(scores))
            res = np.select(conditions, choices, default=np.nan)
            result[mask] = res
        return result

    def _quartile_unhealthy(values, scores):
        result = np.full(n, np.nan)
        for g in unique_genders:
            if pd.isna(g):
                mask = pd.Series(gend).isna().values
            else:
                mask = gend == g
            if not mask.any():
                continue
            g_vals = values[mask]
            with np.errstate(divide='ignore', invalid='ignore'):
                q = np.nanquantile(g_vals, np.linspace(0, 1, 5))
            
            # R unhealthy:
            # actual <= quintile[5] & actual > quintile[4] ~ 0
            # actual <= quintile[4] & actual > quintile[3] ~ 0.5
            # actual <= quintile[3] & actual > quintile[2] ~ 1
            # actual <= quintile[2] & actual >= quintile[1] ~ 1.5
            conditions = [
                (g_vals > q[3]),
                (g_vals > q[2]) & (g_vals <= q[3]),
                (g_vals > q[1]) & (g_vals <= q[2]),
                (g_vals >= q[0]) & (g_vals <= q[1])
            ]
            choices = scores
            res = np.select(conditions, choices, default=np.nan)
            result[mask] = res
        return result

    acs_veg = _quartile_healthy(veg_s, [0.0, 0.25, 0.5, 0.75])
    acs_veg_i = _quartile_healthy(veg_i, [0.0, 0.25, 0.5, 0.75])
    acs_frt = _quartile_healthy(frt_s, [0.0, 0.25, 0.5, 0.75])
    acs_frt_i = _quartile_healthy(frt_i, [0.0, 0.25, 0.5, 0.75])
    acs_wg = _quartile_healthy(wg, [0.0, 1.0, 2.0, 3.0])
    acs_rpm = _quartile_unhealthy(rpm, [0.0, 1.0, 2.0, 3.0])
    acs_hpf = _quartile_unhealthy(hpf, [0.0, 0.5, 1.0, 1.5])

    # SSB component
    acs_ssb = np.where(ssb >= 1, 0.0,
                np.where((ssb < 1) & (ssb >= 0.428), 0.5,
                np.where((ssb < 0.428) & (ssb > 0), 1.0,
                np.where(ssb <= 0, 1.5, np.nan))))

    return {
        "veg": acs_veg,
        "veg_i": acs_veg_i,
        "frt": acs_frt,
        "frt_i": acs_frt_i,
        "wg": acs_wg,
        "rpm": acs_rpm,
        "hpf": acs_hpf,
        "ssb": acs_ssb,
    }


def compute_acs2020_v1(
    data,
    respondent_id,
    gender,
    vegetable,
    vegetable_items,
    fruit,
    fruit_items,
    whole_grain,
    red_processed_meat,
    hpf_rg_ratio,
    ssb_fruit_juice,
):
    """
    计算 ACS2020 V1 (高加工食品用百分比)
    """
    rid = np.asarray(respondent_id)
    gend = np.asarray(gender, dtype=float)

    comp = _compute_acs2020_components(
        gender=gend,
        vegetable=vegetable,
        vegetable_items=vegetable_items,
        fruit=fruit,
        fruit_items=fruit_items,
        whole_grain=whole_grain,
        red_processed_meat=red_processed_meat,
        hpf_rg_val=hpf_rg_ratio,
        ssb_fruit_juice=ssb_fruit_juice,
    )

    acs_all = comp["veg"] + comp["veg_i"] + comp["frt"] + comp["frt_i"] + comp["wg"] + comp["rpm"] + comp["hpf"] + comp["ssb"]

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "GENDER": gend,
        "ACS2020_V1_ALL": acs_all,
        "ACS2020_VEG": comp["veg"],
        "ACS2020_VEG_ITEMS": comp["veg_i"],
        "ACS2020_FRT": comp["frt"],
        "ACS2020_FRT_ITEMS": comp["frt_i"],
        "ACS2020_WGRAIN": comp["wg"],
        "ACS2020_REDPROC_MEAT": comp["rpm"],
        "ACS2020_HPFRG_RATIO": comp["hpf"],
        "ACS2020_SSB_FRTJ": comp["ssb"],
    })


def compute_acs2020_v2(
    data,
    respondent_id,
    gender,
    total_kcal,
    vegetable,
    vegetable_items,
    fruit,
    fruit_items,
    whole_grain,
    red_processed_meat,
    hpf_servings,
    ssb_fruit_juice,
):
    """
    计算 ACS2020 V2 (1000kcal标准化高加工食品/精制谷物组分)
    """
    rid = np.asarray(respondent_id)
    gend = np.asarray(gender, dtype=float)
    kcal = np.asarray(total_kcal, dtype=float)

    with np.errstate(divide='ignore', invalid='ignore'):
        hpf_rg_serv_per_1000 = np.asarray(hpf_servings, dtype=float) / (kcal / 1000.0)

    comp = _compute_acs2020_components(
        gender=gend,
        vegetable=vegetable,
        vegetable_items=vegetable_items,
        fruit=fruit,
        fruit_items=fruit_items,
        whole_grain=whole_grain,
        red_processed_meat=red_processed_meat,
        hpf_rg_val=hpf_rg_serv_per_1000,
        ssb_fruit_juice=ssb_fruit_juice,
    )

    acs_all = comp["veg"] + comp["veg_i"] + comp["frt"] + comp["frt_i"] + comp["wg"] + comp["rpm"] + comp["hpf"] + comp["ssb"]

    return pd.DataFrame({
        "RESPONDENTID": rid,
        "GENDER": gend,
        "ACS2020_V2_ALL": acs_all,
        "TOTALKCAL_ACS2020": kcal,
        "ACS2020_VEG": comp["veg"],
        "ACS2020_VEG_ITEMS": comp["veg_i"],
        "ACS2020_FRT": comp["frt"],
        "ACS2020_FRT_ITEMS": comp["frt_i"],
        "ACS2020_WGRAIN": comp["wg"],
        "ACS2020_REDPROC_MEAT": comp["rpm"],
        "ACS2020_HPFRG": comp["hpf"],
        "ACS2020_SSB_FRTJ": comp["ssb"],
    })
