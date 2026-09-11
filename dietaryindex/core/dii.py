"""
DII - Dietary Inflammatory Index 核心计算模块

精确翻译自 dietaryindex R 包 DII.R 源码:
https://github.com/jamesjiadazhan/dietaryindex/blob/main/R/DII.R

算法参考:
    Shivappa, N., et al. (2014). Designing and developing a literature-derived,
    population-based dietary inflammatory index.
    Public Health Nutrition, 17(8), 1689-1696.
"""

import warnings

import numpy as np
import pandas as pd
from scipy.stats import norm

from dietaryindex.reference.dii_global import DII_REFERENCE, DII_VARIABLE_ORDER


def compute_dii(
    data,
    respondent_id=None,
    repeat_num=1,
    **kwargs
):
    """
    计算膳食炎症指数 (Dietary Inflammatory Index, DII)

    Parameters
    ----------
    data : pd.DataFrame
        包含所有食物和营养素摄入数据的原始数据。
    respondent_id : str or array-like
        每个参与者的唯一标识符。如果传入字符串，则从 data 中选取对应列。
        如果传入 array-like，则直接使用。
    repeat_num : int or array-like, default 1
        每个参与者的重复记录编号。默认为 1。
    **kwargs : dict
        其他 DII 参数与其所在列名的映射，例如:
        ALCOHOL=data['alcohol_g'], VITB12=data['vitamin_b12_mcg'], ...

    Returns
    -------
    pd.DataFrame
        包含 DII_ALL, DII_NOETOH 以及各成分分数的 DataFrame。
        行与输入数据对齐。

    Notes
    -----
    无需提供所有 45 个参数。只提供已有的参数即可，
    未提供的参数将被排除在计算之外，对应的输出列将显示 0。

    Examples
    --------
    >>> import pandas as pd
    >>> from dietaryindex import compute_dii
    >>> df = pd.DataFrame({
    ...     'id': [1, 2],
    ...     'alcohol': [0, 10],
    ...     'vitb12': [2.4, 3.0],
    ...     'vitb6': [1.5, 2.0],
    ... })
    >>> result = compute_dii(
    ...     data=df,
    ...     respondent_id=df['id'],
    ...     ALCOHOL=df['alcohol'],
    ...     VITB12=df['vitb12'],
    ...     VITB6=df['vitb6'],
    ... )
    """
    n_rows = len(data)

    if respondent_id is None:
        rid = pd.Series(range(1, n_rows + 1), name="RESPONDENTID")
    elif isinstance(respondent_id, str):
        rid = data[respondent_id].reset_index(drop=True).rename("RESPONDENTID")
    else:
        rid = pd.Series(np.asarray(respondent_id), name="RESPONDENTID").reset_index(drop=True)

    if isinstance(repeat_num, (int, float)):
        rpt = pd.Series(np.full(n_rows, repeat_num), name="REPEATNUM")
    else:
        rpt = pd.Series(np.asarray(repeat_num), name="REPEATNUM").reset_index(drop=True)

    component_keys = [
        "ALCOHOL", "VITB12", "VITB6", "BCAROTENE", "CAFFEINE", "CARB",
        "CHOLES", "KCAL", "EUGENOL", "TOTALFAT", "FIBER", "FOLICACID",
        "GARLIC", "GINGER", "IRON", "MG", "MUFA", "NIACIN", "N3FAT",
        "N6FAT", "ONION", "PROTEIN", "PUFA", "RIBOFLAVIN", "SAFFRON",
        "SATFAT", "SE", "THIAMIN", "TRANSFAT", "TURMERIC", "VITA",
        "VITC", "VITD", "VITE", "ZN", "TEA", "FLA3OL", "FLAVONES",
        "FLAVONOLS", "FLAVONONES", "ANTHOC", "ISOFLAVONES", "PEPPER",
        "THYME_OREGANO", "ROSEMARY",
    ]

    records = []
    for i in range(n_rows):
        rec = {"RESPONDENTID": rid.iloc[i], "REPEATNUM": rpt.iloc[i]}
        for key in component_keys:
            if key in kwargs and kwargs[key] is not None:
                val = kwargs[key]
                if isinstance(val, pd.DataFrame):
                    rec[key] = val.iloc[i, 0]
                elif isinstance(val, pd.Series):
                    rec[key] = val.iloc[i]
                elif isinstance(val, np.ndarray):
                    rec[key] = val[i]
                else:
                    rec[key] = float(val)
            else:
                rec[key] = np.nan
        records.append(rec)

    long_df = pd.DataFrame(records)

    id_vars = ["RESPONDENTID", "REPEATNUM"]
    melted = long_df.melt(
        id_vars=id_vars,
        value_vars=component_keys,
        var_name="Variable",
        value_name="Value"
    )

    ref_rows = []
    for var in component_keys:
        if var in DII_REFERENCE:
            ref = DII_REFERENCE[var]
            ref_rows.append({
                "Variable": var,
                "Overall_inflammatory_score": ref["inflammatory_score"],
                "Global_mean": ref["global_mean"],
                "SD": ref["sd"],
            })
    ref_df = pd.DataFrame(ref_rows)

    merged = melted.merge(ref_df, on="Variable", how="left")

    merged["Z_SCORE"] = np.where(
        merged["SD"] > 0,
        (merged["Value"] - merged["Global_mean"]) / merged["SD"],
        0.0
    )
    merged["PERCENTILE"] = norm.cdf(merged["Z_SCORE"]) * 2 - 1
    merged["IND_DII_SCORE"] = merged["PERCENTILE"] * merged["Overall_inflammatory_score"]

    base_rows = long_df[id_vars].drop_duplicates().reset_index(drop=True)
    wide = merged.pivot_table(
        index=["RESPONDENTID", "REPEATNUM"],
        columns="Variable",
        values="IND_DII_SCORE",
        aggfunc=lambda s: s.sum(min_count=1),
    ).reset_index()
    wide = base_rows.merge(wide, on=id_vars, how="left")

    for key in component_keys:
        if key not in wide.columns:
            wide[key] = np.nan

    available_components = [
        c for c in component_keys
        if c in wide.columns and wide[c].notna().any()
    ]

    if available_components:
        wide["Components_Used"] = wide[available_components].notna().sum(axis=1)
        wide["DII_ALL"] = wide[available_components].sum(axis=1, min_count=1)
        no_etoh_components = [c for c in available_components if c != "ALCOHOL"]
        wide["DII_NOETOH"] = wide[no_etoh_components].sum(axis=1, min_count=1) if no_etoh_components else np.nan
    else:
        wide["Components_Used"] = 0
        wide["DII_ALL"] = np.nan
        wide["DII_NOETOH"] = np.nan

    for key in component_keys:
        if key not in kwargs or kwargs[key] is None:
            wide[key] = 0.0
        else:
            wide[key] = pd.to_numeric(wide[key], errors="coerce")

    output_cols = ["RESPONDENTID", "DII_ALL", "DII_NOETOH", "Components_Used", "REPEATNUM"]
    for key in component_keys:
        if key in wide.columns:
            output_cols.append(key)

    result = wide[output_cols].copy()
    result = result.reset_index(drop=True)

    for col in result.columns:
        if col not in ["RESPONDENTID", "REPEATNUM", "DII_ALL", "DII_NOETOH", "Components_Used"]:
            result[col] = pd.to_numeric(result[col], errors="coerce")

    return result
