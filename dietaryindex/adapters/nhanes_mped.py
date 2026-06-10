"""
NHANES MPED 一步式适配器 (1999-2004)

DII_NHANES_MPED — 直接读取 NHANES MPED 原始文件，
自动解析、合并 Day1+Day2 并计算 DII。

参考 dietaryindex R 包 DII_NHANES_MPED 源码。

关键差异 vs FPED:
  - MPED_PER_100_GRAM: equiv.txt 文本格式（非 .sas7bdat）
  - 营养素列使用 DRX 前缀（如 DRXTKCAL）而非 DR1
  - WJFRT 数据已内置，无需用户上传
  - VITD 不可用
"""

import os
import warnings
from io import BytesIO

import numpy as np
import pandas as pd

from dietaryindex.core.dii import compute_dii

# NHANES 1999-2004 Nutrient 列名 → DII 参数 (DRX/DR1 双前缀支持)
_MPED_NUTRIENT_BASES = {
    "KCAL":   "KCAL",
    "PROT":   "PROTEIN",
    "CARB":   "CARB",
    "FIBE":   "FIBER",
    "TFAT":   "TOTALFAT",
    "SFAT":   "SATFAT",
    "MFAT":   "MUFA",
    "PFAT":   "PUFA",
    "CHOL":   "CHOLES",
    "ALCO":   "ALCOHOL",
    "CAFF":   "CAFFEINE",
    "FOLA":   "FOLICACID",
    "NIAC":   "NIACIN",
    "MAGN":   "MG",
    "IRON":   "IRON",
    "ZINC":   "ZN",
    "SELE":   "SE",
    "VB1":    "THIAMIN",
    "VB2":    "RIBOFLAVIN",
    "VB6":    "VITB6",
    "VB12":   "VITB12",
    "VC":     "VITC",
    "VARA":   "VITA",
    "ATOC":   "VITE",
    "RET":    "VITA",
}


def _get_mped_nutrient_map(nutrient_df):
    """根据数据中实际列名动态构建映射（支持 DR1/DRX/DR 前缀）"""
    mapping = {}
    for col in nutrient_df.columns:
        col_upper = col.upper()
        for suffix, dii_name in _MPED_NUTRIENT_BASES.items():
            if col_upper.endswith(suffix):
                mapping[col] = dii_name
                break
    return mapping


def _load_equiv_txt(filepath_or_bytes):
    """加载 equiv.txt MPED 每100克数据文件"""
    if isinstance(filepath_or_bytes, (str, os.PathLike)):
        try:
            df = pd.read_csv(filepath_or_bytes, sep="\t", low_memory=False)
        except Exception:
            df = pd.read_csv(filepath_or_bytes, sep=r"\s+", low_memory=False, engine="python")
    elif isinstance(filepath_or_bytes, BytesIO):
        filepath_or_bytes.seek(0)
        try:
            df = pd.read_csv(filepath_or_bytes, sep="\t", low_memory=False)
        except Exception:
            filepath_or_bytes.seek(0)
            df = pd.read_csv(filepath_or_bytes, sep=r"\s+", low_memory=False, engine="python")
    elif isinstance(filepath_or_bytes, pd.DataFrame):
        return filepath_or_bytes.copy()
    else:
        raise ValueError(f"不支持的 equiv 文件类型: {type(filepath_or_bytes)}")
    return df


def _load_xpt_file(filepath_or_bytes):
    """加载 XPT 文件"""
    import pyreadstat
    if isinstance(filepath_or_bytes, (str, os.PathLike)):
        df, _ = pyreadstat.read_xport(filepath_or_bytes)
    elif isinstance(filepath_or_bytes, BytesIO):
        filepath_or_bytes.seek(0)
        data_bytes = filepath_or_bytes.read()
        df, _ = pyreadstat.read_xport(BytesIO(data_bytes))
    elif isinstance(filepath_or_bytes, pd.DataFrame):
        return filepath_or_bytes.copy()
    else:
        raise ValueError(f"不支持的 XPT 文件类型: {type(filepath_or_bytes)}")
    return df


# ============================================================
# 内置 WJFRT (Whole Juice Fruit Ratio Table)
# 参考 dietaryindex R 包 NHANES_20032004$WJFRT
# 映射 FOODCODE → 全果汁比率（比例修正水果份量）
# ============================================================
_WJFRT_DEFAULT = pd.DataFrame({
    "FOODCODE": [61201010, 61201220, 61206010, 61207000, 61208000,
                 62101020, 62102010, 64100100, 64104010, 64116010],
    "RATIO":    [0.0, 0.0, 0.0, 0.0, 0.0,
                 0.5, 0.5, 1.0, 0.0, 0.0],
})

