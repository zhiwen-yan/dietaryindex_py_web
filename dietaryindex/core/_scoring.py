"""
通用评分函数库 - General Scoring Functions

为所有膳食指数提供统一的评分计算工具函数。
所有算法均从 dietaryindex R 包源码精确翻译。
"""

import numpy as np
import pandas as pd


def _safe_nanquantile(a, q):
    """
    Safely calculate nanquantile when there are infinite values (inf).
    Numpy's linear interpolation returns NaN when subtracting inf from inf,
    whereas R's quantile function handles inf correctly.
    """
    a = np.asarray(a, dtype=float)
    is_inf = np.isinf(a)
    is_pos_inf = is_inf & (a > 0)
    is_neg_inf = is_inf & (a < 0)
    if not is_inf.any():
        return np.nanquantile(a, q)
    finite_a = a[~is_inf & ~np.isnan(a)]
    if len(finite_a) == 0:
        return np.nanquantile(a, q)
    max_val = np.nanmax(finite_a)
    min_val = np.nanmin(finite_a)
    # Map infs to huge but finite numbers
    huge_pos = max_val + 1e15
    huge_neg = min_val - 1e15
    a_mapped = np.where(is_pos_inf, huge_pos, np.where(is_neg_inf, huge_neg, a))
    quantiles = np.nanquantile(a_mapped, q)
    # Map back to inf
    threshold_pos = max_val + 1e14
    threshold_neg = min_val - 1e14
    return np.where(
        quantiles > threshold_pos, np.inf,
        np.where(quantiles < threshold_neg, -np.inf, quantiles)
    )


def score_healthy(actual, min_val, max_val, min_score=0.0, max_score=5.0):
    """
    健康成分线性评分（摄入越多分越高）

    等效于 R 中的 SCORE_HEALTHY 函数：
        if actual >= max_val → max_score
        if actual <= min_val → min_score
        else → min_score + (actual - min_val) * max_score / (max_val - min_val)

    用于: AHEI, HEI2015, HEI2020, PHDI
    """
    actual = np.asarray(actual, dtype=float)
    result = np.where(
        actual >= max_val,
        max_score,
        np.where(
            actual <= min_val,
            min_score,
            min_score + (actual - min_val) * max_score / (max_val - min_val)
        )
    )
    return result


def score_unhealthy(actual, min_val, max_val, min_score=0.0, max_score=10.0):
    """
    不健康成分线性评分（摄入越多分越低）

    等效于 R 中的 SCORE_UNHEALTHY 函数：
        if actual >= min_val → min_score
        if actual <= max_val → max_score
        else → min_score + (actual - min_val) * max_score / (max_val - min_val)

    用于: AHEI, HEI2015, HEI2020, PHDI
    """
    actual = np.asarray(actual, dtype=float)
    result = np.where(
        actual >= min_val,
        min_score,
        np.where(
            actual <= max_val,
            max_score,
            min_score + (actual - min_val) * max_score / (max_val - min_val)
        )
    )
    return result


def score_quintile_healthy(actual):
    """
    五等分正向评分（健康成分，摄入越多分越高）

    等效于 R 中的 quintile_healthy 函数：
        基于数据集的五分位数，将人群分为 1-5 分

    用于: DASH, DASHI
    """
    actual = np.asarray(actual, dtype=float)
    quintiles = _safe_nanquantile(actual, np.linspace(0, 1, 6))
    conditions = [
        ((actual >= quintiles[0]) & (actual < quintiles[1])) | (actual == 0),
        (actual >= quintiles[1]) & (actual < quintiles[2]) & (actual != 0),
        (actual >= quintiles[2]) & (actual < quintiles[3]) & (actual != 0),
        (actual >= quintiles[3]) & (actual < quintiles[4]) & (actual != 0),
        (actual >= quintiles[4]) & (actual <= quintiles[5]) & (actual != 0)
    ]
    choices = [1, 2, 3, 4, 5]
    return np.select(conditions, choices, default=np.nan)


