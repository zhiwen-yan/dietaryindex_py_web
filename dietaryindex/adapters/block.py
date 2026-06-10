"""
BLOCK 食物频率问卷 一步式适配器

DII_BLOCK / AHEI_BLOCK / AHEIP_BLOCK — 直接读取 BLOCK FFQ 原始数据文件并计算各指数。

参考 dietaryindex R 包 DII_BLOCK / AHEI_BLOCK / AHEIP_BLOCK 源码。
"""

import numpy as np
import pandas as pd

from dietaryindex.core.dii import compute_dii
from dietaryindex.core.ahei import compute_ahei
from dietaryindex.core.aheip import compute_aheip

# BLOCK FFQ 常见列名 → DII 参数名 映射
BLOCK_COL_TO_DII = {
    "KCAL": "KCAL",
    "PROTEIN": "PROTEIN",
    "CARB": "CARB",
    "FIBER": "FIBER",
    "TOTALFAT": "TOTALFAT",
    "SATFAT": "SATFAT",
    "MONOFAT": "MUFA",
    "POLYFAT": "PUFA",
    "CHOLESTEROL": "CHOLES",
    "ALCOHOL": "ALCOHOL",
    "CAFFEINE": "CAFFEINE",
    "FOLATE": "FOLICACID",
    "NIACIN": "NIACIN",
    "MAGNESIUM": "MG",
    "IRON": "IRON",
    "ZINC": "ZN",
    "SELENIUM": "SE",
    "THIAMIN": "THIAMIN",
    "RIBOFLAVIN": "RIBOFLAVIN",
    "VITAMINB6": "VITB6",
    "VITAMINB12": "VITB12",
    "VITAMINC": "VITC",
    "VITAMIND": "VITD",
    "VITAMINA": "VITA",
    "VITAMINE": "VITE",
    "TRANSFAT": "TRANSFAT",
    "BETACAROTENE": "BCAROTENE",
    "OMEGA3": "N3FAT",
    "OMEGA6": "N6FAT",
}


def compute_dii_block(raw_data):
    """
    一步式计算 BLOCK FFQ 数据的 DII

    Parameters
    ----------
    raw_data : str, BytesIO or pd.DataFrame
        BLOCK 食物频率问卷原始数据文件 (CSV/Excel) 或 DataFrame。

    Returns
    -------
    pd.DataFrame
        包含 RESPONDENTID, DII_ALL, DII_NOETOH 及各成分分数的 DataFrame。

    Notes
    -----
    BLOCK FFQ (Block Food Frequency Questionnaire) 是常用的食物频率问卷。
    其原始数据已经包含每日营养素和食物组估计值，可直接映射到 DII 参数。
    如果数据中包含 RESPONDENTID 列则使用，否则按行编号。
    """
    import os
    from io import BytesIO

    if isinstance(raw_data, pd.DataFrame):
        df = raw_data.copy()
    elif isinstance(raw_data, (str, os.PathLike)):
        fname_lower = str(raw_data).lower()
        if fname_lower.endswith(".csv"):
            df = pd.read_csv(raw_data)
        elif fname_lower.endswith((".xlsx", ".xls")):
            df = pd.read_excel(raw_data)
        else:
            raise ValueError(f"不支持的文件格式: {raw_data}")
    elif isinstance(raw_data, BytesIO):
        raw_data.seek(0)
        try:
            df = pd.read_csv(raw_data)
        except Exception:
            raw_data.seek(0)
            df = pd.read_excel(raw_data)
    else:
        raise ValueError(f"不支持的文件类型: {type(raw_data)}")

    id_col = None
    for candidate in ["RESPONDENTID", "RespondentID", "respondent_id",
                       "ID", "id", "SUBJECTID", "SUBJECT_ID"]:
        if candidate in df.columns:
            id_col = candidate
            break

    respondent_id = df[id_col].values if id_col else np.arange(1, len(df) + 1)

    col_map = {}
    for block_col, dii_name in BLOCK_COL_TO_DII.items():
        match = [c for c in df.columns if c.upper().replace("_", "").replace(" ", "") ==
                 block_col.upper().replace("_", "").replace(" ", "")]
        if not match:
            match = [c for c in df.columns if block_col.upper().replace("_", "")
                     in c.upper().replace("_", "").replace(" ", "")]
        if match:
            col_map[dii_name] = match[0]

    dii_kwargs = {"respondent_id": respondent_id}
    for dii_name, block_col in col_map.items():
        dii_kwargs[dii_name] = df[block_col].values

    result = compute_dii(data=df, **dii_kwargs)
    return result


# ── Standard BLOCK frequency and portion lookup tables ──────────────────────
_STD_FOOD_FREQ = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
_STD_FREQ_SERV = np.array([0, 1 / 90, 1 / 30, 2.5 / 30, 1 / 7, 2 / 7, 3.5 / 7, 5.5 / 7, 1])
_STD_FOOD_PORT = np.array([1, 2, 3, 4])
_STD_PORT_SERV = np.array([0.25, 0.5, 1, 2])