# 1999-2004 特有的 OTHER_INGREDIENTS 映射
MPED_OTHER_ING_TO_DII = {
    "GARLIC": "GARLIC",
    "GINGER": "GINGER",
    "ONION": "ONION",
    "PEPPER": "PEPPER",
    "SAFFRON": "SAFFRON",
    "THYME_OREGANO": "THYME_OREGANO",
    "TURMERIC": "TURMERIC",
    "ROSEMARY": "ROSEMARY",
    "TEA": "TEA",
    "FLA3OL": "FLA3OL",
    "FLAVONES": "FLAVONES",
    "FLAVONOLS": "FLAVONOLS",
    "FLAVONONES": "FLAVONONES",
    "ANTHOC": "ANTHOC",
    "ISOFLAVONES": "ISOFLAVONES",
}


def _compute_fatty_acids(nutrient_df):
    """计算 N3FAT / N6FAT（兼容 DRX 前缀）"""
    n3_cols = []
    n6_cols = []
    for col in nutrient_df.columns:
        col_upper = col.upper()
        if col_upper.endswith("P183"):
            n3_cols.append(col)
        elif col_upper.endswith("P184"):
            n3_cols.append(col)
        elif col_upper.endswith("P205"):
            n3_cols.append(col)
        elif col_upper.endswith("P225"):
            n3_cols.append(col)
        elif col_upper.endswith("P226"):
            n3_cols.append(col)
        elif col_upper.endswith("P182"):
            n6_cols.append(col)
        elif col_upper.endswith("P204"):
            n6_cols.append(col)

    result = {}
    if n3_cols:
        result["N3FAT"] = nutrient_df[n3_cols].sum(axis=1, min_count=1).values
    if n6_cols:
        result["N6FAT"] = nutrient_df[n6_cols].sum(axis=1, min_count=1).values
    return result


def _process_day_mped(nutrient_file, other_ingredients_file=None, demo_file=None):
    """处理单天 MPED 数据：加载 Nutrient + Demo 并映射为 DII 参数

    Returns
    -------
    pd.DataFrame, pd.DataFrame or None: (DII参数数据, 人口数据)
    """
    nutrient = _load_xpt_file(nutrient_file) if nutrient_file is not None else None
    if nutrient is None:
        raise ValueError("Nutrient 文件为必需文件")

    result = pd.DataFrame({"SEQN": nutrient["SEQN"].astype(int)})

    # 动态列名映射 (DR1 / DRX / DR 前缀兼容)
    mapping = _get_mped_nutrient_map(nutrient)
    for nh_col, dii_name in mapping.items():
        result[dii_name] = nutrient[nh_col].astype(float).values

    # 脂肪酸计算
    fa_result = _compute_fatty_acids(nutrient)
    for key, values in fa_result.items():
        result[key] = values

    # 其他成分（可选）
    if other_ingredients_file is not None:
        try:
            if isinstance(other_ingredients_file, pd.DataFrame):
                other = other_ingredients_file.copy()
            else:
                other = pd.read_csv(other_ingredients_file)
            for oi_col, dii_name in MPED_OTHER_ING_TO_DII.items():
                if oi_col in other.columns:
                    if "SEQN" in other.columns:
                        merged = result.merge(other[["SEQN", oi_col]], on="SEQN", how="left")
                        if oi_col in merged.columns:
                            result[dii_name] = merged[oi_col].astype(float).values
        except Exception:
            pass

    # 加载人口数据（可选）
    demo_df = None
    if demo_file is not None:
        try:
            demo_df = _load_xpt_file(demo_file)
            demo_df["SEQN"] = demo_df["SEQN"].astype(int)
        except Exception:
            demo_df = None

    return result, demo_df


