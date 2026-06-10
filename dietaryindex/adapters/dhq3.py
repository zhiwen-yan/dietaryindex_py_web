"""
DHQ3 一步式适配器

DII_DHQ3 / AHEI_DHQ3 — 直接读取 DHQ3 CSV 文件并计算各指数。

参考 dietaryindex R 包 DII_DHQ3 / AHEI_DHQ3 源码。
"""

import numpy as np
import pandas as pd

from dietaryindex.core.dii import compute_dii
from dietaryindex.core.ahei import compute_ahei

# DHQ3 Total Daily Results 列名 → DII 参数名 映射
DHQ3_COL_TO_DII = {
    "KCAL": "KCAL",
    "PROTEIN": "PROTEIN",
    "CARBOHYDRATE": "CARB",
    "FIBER": "FIBER",
    "TOTAL_FAT": "TOTALFAT",
    "SAT_FAT": "SATFAT",
    "MONO_FAT": "MUFA",
    "POLY_FAT": "PUFA",
    "CHOLESTEROL": "CHOLES",
    "ALCOHOL": "ALCOHOL",
    "CAFFEINE": "CAFFEINE",
    "FOLIC_ACID": "FOLICACID",
    "NIACIN": "NIACIN",
    "MAGNESIUM": "MG",
    "IRON": "IRON",
    "ZINC": "ZN",
    "SELENIUM": "SE",
    "THIAMIN": "THIAMIN",
    "RIBOFLAVIN": "RIBOFLAVIN",
    "VITAMIN_B6": "VITB6",
    "VITAMIN_B12": "VITB12",
    "VITAMIN_C": "VITC",
    "VITAMIN_D": "VITD",
    "VITAMIN_A": "VITA",
    "VITAMIN_E": "VITE",
    "N3_FAT": "N3FAT",
    "N6_FAT": "N6FAT",
    "TRANS_FAT": "TRANSFAT",
    "BETA_CAROTENE": "BCAROTENE",
}