def _foodfreq(actual):
    return np.array([_STD_FREQ_SERV[_STD_FOOD_FREQ == a][0] if a in _STD_FOOD_FREQ else 0 for a in actual])


def _foodport(actual):
    return np.array([_STD_PORT_SERV[_STD_FOOD_PORT == a][0] if a in _STD_FOOD_PORT else 0 for a in actual])


def _load_block_data(raw_data):
    """Load BLOCK FFQ data from file path, BytesIO, or DataFrame."""
    import os
    from io import BytesIO

    if isinstance(raw_data, pd.DataFrame):
        return raw_data.copy()
    elif isinstance(raw_data, (str, os.PathLike)):
        fname_lower = str(raw_data).lower()
        if fname_lower.endswith(".csv"):
            return pd.read_csv(raw_data)
        elif fname_lower.endswith((".xlsx", ".xls")):
            return pd.read_excel(raw_data)
        else:
            raise ValueError(f"不支持的文件格式: {raw_data}")
    elif isinstance(raw_data, BytesIO):
        raw_data.seek(0)
        try:
            return pd.read_csv(raw_data)
        except Exception:
            raw_data.seek(0)
            return pd.read_excel(raw_data)
    else:
        raise ValueError(f"不支持的文件类型: {type(raw_data)}")


def _get_block_value(df, col_names):
    """Get column values from DataFrame, trying multiple column name variants."""
    for name in col_names:
        if name in df.columns:
            return pd.to_numeric(df[name], errors="coerce").fillna(0).values
    return np.zeros(len(df))


def _get_block_id(df):
    """Get respondent ID from BLOCK data."""
    for candidate in ["RESPONDENTID", "RespondentID", "respondent_id",
                       "ID", "id", "SUBJECTID", "SUBJECT_ID"]:
        if candidate in df.columns:
            return df[candidate].values
    return np.arange(1, len(df) + 1)


