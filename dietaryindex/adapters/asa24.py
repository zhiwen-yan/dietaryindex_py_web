"""
ASA24 一步式适配器

DII_ASA24 — 直接读取 ASA24 Totals.csv 文件，
按参与者汇总所有回忆记录并计算 DII。

参考 dietaryindex R 包 DII_ASA24 源码。
"""

import numpy as np
import pandas as pd

from dietaryindex.core.dii import compute_dii

# ASA24 Totals.csv 列名 → DII 参数名 映射
ASA24_COL_TO_DII = {
    "KCAL": "KCAL",
    "PROT": "PROTEIN",
    "CARB": "CARB",
    "TFIBE": "FIBER",
    "TFAT": "TOTALFAT",
    "SFAT": "SATFAT",
    "MFAT": "MUFA",
    "PFAT": "PUFA",
    "CHOLE": "CHOLES",
    "ALCO": "ALCOHOL",
    "CAFF": "CAFFEINE",
    "FOLA": "FOLICACID",
    "NIA": "NIACIN",
    "MG": "MG",
    "IRON": "IRON",
    "ZINC": "ZN",
    "SELE": "SE",
    "THIA": "THIAMIN",
    "RIBO": "RIBOFLAVIN",
    "VITB6": "VITB6",
    "VITB12": "VITB12",
    "VITC": "VITC",
    "VITD": "VITD",
    "VITA": "VITA",
    "ATOC": "VITE",
    "N3FAT": "N3FAT",
    "N6FAT": "N6FAT",
}


def compute_dii_asa24(data_path, recall_summarize=True):
    """
    一步式计算 ASA24 数据的 DII

    Parameters
    ----------
    data_path : str or BytesIO
        ASA24 导出的 Totals.csv 文件路径或 BytesIO。
    recall_summarize : bool, default True
        是否按每人每天平均所有回忆记录。默认 True。

    Returns
    -------
    pd.DataFrame
        包含 UserName, DII_ALL, DII_NOETOH 及各成分分数的 DataFrame。
        每人一行 (如果 recall_summarize=True)。

    Notes
    -----
    ASA24 (Automated Self-Administered 24-hour Dietary Assessment Tool)
    是美国 NCI 开发的在线 24 小时膳食回顾工具。
    导出数据中，Totals.csv 包含每个回忆日的营养素总量。
    """
    import os
    from io import BytesIO

    if isinstance(data_path, (str, os.PathLike)):
        df = pd.read_csv(data_path, low_memory=False)
    elif isinstance(data_path, BytesIO):
        data_path.seek(0)
        df = pd.read_csv(data_path, low_memory=False)
    else:
        raise ValueError(f"不支持的文件类型: {type(data_path)}")

    col_map = {}
    for asa_col, dii_name in ASA24_COL_TO_DII.items():
        match = [c for c in df.columns if c.upper() == asa_col or c.upper().startswith(asa_col + "_")]
        if match:
            col_map[dii_name] = match[0]

    if recall_summarize:
        id_col = None
        for candidate in ["UserName", "username", "UserName", "USERNAME"]:
            if candidate in df.columns:
                id_col = candidate
                break

        if id_col is not None:
            agg_dict = {col_map[k]: "mean" for k in col_map}
            agg_dict[id_col] = "first"
            df = df.groupby(id_col, as_index=False).agg(agg_dict)

    # 为每行分配 ID
    if "UserName" in df.columns:
        respondent_id = df["UserName"].values
    elif "username" in df.columns:
        respondent_id = df["username"].values
    else:
        respondent_id = np.arange(1, len(df) + 1)

    dii_kwargs = {"respondent_id": respondent_id}
    for dii_name, asa_col in col_map.items():
        dii_kwargs[dii_name] = df[asa_col].values

    result = compute_dii(data=df, **dii_kwargs)
    return result