def score_quintile_unhealthy(actual):
    """
    五等分反向评分（不健康成分，摄入越多分越低）

    等效于 R 中的 quintile_unhealthy 函数：
        基于数据集的五分位数，反向分配 5-1 分

    用于: DASH, DASHI
    """
    actual = np.asarray(actual, dtype=float)
    quintiles = _safe_nanquantile(actual, np.linspace(0, 1, 6))
    conditions = [
        ((actual >= quintiles[0]) & (actual < quintiles[1])) | (actual == 0),
        (actual >= quintiles[1]) & (actual < quintiles[2]) & (actual != 0),
        (actual >= quintiles[2]) & (actual < quintiles[3]) & (actual != 0),
        (actual >= quintiles[3]) & (actual < quintiles[4]) & (actual != 0),
        (actual >= quintiles[4]) & (actual <= quintiles[5]) & (actual != 0)
    ]
    choices = [5, 4, 3, 2, 1]
    return np.select(conditions, choices, default=np.nan)


def score_median_healthy(actual):
    """
    中位数正向评分（健康成分，高于中位数=1分）

    等效于 R 中的 median_healthy 函数

    用于: MED, MEDI
    """
    actual = np.asarray(actual, dtype=float)
    median_val = np.nanmedian(actual)
    res = np.where(
        (actual < median_val) | (actual == 0),
        0.0,
        1.0
    )
    res[np.isnan(actual)] = np.nan
    return res


def score_median_unhealthy(actual):
    """
    中位数反向评分（不健康成分，高于中位数=0分）

    等效于 R 中的 median_unhealthy 函数

    用于: MED, MEDI
    """
    actual = np.asarray(actual, dtype=float)
    median_val = np.nanmedian(actual)
    res = np.where(
        (actual < median_val) | (actual == 0),
        1.0,
        0.0
    )
    res[np.isnan(actual)] = np.nan
    return res


def score_quartile_healthy(actual, score_values=(0.0, 0.25, 0.5, 0.75)):
    """
    四等分正向评分

    等效于 R 中的 quintile_healthy1 函数

    用于: ACS2020_V1
    """
    actual = np.asarray(actual, dtype=float)
    quartiles = np.nanquantile(actual, np.linspace(0, 1, 5))
    conditions = [
        actual > quartiles[3],
        (actual > quartiles[2]) & (actual <= quartiles[3]),
        (actual > quartiles[1]) & (actual <= quartiles[2]),
        actual <= quartiles[1]
    ]
    return np.select(conditions, list(reversed(score_values)), default=0)


def score_quartile_unhealthy(actual, score_values=(0.0, 1.0, 2.0, 3.0)):
    """
    四等分反向评分

    等效于 R 中的 quintile_unhealthy4 函数

    用于: ACS2020_V1
    """
    actual = np.asarray(actual, dtype=float)
    quartiles = np.nanquantile(actual, np.linspace(0, 1, 5))
    conditions = [
        actual > quartiles[3],
        (actual > quartiles[2]) & (actual <= quartiles[3]),
        (actual > quartiles[1]) & (actual <= quartiles[2]),
        actual <= quartiles[1]
    ]
    return np.select(conditions, score_values, default=0)


def score_decile_sodium(sodium_serv):
    """
    钠摄入十一等分逆序评分

    等效于 R 中 AHEI 的 SODIUM_DECILE 逻辑：
        decile 1-11 → 分数 10-0
        区间划分：
        [deciles[i], deciles[i+1]) -> 10-i (对于 i = 0..9)
        [deciles[10], deciles[11]] -> 0

    用于: AHEI
    """
    sodium_serv = np.asarray(sodium_serv, dtype=float)
    deciles = _safe_nanquantile(sodium_serv, np.linspace(0, 1, 12))
    conditions = []
    # Score 10 down to 1 (left-closed, right-open)
    for i in range(10):
        conditions.append(
            (sodium_serv >= deciles[i]) & (sodium_serv < deciles[i + 1])
        )
    # Score 0 (both boundaries closed)
    conditions.append(
        (sodium_serv >= deciles[10]) & (sodium_serv <= deciles[11])
    )
    choices = list(range(10, -1, -1))
    return np.select(conditions, choices, default=np.nan)