def compute_ahei_block(raw_data):
    """
    一步式计算 BLOCK FFQ 数据的 AHEI

    精确翻译自 R 包 AHEI_BLOCK.R 源码。
    基于 FREQ/QUAN 频率和份量转换，计算 AHEI 总分和组分分数。
    """
    df = _load_block_data(raw_data)

    respondent_id = _get_block_id(df)
    gender = _get_block_value(df, ["SEX", "GENDER", "Gender", "sex", "gender"])

    # Standard frequency/portion conversion for special items
    freq_straw = pd.to_numeric(df.get("STRAWBERRIESFREQ", pd.Series(0, index=df.index)), errors="coerce").fillna(0).values
    quan_straw = pd.to_numeric(df.get("STRAWBERRIESQUAN", pd.Series(0, index=df.index)), errors="coerce").fillna(0).values

    f_berries = _foodfreq(freq_straw) * _foodport(quan_straw)

    # Build AHEI serving size components exactly as in R
    veg_serv = (
        _get_block_value(df, ["V_DRKGR", "V_DRKGR_VEG"])
        + (_get_block_value(df, ["V_DPYEL", "V_DPYEL_VEG"])
           + _get_block_value(df, ["V_OTHER", "V_OTHER_VEG"])
           + _get_block_value(df, ["V_STARCY", "V_STARCY_VEG"])
           + _get_block_value(df, ["V_TOMATO", "V_TOMATO_VEG"])) / 0.5
    )

    f_solid = _get_block_value(df, ["F_SOLID", "F_SOLID_FRT"])
    f_whole = f_solid - f_berries + f_berries * 2
    frt_serv = f_whole

    wgrain_serv = _get_block_value(df, ["G_WHL", "G_WHL_GRAIN"]) / 0.035274

    nutsleg_serv = (
        _get_block_value(df, ["LEGUMES", "LEGUMES_VEG"]) * 4
        + _get_block_value(df, ["M_NUTSD", "M_NUTSD_MEAT"])
        + _get_block_value(df, ["M_SOY", "M_SOY_MEAT"])
    )

    kcal = _get_block_value(df, ["DT_KCAL", "TOTALKCAL", "KCAL", "TOTAL_KCAL"])
    kcal_safe = np.where(kcal > 0, kcal, 2000.0)

    n6 = _get_block_value(df, ["DT_TOTN6", "DT_N6"])
    n3_total = _get_block_value(df, ["DT_TOTN3", "DT_N3"])
    fa205 = _get_block_value(df, ["DT_FA205", "DT_EPA"])
    fa226 = _get_block_value(df, ["DT_FA226", "DT_DHA"])
    pufa_serv = (((n6 + n3_total - fa205 - fa226) * 9) / kcal_safe) * 100

    n3fat_serv = (fa205 + fa226) * 1000

    ssb_grams = _get_block_value(df, ["GROUP_SUGARYBEVG_TOTAL_GRAMS", "SSB_GRAMS"])
    f_juice = _get_block_value(df, ["F_JUICE", "F_JUICE_FRT"])
    ssb_frtj_serv = (ssb_grams / 240) + f_juice

    redproc_meat_serv = (
        _get_block_value(df, ["M_FRANK", "M_FRANK_MEAT"]) / 1.5
        + (_get_block_value(df, ["M_MEAT", "M_MEAT_MEAT"])
           + _get_block_value(df, ["M_ORGAN", "M_ORGAN_MEAT"])) / 4
    )

    trans_fat = _get_block_value(df, ["DT_TRFAT", "TRANSFAT", "DT_TRANS"])
    trans_serv = ((trans_fat * 9) / kcal_safe) * 100

    sodium = _get_block_value(df, ["DT_SODI", "SODIUM", "DT_SODIUM"])
    sodium_serv = sodium / (kcal_safe / 2000)

    alcohol_serv = _get_block_value(df, ["A_BEV", "ALCOHOL", "DT_ALCO"])

    result = compute_ahei(
        data=df,
        respondent_id=respondent_id,
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


def compute_aheip_block(raw_data):
    """
    一步式计算 BLOCK FFQ 数据的 AHEIP (孕期替代健康饮食指数)

    精确翻译自 R 包 AHEIP_BLOCK.R 源码。
    """
    df = _load_block_data(raw_data)

    respondent_id = _get_block_id(df)

    # Special items
    freq_tofu = pd.to_numeric(df.get("TOFUFREQ", pd.Series(0, index=df.index)), errors="coerce").fillna(0).values
    quan_tofu = pd.to_numeric(df.get("TOFUQUAN", pd.Series(0, index=df.index)), errors="coerce").fillna(0).values
    tofu = _foodfreq(freq_tofu) * _foodport(quan_tofu)

    freq_straw = pd.to_numeric(df.get("STRAWBERRIESFREQ", pd.Series(0, index=df.index)), errors="coerce").fillna(0).values
    quan_straw = pd.to_numeric(df.get("STRAWBERRIESQUAN", pd.Series(0, index=df.index)), errors="coerce").fillna(0).values
    f_berries = _foodfreq(freq_straw) * _foodport(quan_straw)

    veg_serv = (
        _get_block_value(df, ["V_DRKGR", "V_DRKGR_VEG"])
        + (_get_block_value(df, ["V_DPYEL", "V_DPYEL_VEG"])
           + _get_block_value(df, ["V_OTHER", "V_OTHER_VEG"])
           + _get_block_value(df, ["V_STARCY", "V_STARCY_VEG"])
           + _get_block_value(df, ["V_TOMATO", "V_TOMATO_VEG"])
           + tofu) / 0.5
    )

    f_solid = _get_block_value(df, ["F_SOLID", "F_SOLID_FRT"])
    f_whole = f_solid - f_berries + f_berries * 2
    frt_serv = f_whole

    white_meat = (_get_block_value(df, ["M_POULT", "M_POULT_MEAT"])
                  + _get_block_value(df, ["M_FISH_HI", "M_FISH_HI_MEAT"])
                  + _get_block_value(df, ["M_FISH_LO", "M_FISH_LO_MEAT"])) / 4
    red_meat = (
        _get_block_value(df, ["M_FRANK", "M_FRANK_MEAT"]) / 1.5
        + (_get_block_value(df, ["M_MEAT", "M_MEAT_MEAT"])
           + _get_block_value(df, ["M_ORGAN", "M_ORGAN_MEAT"])) / 4
    )
    red_meat_safe = np.where(red_meat > 0, red_meat, 1e-10)
    whitered_rt_serv = white_meat / red_meat_safe

    fiber_serv = _get_block_value(df, ["DT_FIBE", "FIBER", "DT_FIBER"])

    kcal = _get_block_value(df, ["DT_KCAL", "TOTALKCAL", "KCAL"])
    kcal_safe = np.where(kcal > 0, kcal, 2000.0)

    trans_fat = _get_block_value(df, ["DT_TRFAT", "TRANSFAT", "DT_TRANS"])
    trans_serv = ((trans_fat * 9) / kcal_safe) * 100

    polyfat = _get_block_value(df, ["DT_PFAT", "POLYFAT", "DT_POLY"])
    satfat = _get_block_value(df, ["DT_SFAT", "SATFAT", "DT_SAT"])
    satfat_safe = np.where(satfat > 0, satfat, 1e-10)
    polysat_rt = polyfat / satfat_safe

    calcium_serv = _get_block_value(df, ["DT_CALC", "CALCIUM", "DT_CALCIUM"])
    folate_serv = _get_block_value(df, ["DT_FOLFD", "FOLATE", "DT_FOLATE"])
    iron_serv = _get_block_value(df, ["DT_IRON", "IRON", "DT_IRON"])

    result = compute_aheip(
        data=df,
        respondent_id=respondent_id,
        vegetable=veg_serv,
        fruit=frt_serv,
        white_red_ratio=whitered_rt_serv,
        fiber=fiber_serv,
        trans_fat=trans_serv,
        poly_sat_ratio=polysat_rt,
        calcium=calcium_serv,
        folate=folate_serv,
        iron=iron_serv,
    )
    return result