def compute_dii_dhq3(data_path):
    """
    一步式计算 DHQ3 数据的 DII

    Parameters
    ----------
    data_path : str or BytesIO
        DHQ3 导出的 Total Daily Results CSV 文件路径或 BytesIO。
        文件名通常以 results.csv 结尾。

    Returns
    -------
    pd.DataFrame
        包含 Respondent ID, DII_ALL, DII_NOETOH 及各成分分数的 DataFrame。

    Notes
    -----
    DHQ3 (Diet History Questionnaire III) 是 NCI 开发的饮食历史问卷。
    Total Daily Results CSV 包含每个参与者每日营养素和食物组估计值。
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

    id_col = None
    for candidate in ["Respondent ID", "RespondentID", "RESPONDENTID",
                       "respondent_id", "ID", "id"]:
        if candidate in df.columns:
            id_col = candidate
            break

    if id_col is not None:
        respondent_id = df[id_col].values
    else:
        respondent_id = np.arange(1, len(df) + 1)

    col_map = {}
    for dhq_col, dii_name in DHQ3_COL_TO_DII.items():
        match = [c for c in df.columns if c.upper() == dhq_col.upper().replace(" ", "_")
                 or c.upper().replace(" ", "_") == dhq_col.upper().replace(" ", "_")]
        if not match:
            match = [c for c in df.columns if dhq_col.upper().replace(" ", "_") in c.upper().replace(" ", "_")]
        if match:
            col_map[dii_name] = match[0]

    dii_kwargs = {"respondent_id": respondent_id}
    for dii_name, dhq_col in col_map.items():
        dii_kwargs[dii_name] = df[dhq_col].values

    result = compute_dii(data=df, **dii_kwargs)
    return result


# ── DHQ3 AHEI detail-level food codes (SSB identification) ──────────────────
# Coffee/Tea Food IDs
_AHEI_DHQ3_COFFEE_TEA = [16.1, 17.1, 64.1, 64.2, 1081.1, 1123.1, 1123.2, 1130.2, 1130.5]
# Drink Food IDs
_AHEI_DHQ3_DRINK = [10.6, 10.9, 11.1, 11.2, 1140.1, 1140.2, 1144.1, 1150.1, 1152.1]
_AHEI_DHQ3_SSB = _AHEI_DHQ3_COFFEE_TEA + _AHEI_DHQ3_DRINK


def compute_ahei_dhq3(data_path):
    """
    一步式计算 DHQ3 详细数据（detail.csv）的 AHEI

    精确翻译自 R 包 AHEI_DHQ3.R 源码。
    使用 DHQ3 的 detail.csv 文件（个体食物记录），通过 Food ID 识别含糖饮料等特殊食物。
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

    if "Food ID" not in df.columns:
        raise ValueError(
            "AHEI_DHQ3 需要 DHQ3 的 detail.csv 文件（含 Food ID 列）。\n"
            "如果您使用的是 Total Daily Results 文件，请使用通用版（列名映射）模式。"
        )

    food_id = pd.to_numeric(df["Food ID"], errors="coerce").values

    added_sugar_ssb = np.where(np.isin(food_id, _AHEI_DHQ3_SSB),
                                pd.to_numeric(df["*Added sugars (g)"], errors="coerce").fillna(0).values, 0)

    df["_ADDED_SUGAR_SSB"] = added_sugar_ssb

    def _safe_sum(col):
        return pd.to_numeric(df[col], errors="coerce").fillna(0).sum()

    grouped = df.groupby("Respondent ID", as_index=False).agg({
        "_ADDED_SUGAR_SSB": "sum",
        "Energy (kcal)": "sum",
        "Sex (1=male; 2=female)": "min",
    })

    for col_name in ["Dark-green vegetable (cups)",
                     "Total red/orange vegetable (cups)",
                     "Other starchy vegetable (cups)",
                     "Other vegetable (cups)",
                     "Total fruit (cups)",
                     "Juice fruit (cups)",
                     "Whole grain (oz)",
                     "Nuts, seeds, soy, and legumes (oz)",
                     "Total polyunsaturated fatty acids (g)",
                     "PFA 20:5 (Eicosapentaenoic) (g)",
                     "PFA 22:6 (Docosahexaenoic) (g)",
                     "Cured meat protein foods (oz)",
                     "Meat from beef, pork, veal, lamb, and game protein foods (oz)",
                     "Meat from organ meat protein foods (oz)",
                     "*Total trans fatty acitds (g)",
                     "Sodium (mg)",
                     "Alcohol (drink(s))"]:
        if col_name in df.columns:
            grouped[col_name] = df.groupby("Respondent ID")[col_name].sum().values

    resp_id = grouped["Respondent ID"].values
    gender = grouped["Sex (1=male; 2=female)"].values
    kcal = grouped["Energy (kcal)"].values
    kcal_safe = np.where(kcal > 0, kcal, 2000.0)

    veg_serv = (
        grouped.get("Dark-green vegetable (cups)", pd.Series(0, index=grouped.index)).values
        + (
            grouped.get("Total red/orange vegetable (cups)", pd.Series(0, index=grouped.index)).values
            + grouped.get("Other starchy vegetable (cups)", pd.Series(0, index=grouped.index)).values
            + grouped.get("Other vegetable (cups)", pd.Series(0, index=grouped.index)).values
        ) / 0.5
    )

    total_fruit = grouped.get("Total fruit (cups)", pd.Series(0, index=grouped.index)).values
    juice_fruit = grouped.get("Juice fruit (cups)", pd.Series(0, index=grouped.index)).values
    frt_serv = total_fruit - juice_fruit

    wgrain_serv = grouped.get("Whole grain (oz)", pd.Series(0, index=grouped.index)).values / 0.035274

    nutsleg_serv = grouped.get("Nuts, seeds, soy, and legumes (oz)", pd.Series(0, index=grouped.index)).values

    tot_pufa = grouped.get("Total polyunsaturated fatty acids (g)", pd.Series(0, index=grouped.index)).values
    fa205 = grouped.get("PFA 20:5 (Eicosapentaenoic) (g)", pd.Series(0, index=grouped.index)).values
    fa226 = grouped.get("PFA 22:6 (Docosahexaenoic) (g)", pd.Series(0, index=grouped.index)).values
    pufa_serv = ((tot_pufa - fa205 - fa226) * 9 / kcal_safe) * 100

    n3fat_serv = (fa205 + fa226) * 1000

    ssb_frtj_serv = grouped["_ADDED_SUGAR_SSB"].values / 26

    cured_meat = grouped.get("Cured meat protein foods (oz)", pd.Series(0, index=grouped.index)).values
    beef_meat = grouped.get("Meat from beef, pork, veal, lamb, and game protein foods (oz)", pd.Series(0, index=grouped.index)).values
    organ_meat = grouped.get("Meat from organ meat protein foods (oz)", pd.Series(0, index=grouped.index)).values
    redproc_meat_serv = (cured_meat / 1.5) + ((beef_meat + organ_meat) / 4)

    trans_fat = grouped.get("*Total trans fatty acitds (g)", pd.Series(0, index=grouped.index)).values
    trans_serv = (trans_fat * 9 / kcal_safe) * 100

    sodium = grouped.get("Sodium (mg)", pd.Series(0, index=grouped.index)).values
    sodium_serv = sodium / (kcal_safe / 2000)

    alcohol_serv = grouped.get("Alcohol (drink(s))", pd.Series(0, index=grouped.index)).values

    result = compute_ahei(
        data=grouped,
        respondent_id=resp_id,
        gender=gender,
        total_kcal=kcal_safe,
        vegetable=veg_serv,
        fruit=frt_serv,
        whole_grain=wgrain_serv,
        nut_legume=nutsleg_serv,
        n3_fat=n3fat_serv,
        pufa=pufa_serv,
        ssb_fruit_juice=ssb_frtj_serv,
        red_processed_meat=redproc_meat_serv,
        trans_fat=trans_serv,
        sodium=sodium_serv,
        alcohol=alcohol_serv,
    )
    return result