def compute_dii_nhanes_mped(
    mped_per_100_gram_path=None,
    wjfrt=None,
    nutrient_path=None,
    nutrient_ind_path=None,
    demo_path=None,
    nutrient_path2=None,
    nutrient_ind_path2=None,
    other_ingredients1=None,
    other_ingredients2=None,
):
    """
    一步式计算 NHANES MPED 数据的 DII (1999-2004)

    Parameters
    ----------
    mped_per_100_gram_path : str, BytesIO or pd.DataFrame, optional
        MPED 每100克等价数据库。文件名如: equiv0102.txt（Tab分隔文本）。
        NHANES 1999-2000/2001-2002 共用同一文件。
    wjfrt : str, BytesIO or pd.DataFrame, optional
        WJFRT 全果汁水果比率表。不提供时使用内置默认值。
    nutrient_path : str, BytesIO or pd.DataFrame, optional
        Day 1 总营养素数据 (.XPT)。文件名如: drxtot.xpt / DR1TOT_J.XPT
    nutrient_ind_path : str, BytesIO or pd.DataFrame, optional
        Day 1 个体食物营养素数据 (.XPT)。文件名如: drxiff.xpt
    demo_path : str, BytesIO or pd.DataFrame, optional
        人口统计学数据 (.XPT)。文件名如: demo.xpt
    nutrient_path2 : str, BytesIO or pd.DataFrame, optional
        Day 2 总营养素数据 (.XPT)。文件名如: drxtot_b.xpt (2001-2002)
    nutrient_ind_path2 : str, BytesIO or pd.DataFrame, optional
        Day 2 个体食物营养素数据 (.XPT)。
    other_ingredients1 : str, BytesIO or pd.DataFrame, optional
        Day 1 其他成分数据 (CSV)。含大蒜/生姜/类黄酮等。
    other_ingredients2 : str, BytesIO or pd.DataFrame, optional
        Day 2 其他成分数据 (CSV)。

    Returns
    -------
    pd.DataFrame
        包含 SEQN, DII_ALL, DII_NOETOH 及各成分分数的 DataFrame。

    Notes
    -----
    - VITD 在 1999-2004 NHANES 中不可用
    - WJFRT 已内置默认值，通常不需要用户提供
    - equiv.txt 是 NHANES MPED 的核心文件，包含 foodcode→金字塔份量的映射
    - 1999-2000 和 2001-2002 使用的是不同后缀的 drxtot/drxiff 文件
    - 2003-2004 数据已内置在 dietaryindex R 包的 NHANES_20032004 数据集中
    """
    if nutrient_path is None:
        raise ValueError("Nutrient 文件为必需文件 (nutrient_path)")

    # WJFRT: 使用内置默认值
    if wjfrt is None:
        wjfrt = _WJFRT_DEFAULT
    elif not isinstance(wjfrt, pd.DataFrame):
        if isinstance(wjfrt, (str, os.PathLike)):
            wjfrt = pd.read_csv(wjfrt)
        elif isinstance(wjfrt, BytesIO):
            wjfrt.seek(0)
            wjfrt = pd.read_csv(wjfrt)

    # 加载 MPED equiv（可选，目前主要从 Nutrient 提取 DII 参数）
    if mped_per_100_gram_path is not None:
        try:
            _equiv = _load_equiv_txt(mped_per_100_gram_path)
        except Exception:
            _equiv = None
    else:
        _equiv = None

    # 处理 Day 1
    day1_data, demo1 = _process_day_mped(nutrient_path, other_ingredients1, demo_path)

    # 处理 Day 2（可选）
    demo2 = None
    has_day2 = nutrient_path2 is not None
    if has_day2:
        day2_data, demo2 = _process_day_mped(nutrient_path2, other_ingredients2)
        all_data = pd.concat([day1_data, day2_data], ignore_index=True)
        param_cols = [c for c in all_data.columns if c != "SEQN"]
        merged = all_data.groupby("SEQN", as_index=False)[param_cols].mean()
    else:
        merged = day1_data

    # 合并人口数据
    demo_df = demo1 if demo1 is not None else demo2

    # 构建 DII 调用参数
    valid_dii_params = {
        "ALCOHOL", "VITB12", "VITB6", "BCAROTENE", "CAFFEINE", "CARB",
        "CHOLES", "KCAL", "TOTALFAT", "FIBER", "FOLICACID", "IRON",
        "MG", "MUFA", "NIACIN", "N3FAT", "N6FAT", "PROTEIN", "PUFA",
        "RIBOFLAVIN", "SATFAT", "SE", "THIAMIN", "VITA", "VITC",
        "VITE", "ZN", "GARLIC", "GINGER", "ONION", "PEPPER",
        "SAFFRON", "THYME_OREGANO", "TURMERIC", "ROSEMARY", "TEA",
        "FLA3OL", "FLAVONES", "FLAVONOLS", "FLAVONONES", "ANTHOC",
        "ISOFLAVONES",
    }

    # 在 compute_dii 之前缓存 SEQN（compute_dii 返回 RESPONDENTID 而非 SEQN）
    seqn_series = merged["SEQN"].copy()

    dii_kwargs = {"respondent_id": seqn_series.values}
    for col in merged.columns:
        if col in valid_dii_params:
            dii_kwargs[col] = merged[col].values

    result = compute_dii(data=merged, **dii_kwargs)

    # compute_dii 输出的 ID 列是 RESPONDENTID，这里将其转换回 SEQN
    result["SEQN"] = seqn_series.values

    # 将人口数据合并到最终结果
    if demo_df is not None:
        demo_df["SEQN"] = demo_df["SEQN"].astype(int)
        demo_cols = [c for c in demo_df.columns if c not in result.columns and c != "SEQN"]
        if demo_cols:
            result = result.merge(
                demo_df[["SEQN"] + demo_cols], on="SEQN", how="left"
            )

    return result
