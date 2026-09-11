"""NHANES FPED iff-level adapters for indices requiring individual food items.

These adapters are aligned to the corresponding dietaryindex R package entry
points and mirror the R-side preprocessing formulas before calling the Python
core scoring functions.
"""

import numpy as np
import pandas as pd

from dietaryindex.core.dash import compute_dash
from dietaryindex.core.di_gm import compute_di_gm
from dietaryindex.core.medi import compute_medi, compute_medi_v2
from dietaryindex.core._scoring import score_healthy, score_unhealthy, score_decile_sodium


def _unique_preserve_order(values):
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(int(value))
    return result


def _package_data_path(filename):
    from pathlib import Path

    return Path(__file__).resolve().parents[1] / "data" / filename


def _load_package_numeric_csv(filename, fallback):
    path = _package_data_path(filename)
    if not path.exists():
        return fallback

    data = pd.read_csv(path)
    if "code" not in data.columns:
        return fallback
    values = pd.to_numeric(data["code"], errors="coerce").dropna().astype(int).tolist()
    return _unique_preserve_order(values) if values else fallback


# AHEI R uses data("SSB_FNDDS_1718"); vendor the extracted codes from that
# dataset so the Python default matches the R package exactly.
_SSB_CODES_DEFAULT = _load_package_numeric_csv(
    "ssb_fndds_1718_codes.csv",
    [
        92410310, 92410320, 92410330, 92410340, 92410350, 92410360, 92410370,
        92410390, 92410410, 92410420, 92410430, 92410450, 92410460, 92410500,
        92410510, 92410520, 92410550, 92410560, 92410590, 92410610, 92410620,
        92410710, 92410720, 92410810, 92410820, 92410830, 92411000, 92411210,
        92411410, 92411510, 92411610, 92510120, 92510210, 92510220, 92510230,
        92510240, 92510250, 92510260, 92510270, 92510280, 92510310, 92510320,
        92510410, 92510510, 92510610, 92510620, 92510810, 92510910, 92511010,
        92530110, 92530210, 92530310, 92530410, 92530510, 92530610, 92530620,
        92530710, 92531010, 92531110, 92531610, 92531810, 92532010, 92540210,
        92541010, 92541110, 92550810, 92550910, 92560210, 92560310, 92560410,
        92560610, 92560810, 92561110, 92561210, 92561310, 92561410, 92561510,
        92561610, 92561710, 92561810, 92561910, 92562010, 92562210, 92562310,
        92562410, 92562510, 92562610, 92570110, 92570510, 92570710, 92570910,
        92571010, 92571210, 92571310, 92571710, 92571910, 92572510, 92572610,
    ],
)

_DASH_SSB_CODES_DEFAULT = _load_package_numeric_csv(
    "dash_ssb_fndds_1718_codes.csv", _SSB_CODES_DEFAULT
)
_MEDI_SSB_CODES_DEFAULT = _load_package_numeric_csv(
    "medi_ssb_fndds_1718_codes.csv", _SSB_CODES_DEFAULT
)

_SKIM_MILK_CODES_DEFAULT = _load_package_numeric_csv(
    "dash_skim_milk_fndds_1718_codes.csv",
    [11111170, 11113000, 11114320, 11115000, 11120000, 11121300, 11212050],
)
_LOWF_CHEESE_CODES_DEFAULT = _load_package_numeric_csv(
    "dash_lowf_cheese_fndds_1718_codes.csv",
    [14204010, 14204020, 14206010, 14207010],
)
_SWEETS_CODES_DEFAULT = _load_package_numeric_csv(
    "medi_sweets_fndds_1718_codes.csv", [53100100]
)
_FAT_OIL_CODES_DEFAULT = _load_package_numeric_csv(
    "medi_fat_oil_fndds_1718_codes.csv", [82104000]
)
_OLIVE_OIL_CODES_DEFAULT = _load_package_numeric_csv(
    "medi_olive_oil_fndds_1718_codes.csv", [82104000]
)

_AVOCADO_CODES_DEFAULT = _load_package_numeric_csv(
    "di_gm_avocado_fndds_1718_codes.csv", [63105010]
)
_BROCCOLI_CODES_DEFAULT = _load_package_numeric_csv(
    "di_gm_broccoli_fndds_1718_codes.csv",
    [72103000, 72103030, 72201100, 72201190, 72201211, 72201212, 72201220],
)
_CHICKPEA_CODES_DEFAULT = _load_package_numeric_csv(
    "di_gm_chickpea_fndds_1718_codes.csv",
    [41301990, 41302010, 41302020, 41302040, 41302080, 41302110],
)
_COFFEE_CODES_DEFAULT = _load_package_numeric_csv(
    "di_gm_coffee_fndds_1718_codes.csv",
    [92100000, 92100500, 92101000],
)
_CRANBERRY_CODES_DEFAULT = _load_package_numeric_csv(
    "di_gm_cranberry_fndds_1718_codes.csv",
    [62109100, 63207010, 63207110],
)
_FERMENTED_DAIRY_CODES_DEFAULT = _load_package_numeric_csv(
    "di_gm_fermented_dairy_fndds_1718_codes.csv",
    [11400000, 11410000, 14101010],
)
_GREEN_TEA_CODES_DEFAULT = _load_package_numeric_csv(
    "di_gm_green_tea_fndds_1718_codes.csv",
    [92303010, 92303100, 92305900],
)
_SOYBEAN_CODES_DEFAULT = _load_package_numeric_csv(
    "di_gm_soybean_fndds_1718_codes.csv",
    [11320000, 11320100, 11320200, 11321000, 11321100, 11321200, 41107010, 41410010],
)


def _load_iff(uploaded):
    from dietaryindex.adapters.nhanes_fped_other import _resolve_upload

    return _resolve_upload(uploaded)


def _first_existing(df, names, default=0.0):
    for name in names:
        if name in df.columns:
            return df[name]
    return pd.Series(default, index=df.index)


def _num(df, names, default=0.0):
    series = pd.to_numeric(_first_existing(df, names, default), errors="coerce").fillna(default)
    return series.where(series.isna() | (series.abs() >= 1e-12), 0.0)


def _round_numeric_frame(df, decimals=12):
    if df is None or df.empty:
        return df
    result = df.copy()
    numeric_cols = result.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        result[numeric_cols] = result[numeric_cols].round(decimals)
    return result


def _sum_like_r(series):
    return sum(series.tolist())


def _aggregate_by_seqn(summary, *, sum_cols=None, first_cols=None, min_cols=None):
    sum_cols = list(sum_cols or [])
    first_cols = list(first_cols or [])
    min_cols = list(min_cols or [])
    rows = []
    for seqn, group in summary.groupby("SEQN", sort=False):
        row = {"SEQN": int(seqn)}
        for col in sum_cols:
            row[col] = _sum_like_r(group[col])
        for col in first_cols:
            row[col] = group[col].iloc[0]
        for col in min_cols:
            row[col] = group[col].min()
        rows.append(row)
    return pd.DataFrame(rows)


def _prepare_iff_day(fped_input, nutrient_input, day, *, filter_positive_line_kcal=False):
    if fped_input is None or nutrient_input is None:
        return None

    fped = _load_iff(fped_input)
    nutrient = _load_iff(nutrient_input)
    if fped is None or nutrient is None:
        return None

    line_col = f"DR{day}ILINE"
    status_col = f"DR{day}DRSTZ"
    kcal_col = f"DR{day}IKCAL"
    if line_col not in fped.columns or line_col not in nutrient.columns:
        raise ValueError(
            f"Please use individual-level day {day} data. "
            f"Nutrient data should be like DR{day}IFF and FPED data like fped_dr{day}iff."
        )

    nutrient = nutrient.copy()
    fped = fped.copy()

    if status_col in nutrient.columns:
        nutrient = nutrient[nutrient[status_col] == 1].copy()
    if filter_positive_line_kcal and kcal_col in nutrient.columns:
        kcal = pd.to_numeric(nutrient[kcal_col], errors="coerce").fillna(0.0)
        kcal = kcal.where(kcal.abs() >= 1e-12, 0.0)
        nutrient = nutrient[kcal > 0].copy()

    nutrient = nutrient.sort_values("SEQN")
    fped = fped.sort_values("SEQN")

    merged = nutrient.merge(fped, on=["SEQN", line_col], how="left", suffixes=("_NUT", "_FPED"))
    food_code = _num(
        merged,
        [f"DR{day}IFDCD_NUT", f"DR{day}IFDCD_FPED", f"DR{day}IFDCD.x", f"DR{day}IFDCD.y", f"DR{day}IFDCD"],
        default=np.nan,
    )
    grams = _num(
        merged,
        [f"DR{day}IGRMS_NUT", f"DR{day}IGRMS_FPED", f"DR{day}IGRMS.x", f"DR{day}IGRMS.y", f"DR{day}IGRMS"],
        default=0.0,
    )
    merged["_FOOD_CODE"] = food_code
    merged["_GRAMS"] = grams
    return merged


def _merge_demo(result, demo_path):
    if demo_path is None or result.empty:
        return result

    from dietaryindex.adapters.nhanes_fped_other import _resolve_upload

    demo_df = _resolve_upload(demo_path)
    if demo_df is None or "SEQN" not in demo_df.columns:
        return result

    demo_df = demo_df.copy()
    demo_df["SEQN"] = demo_df["SEQN"].astype(int)
    demo_cols = [c for c in demo_df.columns if c not in result.columns and c != "SEQN"]
    if not demo_cols:
        return result
    merged = result.merge(demo_df[["SEQN"] + demo_cols], on="SEQN", how="left")
    # Several scorers need sex before component calculation.  Preserve an
    # existing non-missing GENDER value, but backfill it from the canonical
    # NHANES RIAGENDR field when DEMO is supplied separately.
    if "GENDER" in merged.columns and "RIAGENDR" in merged.columns:
        merged["GENDER"] = pd.to_numeric(merged["GENDER"], errors="coerce").fillna(
            pd.to_numeric(merged["RIAGENDR"], errors="coerce")
        )
    return merged


def _average_day_results(day1, day2, preserve_cols=None):
    if day1 is None or day1.empty:
        return day2
    if day2 is None or day2.empty:
        return day1

    preserve_cols = set(preserve_cols or [])
    merged = day1.merge(day2, on="SEQN", how="inner", suffixes=("_1", "_2"))
    result = pd.DataFrame({"SEQN": merged["SEQN"]})

    for col in preserve_cols:
        c1 = f"{col}_1"
        if c1 in merged.columns:
            result[col] = merged[c1]

    for col in day1.columns:
        if col == "SEQN" or col in preserve_cols:
            continue
        c1 = f"{col}_1"
        c2 = f"{col}_2"
        if c1 in merged.columns and c2 in merged.columns:
            result[col] = (
                pd.to_numeric(merged[c1], errors="coerce")
                + pd.to_numeric(merged[c2], errors="coerce")
            ) / 2.0

    return result


def _summarize_ahei(joined, day, ssb_codes):
    if joined is None or joined.empty:
        return None

    food_code = _num(joined, ["_FOOD_CODE"], default=np.nan)
    energy = _num(joined, [f"DR{day}IKCAL"])
    summary = pd.DataFrame(
        {
            "SEQN": joined["SEQN"].astype(int),
            "GENDER": _num(joined, ["RIAGENDR"], default=np.nan),
            "ENERGY": energy,
            "VEG_SERV": _num(joined, [f"DR{day}I_V_DRKGR"])
            + (
                _num(joined, [f"DR{day}I_V_REDOR_TOTAL"])
                + _num(joined, [f"DR{day}I_V_OTHER"])
                + _num(joined, [f"DR{day}I_V_STARCHY_OTHER"])
            )
            / 0.5,
            "FRT_SERV": _num(joined, [f"DR{day}I_F_TOTAL"]) - _num(joined, [f"DR{day}I_F_JUICE"]),
            "WGRAIN_SERV": _num(joined, [f"DR{day}I_G_WHOLE"]) / 0.035274,
            "NUTSLEG_SERV": _num(joined, [f"DR{day}I_PF_LEGUMES"])
            + _num(joined, [f"DR{day}I_PF_NUTSDS"])
            + _num(joined, [f"DR{day}I_PF_SOY"]),
            "PUFA_G": _num(joined, [f"DR{day}IP182"])
            + _num(joined, [f"DR{day}IP183"])
            + _num(joined, [f"DR{day}IP184"])
            + _num(joined, [f"DR{day}IP204"])
            + _num(joined, [f"DR{day}IP225"]),
            "N3_MG": (_num(joined, [f"DR{day}IP205"]) + _num(joined, [f"DR{day}IP226"])) * 1000.0,
            "SSB_SERV": np.where(
                food_code.isin(ssb_codes),
                _num(joined, [f"DR{day}I_ADD_SUGARS"]) * 4.0 / 26.0,
                0.0,
            ),
            "REDPROC_MEAT_SERV": _num(joined, [f"DR{day}I_PF_CUREDMEAT"]) / 1.5
            + (_num(joined, [f"DR{day}I_PF_MEAT"]) + _num(joined, [f"DR{day}I_PF_ORGAN"])) / 4.0,
            "SODIUM_RAW": _num(joined, [f"DR{day}ISODI"]),
            "ALCOHOL_SERV": _num(joined, [f"DR{day}I_A_DRINKS"]),
        }
    )

    grouped = summary.groupby("SEQN", as_index=False).agg(
        {
            "GENDER": "min",
            "ENERGY": "sum",
            "VEG_SERV": "sum",
            "FRT_SERV": "sum",
            "WGRAIN_SERV": "sum",
            "NUTSLEG_SERV": "sum",
            "PUFA_G": "sum",
            "N3_MG": "sum",
            "SSB_SERV": "sum",
            "REDPROC_MEAT_SERV": "sum",
            "SODIUM_RAW": "sum",
            "ALCOHOL_SERV": "sum",
        }
    )
    grouped = grouped[grouped["ENERGY"] > 0].reset_index(drop=True)
    if grouped.empty:
        return grouped

    grouped["PUFA_SERV"] = np.where(
        grouped["ENERGY"] > 0,
        (grouped["PUFA_G"] * 9.0 / grouped["ENERGY"]) * 100.0,
        np.nan,
    )
    return _round_numeric_frame(grouped)


def _score_ahei_nhanes(summary, day):
    if summary is None or summary.empty:
        return None

    gender = summary["GENDER"].to_numpy(dtype=float)
    veg = summary["VEG_SERV"].to_numpy(dtype=float)
    frt = summary["FRT_SERV"].to_numpy(dtype=float)
    wgrain = summary["WGRAIN_SERV"].to_numpy(dtype=float)
    nutsleg = summary["NUTSLEG_SERV"].to_numpy(dtype=float)
    n3fat = summary["N3_MG"].to_numpy(dtype=float)
    pufa = summary["PUFA_SERV"].to_numpy(dtype=float)
    ssb = summary["SSB_SERV"].to_numpy(dtype=float)
    redproc = summary["REDPROC_MEAT_SERV"].to_numpy(dtype=float)
    sodium_raw = summary["SODIUM_RAW"].to_numpy(dtype=float)
    energy = summary["ENERGY"].to_numpy(dtype=float)
    alcohol = summary["ALCOHOL_SERV"].to_numpy(dtype=float)

    ahei_veg = score_healthy(veg, 0, 5, 0, 10)
    ahei_frt = score_healthy(frt, 0, 4, 0, 10)
    ahei_wgrain = np.where(
        gender == 2,
        score_healthy(wgrain, 0, 75, 0, 10),
        np.where(gender == 1, score_healthy(wgrain, 0, 90, 0, 10), np.nan),
    )
    ahei_nutsleg = score_healthy(nutsleg, 0, 1, 0, 10)
    ahei_n3fat = score_healthy(n3fat, 0, 250, 0, 10)
    ahei_pufa = score_healthy(pufa, 2, 10, 0, 10)
    ahei_ssb = score_unhealthy(ssb, 1, 0, 0, 10)
    ahei_redproc = score_unhealthy(redproc, 1.5, 0, 0, 10)

    sodium_serv = np.where(energy > 0, sodium_raw / (energy / 2000.0), np.nan)
    ahei_sodium = score_decile_sodium(sodium_serv)

    if day == 1:
        cond_f = [
            (gender == 2) & (alcohol >= 2.5),
            (gender == 2) & (alcohol < 2.5) & (alcohol > 1.5),
            (gender == 2) & (alcohol <= 1.5) & (alcohol >= 0.5),
            (gender == 2) & (alcohol < 0.5) & (alcohol > 0.125),
            (gender == 2) & (alcohol <= 0.125),
        ]
        cond_m = [
            (gender == 1) & (alcohol >= 3.5),
            (gender == 1) & (alcohol < 3.5) & (alcohol > 2.0),
            (gender == 1) & (alcohol <= 2.0) & (alcohol >= 0.5),
            (gender == 1) & (alcohol < 0.5) & (alcohol > 0.125),
            (gender == 1) & (alcohol <= 0.125),
        ]
    else:
        # Match the exact day-2 branch in the R adapter, including its ordering.
        cond_f = [
            (gender == 2) & (alcohol >= 2.5),
            (gender == 2) & (alcohol < 2.5) & (alcohol > 1.5),
            (gender == 2) & (alcohol <= 1.5) & (alcohol >= 0.5),
            (gender == 2) & (alcohol < 0.5),
            (gender == 2) & (alcohol <= 0.125),
        ]
        cond_m = [
            (gender == 1) & (alcohol >= 3.5),
            (gender == 1) & (alcohol < 3.5) & (alcohol > 2.0),
            (gender == 1) & (alcohol <= 2.0) & (alcohol >= 0.5),
            (gender == 1) & (alcohol < 0.5),
            (gender == 1) & (alcohol <= 0.125),
        ]

    choice_f = [
        0.0,
        0.0 + (alcohol - 2.5) * 10.0 / (1.5 - 2.5),
        10.0,
        0.0 + (alcohol - 0.0) * 10.0 / (0.5 - 0.0),
        2.5,
    ]
    choice_m = [
        0.0,
        0.0 + (alcohol - 3.5) * 10.0 / (2.0 - 3.5),
        10.0,
        0.0 + (alcohol - 0.0) * 10.0 / (0.5 - 0.0),
        2.5,
    ]
    ahei_alcohol = np.select(cond_f + cond_m, choice_f + choice_m, default=np.nan)

    ahei_all = (
        ahei_veg
        + ahei_frt
        + ahei_wgrain
        + ahei_nutsleg
        + ahei_n3fat
        + ahei_pufa
        + ahei_ssb
        + ahei_redproc
        + ahei_sodium
        + ahei_alcohol
    )
    ahei_noetoh = (
        ahei_veg
        + ahei_frt
        + ahei_wgrain
        + ahei_nutsleg
        + ahei_n3fat
        + ahei_pufa
        + ahei_ssb
        + ahei_redproc
        + ahei_sodium
    )

    return pd.DataFrame(
        {
            "SEQN": summary["SEQN"].values,
            "RESPONDENTID": summary["SEQN"].values,
            "GENDER": gender,
            "AHEI_ALL": ahei_all,
            "AHEI_NOETOH": ahei_noetoh,
            "AHEI_VEG": ahei_veg,
            "AHEI_FRT": ahei_frt,
            "AHEI_WGRAIN": ahei_wgrain,
            "AHEI_NUTSLEG": ahei_nutsleg,
            "AHEI_N3FAT": ahei_n3fat,
            "AHEI_PUFA": ahei_pufa,
            "AHEI_SSB_FRTJ": ahei_ssb,
            "AHEI_REDPROC_MEAT": ahei_redproc,
            "AHEI_TRANS": np.full(len(summary), np.nan),
            "AHEI_SODIUM": ahei_sodium,
            "AHEI_ALCOHOL": ahei_alcohol,
        }
    )


def _score_quintile_healthy_nhanes(actual):
    actual = np.asarray(actual, dtype=float)
    values = np.sort(actual[~np.isnan(actual)])
    quintiles = np.empty(6, dtype=float)
    # Use explicit decimal literals to match R's seq(0, 1, by = 0.2) boundaries.
    for i, p in enumerate((0.0, 0.2, 0.4, 0.6, 0.8, 1.0)):
        if p <= 0:
            quintiles[i] = values[0]
            continue
        if p >= 1:
            quintiles[i] = values[-1]
            continue
        h = (len(values) - 1) * p + 1
        j = int(np.floor(h))
        gamma = h - j
        xj = values[j - 1]
        xjp1 = values[j] if j < len(values) else values[-1]
        quintiles[i] = (1.0 - gamma) * xj + gamma * xjp1
    conditions = [
        ((actual >= quintiles[0]) & (actual < quintiles[1])) | (actual == 0),
        (actual >= quintiles[1]) & (actual < quintiles[2]) & (actual != 0),
        (actual >= quintiles[2]) & (actual < quintiles[3]) & (actual != 0),
        (actual >= quintiles[3]) & (actual < quintiles[4]) & (actual != 0),
        (actual >= quintiles[4]) & (actual <= quintiles[5]) & (actual != 0),
    ]
    return np.select(conditions, [1.0, 2.0, 3.0, 4.0, 5.0], default=np.nan)


def _score_quintile_unhealthy_nhanes(actual):
    actual = np.asarray(actual, dtype=float)
    values = np.sort(actual[~np.isnan(actual)])
    quintiles = np.empty(6, dtype=float)
    # Use explicit decimal literals to match R's seq(0, 1, by = 0.2) boundaries.
    for i, p in enumerate((0.0, 0.2, 0.4, 0.6, 0.8, 1.0)):
        if p <= 0:
            quintiles[i] = values[0]
            continue
        if p >= 1:
            quintiles[i] = values[-1]
            continue
        h = (len(values) - 1) * p + 1
        j = int(np.floor(h))
        gamma = h - j
        xj = values[j - 1]
        xjp1 = values[j] if j < len(values) else values[-1]
        quintiles[i] = (1.0 - gamma) * xj + gamma * xjp1
    conditions = [
        ((actual >= quintiles[0]) & (actual < quintiles[1])) | (actual == 0),
        (actual >= quintiles[1]) & (actual < quintiles[2]) & (actual != 0),
        (actual >= quintiles[2]) & (actual < quintiles[3]) & (actual != 0),
        (actual >= quintiles[3]) & (actual < quintiles[4]) & (actual != 0),
        (actual >= quintiles[4]) & (actual <= quintiles[5]) & (actual != 0),
    ]
    return np.select(conditions, [5.0, 4.0, 3.0, 2.0, 1.0], default=np.nan)


def _score_dash_nhanes(summary):
    if summary is None or summary.empty:
        return None

    fruit = summary["FRT_FRTJ_SERV"].to_numpy(dtype=float)
    veg = summary["VEG_SERV"].to_numpy(dtype=float)
    nutsleg = summary["NUTSLEG_SERV"].to_numpy(dtype=float)
    wgrain = summary["WGRAIN_SERV"].to_numpy(dtype=float)
    lowf_dairy = summary["LOWF_DAIRY_SERV"].to_numpy(dtype=float)
    energy = summary["ENERGY"].to_numpy(dtype=float)
    sodium_raw = summary["SODIUM_RAW"].to_numpy(dtype=float)
    redproc = summary["REDPROC_MEAT_SERV"].to_numpy(dtype=float)
    ssb_frtj = summary["SSB_FRTJ_SERV"].to_numpy(dtype=float)

    sodium = np.where(energy > 0, sodium_raw / (energy / 2000.0), np.nan)
    dash_frt = _score_quintile_healthy_nhanes(fruit)
    dash_veg = _score_quintile_healthy_nhanes(veg)
    dash_nutsleg = _score_quintile_healthy_nhanes(nutsleg)
    dash_wgrain = _score_quintile_healthy_nhanes(wgrain)
    dash_lowf_dairy = _score_quintile_healthy_nhanes(lowf_dairy)
    dash_sodium = _score_quintile_unhealthy_nhanes(sodium)
    dash_redproc = _score_quintile_unhealthy_nhanes(redproc)
    dash_ssb_frtj = _score_quintile_unhealthy_nhanes(ssb_frtj)
    dash_all = (
        dash_frt
        + dash_veg
        + dash_nutsleg
        + dash_wgrain
        + dash_lowf_dairy
        + dash_sodium
        + dash_redproc
        + dash_ssb_frtj
    )
    return pd.DataFrame(
        {
            "RESPONDENTID": summary["SEQN"].values,
            "DASH_ALL": dash_all,
            "DASH_FRT": dash_frt,
            "DASH_VEG": dash_veg,
            "DASH_NUTSLEG": dash_nutsleg,
            "DASH_WGRAIN": dash_wgrain,
            "DASH_LOWF_DAIRY": dash_lowf_dairy,
            "DASH_SODIUM": dash_sodium,
            "DASH_REDPROC_MEAT": dash_redproc,
            "DASH_SSB_FRTJ": dash_ssb_frtj,
        }
    )


def _summarize_dash(joined, day, ssb_codes, skim_codes, cheese_codes):
    if joined is None or joined.empty:
        return None

    food_code = _num(joined, ["_FOOD_CODE"], default=np.nan)
    summary = pd.DataFrame(
        {
            "SEQN": joined["SEQN"].astype(int),
            "ENERGY": _num(joined, [f"DR{day}IKCAL"]),
            "FRT_FRTJ_SERV": _num(joined, [f"DR{day}I_F_TOTAL"]),
            "VEG_SERV": _num(joined, [f"DR{day}I_V_DRKGR"])
            + (
                _num(joined, [f"DR{day}I_V_REDOR_TOTAL"])
                + _num(joined, [f"DR{day}I_V_OTHER"])
                + _num(joined, [f"DR{day}I_V_STARCHY_OTHER"])
            )
            / 0.5,
            "NUTSLEG_SERV": _num(joined, [f"DR{day}I_PF_LEGUMES"])
            + _num(joined, [f"DR{day}I_PF_NUTSDS"])
            + _num(joined, [f"DR{day}I_PF_SOY"]),
            "WGRAIN_SERV": _num(joined, [f"DR{day}I_G_WHOLE"]),
            "LOWF_DAIRY_SERV": np.where(
                food_code.isin(skim_codes),
                _num(joined, [f"DR{day}I_D_MILK"]),
                0.0,
            )
            + np.where(
                food_code.isin(cheese_codes),
                _num(joined, [f"DR{day}I_D_CHEESE"]) * 4.0,
                0.0,
            )
            + _num(joined, [f"DR{day}I_D_YOGURT"]),
            "SODIUM_RAW": _num(joined, [f"DR{day}ISODI"]),
            "REDPROC_MEAT_SERV": _num(joined, [f"DR{day}I_PF_CUREDMEAT"]) / 1.5
            + (_num(joined, [f"DR{day}I_PF_MEAT"]) + _num(joined, [f"DR{day}I_PF_ORGAN"])) / 4.0,
            "SSB_FRTJ_SERV": np.where(
                food_code.isin(ssb_codes),
                _num(joined, [f"DR{day}I_ADD_SUGARS"]) * 4.0 / 26.0,
                0.0,
            ),
        }
    )

    grouped = _aggregate_by_seqn(
        summary,
        sum_cols=[
            "ENERGY",
            "FRT_FRTJ_SERV",
            "VEG_SERV",
            "NUTSLEG_SERV",
            "WGRAIN_SERV",
            "LOWF_DAIRY_SERV",
            "SODIUM_RAW",
            "REDPROC_MEAT_SERV",
            "SSB_FRTJ_SERV",
        ],
    )
    grouped = grouped[grouped["ENERGY"] > 0].reset_index(drop=True)
    return grouped


def _summarize_medi(joined, day, ssb_codes, sweets_codes, fat_oil_codes, olive_oil_codes):
    if joined is None or joined.empty:
        return None

    food_code = _num(joined, ["_FOOD_CODE"], default=np.nan)
    grams = _num(joined, ["_GRAMS"])
    summary = pd.DataFrame(
        {
            "SEQN": joined["SEQN"].astype(int),
            "OLIVE_OIL_SERV_MEDI": np.where(food_code.isin(olive_oil_codes), grams / 10.0, 0.0),
            "FRT_SERV_MEDI": _num(joined, [f"DR{day}I_F_CITMLB"]) + _num(joined, [f"DR{day}I_F_OTHER"]),
            "VEG_SERV_MEDI": _num(joined, [f"DR{day}I_V_DRKGR"]) / 2.0
            + _num(joined, [f"DR{day}I_V_REDOR_TOTAL"])
            + _num(joined, [f"DR{day}I_V_OTHER"])
            + _num(joined, [f"DR{day}I_V_STARCHY_OTHER"]),
            "LEGUMES_SERV_MEDI": (_num(joined, [f"DR{day}I_V_LEGUMES"]) * 4.0 + _num(joined, [f"DR{day}I_PF_SOY"])) / 1.5,
            "NUTS_SERV_MEDI": _num(joined, [f"DR{day}I_PF_NUTSDS"]),
            "FISH_SEAFOOD_SERV_MEDI": (_num(joined, [f"DR{day}I_PF_SEAFD_HI"]) + _num(joined, [f"DR{day}I_PF_SEAFD_LOW"])) / 4.0,
            "ALCOHOL_SERV_MEDI": _num(joined, [f"DR{day}I_A_DRINKS"]),
            "SSB_SERV_MEDI": np.where(food_code.isin(ssb_codes), _num(joined, [f"DR{day}I_ADD_SUGARS"]) * 4.0 / 26.0, 0.0),
            "SWEETS_SERV_MEDI": np.where(food_code.isin(sweets_codes), grams / 50.0, 0.0),
            "DISCRET_FAT_SERV_MEDI": np.where(food_code.isin(fat_oil_codes), grams / 10.0, 0.0),
            "REDPROC_MEAT_SERV_MEDI": (
                _num(joined, [f"DR{day}I_PF_CUREDMEAT"])
                + _num(joined, [f"DR{day}I_PF_MEAT"])
                + _num(joined, [f"DR{day}I_PF_ORGAN"])
            )
            / 5.0,
        }
    )
    return summary.groupby("SEQN", as_index=False).sum()


def _summarize_di_gm(joined, day, code_map):
    if joined is None or joined.empty:
        return None

    food_code = _num(joined, ["_FOOD_CODE"], default=np.nan)
    grams = _num(joined, ["_GRAMS"])
    summary = pd.DataFrame(
        {
            "SEQN": joined["SEQN"].astype(int),
            "GENDER": _num(joined, ["RIAGENDR"], default=np.nan),
            "AVOCADO": np.where(food_code.isin(code_map["AVOCADO"]), grams, 0.0),
            "BROCCOLI": np.where(food_code.isin(code_map["BROCCOLI"]), grams, 0.0),
            "CHICKPEA": np.where(food_code.isin(code_map["CHICKPEA"]), grams, 0.0),
            "COFFEE": np.where(food_code.isin(code_map["COFFEE"]), grams, 0.0),
            "CRANBERRY": np.where(food_code.isin(code_map["CRANBERRY"]), grams, 0.0),
            "FERMENTED_DAIRY": np.where(food_code.isin(code_map["FERMENTED_DAIRY"]), grams, 0.0),
            "FIBER": _num(joined, [f"DR{day}IFIBE"]),
            "GREEN_TEA": np.where(food_code.isin(code_map["GREEN_TEA"]), grams, 0.0),
            "SOYBEAN": np.where(food_code.isin(code_map["SOYBEAN"]), grams, 0.0),
            "WHOLE_GRAIN": _num(joined, [f"DR{day}I_G_WHOLE"]),
            "ENERGY": _num(joined, [f"DR{day}IKCAL"]),
            "TOTAL_FAT": _num(joined, [f"DR{day}ITFAT"]),
            "TOTAL_FAT_PCT": np.where(
                _num(joined, [f"DR{day}IKCAL"]) > 0,
                (_num(joined, [f"DR{day}ITFAT"]) * 9.0 / _num(joined, [f"DR{day}IKCAL"])) * 100.0,
                0.0,
            ),
            "PROCESSED_MEAT": _num(joined, [f"DR{day}I_PF_CUREDMEAT"]),
            "RED_MEAT": _num(joined, [f"DR{day}I_PF_MEAT"]),
            "REFINED_GRAIN": _num(joined, [f"DR{day}I_G_REFINED"]),
        }
    )

    return _aggregate_by_seqn(
        summary,
        sum_cols=[
            "AVOCADO",
            "BROCCOLI",
            "CHICKPEA",
            "COFFEE",
            "CRANBERRY",
            "FERMENTED_DAIRY",
            "FIBER",
            "GREEN_TEA",
            "SOYBEAN",
            "WHOLE_GRAIN",
            "ENERGY",
            "TOTAL_FAT",
            "TOTAL_FAT_PCT",
            "PROCESSED_MEAT",
            "RED_MEAT",
            "REFINED_GRAIN",
        ],
        first_cols=["GENDER"],
    )


def _score_di_gm_nhanes(summary):
    if summary is None or summary.empty:
        return None

    rid = summary["SEQN"].to_numpy(dtype=float)
    gender = summary["GENDER"].to_numpy(dtype=float)
    is_female = gender == 2
    is_male = gender == 1
    n = len(summary)

    healthy = {
        "AVOCADO": summary["AVOCADO"].to_numpy(dtype=float),
        "BROCCOLI": summary["BROCCOLI"].to_numpy(dtype=float),
        "CHICKPEA": summary["CHICKPEA"].to_numpy(dtype=float),
        "COFFEE": summary["COFFEE"].to_numpy(dtype=float),
        "CRANBERRY": summary["CRANBERRY"].to_numpy(dtype=float),
        "FERMENTED_DAIRY": summary["FERMENTED_DAIRY"].to_numpy(dtype=float),
        "FIBER": summary["FIBER"].to_numpy(dtype=float),
        "GREEN_TEA": summary["GREEN_TEA"].to_numpy(dtype=float),
        "SOYBEAN": summary["SOYBEAN"].to_numpy(dtype=float),
        "WHOLE_GRAIN": summary["WHOLE_GRAIN"].to_numpy(dtype=float),
    }
    unhealthy = {
        "PROCESSED_MEAT": summary["PROCESSED_MEAT"].to_numpy(dtype=float),
        "RED_MEAT": summary["RED_MEAT"].to_numpy(dtype=float),
        "REFINED_GRAIN": summary["REFINED_GRAIN"].to_numpy(dtype=float),
    }
    total_fat_pct = summary["TOTAL_FAT_PCT"].to_numpy(dtype=float)

    scores = {}
    for name, values in healthy.items():
        s = np.full(n, np.nan)
        for mask in [is_female, is_male]:
            if not mask.any():
                continue
            g_vals = values[mask]
            med = np.nextafter(np.nanmedian(g_vals), np.inf)
            s[mask] = np.where(np.isnan(g_vals), np.nan, np.where((g_vals < med) | (g_vals == 0), 0.0, 1.0))
        scores[f"DI_GM_{name}"] = s

    for name, values in unhealthy.items():
        s = np.full(n, np.nan)
        for mask in [is_female, is_male]:
            if not mask.any():
                continue
            g_vals = values[mask]
            med = np.nextafter(np.nanmedian(g_vals), np.inf)
            s[mask] = np.where(np.isnan(g_vals), np.nan, np.where((g_vals < med) | (g_vals == 0), 1.0, 0.0))
        scores[f"DI_GM_{name}"] = s

    tfat_score = np.where(np.isnan(total_fat_pct), np.nan, np.where(total_fat_pct >= 40, 0.0, 1.0))
    total = tfat_score
    for values in scores.values():
        total = total + values

    return pd.DataFrame(
        {
            "RESPONDENTID": rid,
            "GENDER": gender,
            "DI_GM_TOTAL": total,
            "DI_GM_AVOCADO": scores["DI_GM_AVOCADO"],
            "DI_GM_BROCCOLI": scores["DI_GM_BROCCOLI"],
            "DI_GM_CHICKPEA": scores["DI_GM_CHICKPEA"],
            "DI_GM_COFFEE": scores["DI_GM_COFFEE"],
            "DI_GM_CRANBERRY": scores["DI_GM_CRANBERRY"],
            "DI_GM_FERMENTED_DAIRY": scores["DI_GM_FERMENTED_DAIRY"],
            "DI_GM_FIBER": scores["DI_GM_FIBER"],
            "DI_GM_GREEN_TEA": scores["DI_GM_GREEN_TEA"],
            "DI_GM_SOYBEAN": scores["DI_GM_SOYBEAN"],
            "DI_GM_WHOLE_GRAIN": scores["DI_GM_WHOLE_GRAIN"],
            "DI_GM_TOTAL_FAT_PERCENTAGE": tfat_score,
            "DI_GM_PROCESSED_MEAT": scores["DI_GM_PROCESSED_MEAT"],
            "DI_GM_RED_MEAT": scores["DI_GM_RED_MEAT"],
            "DI_GM_REFINED_GRAIN": scores["DI_GM_REFINED_GRAIN"],
        }
    )


def compute_dash_nhanes_fped(
    fped_ind_path=None,
    nutrient_ind_path=None,
    fped_ind_path2=None,
    nutrient_ind_path2=None,
    skim_milk_code=None,
    lowf_cheese_code=None,
    ssb_code=None,
    demo_path=None,
):
    if skim_milk_code is None:
        skim_milk_code = _SKIM_MILK_CODES_DEFAULT
    if lowf_cheese_code is None:
        lowf_cheese_code = _LOWF_CHEESE_CODES_DEFAULT
    if ssb_code is None:
        ssb_code = _DASH_SSB_CODES_DEFAULT

    def _compute_day(day, fped_path, nutrient_path):
        joined = _prepare_iff_day(fped_path, nutrient_path, day, filter_positive_line_kcal=False)
        summary = _summarize_dash(joined, day, ssb_code, skim_milk_code, lowf_cheese_code)
        if summary is None or summary.empty:
            return None
        result = compute_dash(
            data=summary,
            respondent_id=summary["SEQN"].values,
            total_kcal=summary["ENERGY"].values,
            fruit_fruit_juice=summary["FRT_FRTJ_SERV"].values,
            vegetable=summary["VEG_SERV"].values,
            nut_legume=summary["NUTSLEG_SERV"].values,
            whole_grain=summary["WGRAIN_SERV"].values,
            low_fat_dairy=summary["LOWF_DAIRY_SERV"].values,
            sodium=summary["SODIUM_RAW"].values,
            red_processed_meat=summary["REDPROC_MEAT_SERV"].values,
            ssb_fruit_juice=summary["SSB_FRTJ_SERV"].values,
        )
        result["DASH_REDPROC_MEAT"] = _score_quintile_unhealthy_nhanes(summary["REDPROC_MEAT_SERV"].values)
        result["DASH_ALL"] = (
            result["DASH_FRT"]
            + result["DASH_VEG"]
            + result["DASH_NUTSLEG"]
            + result["DASH_WGRAIN"]
            + result["DASH_LOWF_DAIRY"]
            + result["DASH_SODIUM"]
            + result["DASH_REDPROC_MEAT"]
            + result["DASH_SSB_FRTJ"]
        )
        result["SEQN"] = summary["SEQN"].values
        result["RESPONDENTID"] = summary["SEQN"].values
        return result

    day1 = _compute_day(1, fped_ind_path, nutrient_ind_path)
    day2 = _compute_day(2, fped_ind_path2, nutrient_ind_path2)
    result = _average_day_results(day1, day2, preserve_cols=["RESPONDENTID"])
    return _merge_demo(result, demo_path)


def compute_ahei_nhanes_fped(
    fped_ind_path=None,
    nutrient_ind_path=None,
    fped_ind_path2=None,
    nutrient_ind_path2=None,
    ssb_code=None,
    demo_path=None,
):
    if ssb_code is None:
        ssb_code = _SSB_CODES_DEFAULT

    def _compute_day(day, fped_path, nutrient_path):
        joined = _prepare_iff_day(fped_path, nutrient_path, day, filter_positive_line_kcal=False)
        summary = _summarize_ahei(joined, day, ssb_code)
        if summary is None or summary.empty:
            return None
        summary = _merge_demo(summary, demo_path)
        return _score_ahei_nhanes(summary, day)

    day1 = _compute_day(1, fped_ind_path, nutrient_ind_path)
    day2 = _compute_day(2, fped_ind_path2, nutrient_ind_path2)
    result = _average_day_results(day1, day2, preserve_cols=["RESPONDENTID", "GENDER"])
    return _merge_demo(result, demo_path)


def compute_medi_nhanes_fped(
    fped_ind_path=None,
    nutrient_ind_path=None,
    fped_ind_path2=None,
    nutrient_ind_path2=None,
    sweets_code=None,
    fat_oil_code=None,
    ssb_code=None,
    olive_oil_code=None,
    demo_path=None,
    version="v1",
):
    if sweets_code is None:
        sweets_code = _SWEETS_CODES_DEFAULT
    if fat_oil_code is None:
        fat_oil_code = _FAT_OIL_CODES_DEFAULT
    if ssb_code is None:
        ssb_code = _MEDI_SSB_CODES_DEFAULT
    if olive_oil_code is None:
        olive_oil_code = _OLIVE_OIL_CODES_DEFAULT

    medi_fn = compute_medi_v2 if version.lower() == "v2" else compute_medi

    def _compute_day(day, fped_path, nutrient_path):
        joined = _prepare_iff_day(fped_path, nutrient_path, day, filter_positive_line_kcal=True)
        summary = _summarize_medi(joined, day, ssb_code, sweets_code, fat_oil_code, olive_oil_code)
        if summary is None or summary.empty:
            return None

        result = medi_fn(
            data=summary,
            respondent_id=summary["SEQN"].values,
            olive_oil=summary["OLIVE_OIL_SERV_MEDI"].values,
            fruit=summary["FRT_SERV_MEDI"].values,
            vegetable=summary["VEG_SERV_MEDI"].values,
            legumes=summary["LEGUMES_SERV_MEDI"].values,
            nuts=summary["NUTS_SERV_MEDI"].values,
            fish_seafood=summary["FISH_SEAFOOD_SERV_MEDI"].values,
            alcohol=summary["ALCOHOL_SERV_MEDI"].values,
            ssb=summary["SSB_SERV_MEDI"].values,
            sweets=summary["SWEETS_SERV_MEDI"].values,
            discret_fat=summary["DISCRET_FAT_SERV_MEDI"].values,
            red_processed_meat=summary["REDPROC_MEAT_SERV_MEDI"].values,
        )
        result["SEQN"] = summary["SEQN"].values
        result["RESPONDENTID"] = summary["SEQN"].values
        return result

    day1 = _compute_day(1, fped_ind_path, nutrient_ind_path)
    day2 = _compute_day(2, fped_ind_path2, nutrient_ind_path2)
    result = _average_day_results(day1, day2, preserve_cols=["RESPONDENTID"])
    return _merge_demo(result, demo_path)


def compute_di_gm_nhanes_fped(
    fped_ind_path=None,
    nutrient_ind_path=None,
    fped_ind_path2=None,
    nutrient_ind_path2=None,
    avocado_code=None,
    broccoli_code=None,
    chickpea_code=None,
    coffee_code=None,
    cranberry_code=None,
    fermented_dairy_code=None,
    green_tea_code=None,
    soybean_code=None,
    demo_path=None,
    two_day_method="intake_average",
):
    """Compute DI-GM from NHANES FPED individual-food files.

    two_day_method:
      - "intake_average" (default): average Day 1/Day 2 component intakes, then score.
      - "score_average": score each day first, then average scores (R package parity).
    """
    code_map = {
        "AVOCADO": avocado_code if avocado_code is not None else _AVOCADO_CODES_DEFAULT,
        "BROCCOLI": broccoli_code if broccoli_code is not None else _BROCCOLI_CODES_DEFAULT,
        "CHICKPEA": chickpea_code if chickpea_code is not None else _CHICKPEA_CODES_DEFAULT,
        "COFFEE": coffee_code if coffee_code is not None else _COFFEE_CODES_DEFAULT,
        "CRANBERRY": cranberry_code if cranberry_code is not None else _CRANBERRY_CODES_DEFAULT,
        "FERMENTED_DAIRY": fermented_dairy_code if fermented_dairy_code is not None else _FERMENTED_DAIRY_CODES_DEFAULT,
        "GREEN_TEA": green_tea_code if green_tea_code is not None else _GREEN_TEA_CODES_DEFAULT,
        "SOYBEAN": soybean_code if soybean_code is not None else _SOYBEAN_CODES_DEFAULT,
    }

    def _compute_day_summary(day, fped_path, nutrient_path):
        joined = _prepare_iff_day(fped_path, nutrient_path, day, filter_positive_line_kcal=True)
        return _summarize_di_gm(joined, day, code_map)

    def _score_summary(summary, *, fat_pct_col="TOTAL_FAT_PCT"):
        if summary is None or summary.empty:
            return None
        result = compute_di_gm(
            data=summary,
            respondent_id=summary["SEQN"].values,
            gender=summary["GENDER"].values,
            avocado=summary["AVOCADO"].values,
            broccoli=summary["BROCCOLI"].values,
            chickpea=summary["CHICKPEA"].values,
            coffee=summary["COFFEE"].values,
            cranberry=summary["CRANBERRY"].values,
            fermented_dairy=summary["FERMENTED_DAIRY"].values,
            fiber=summary["FIBER"].values,
            green_tea=summary["GREEN_TEA"].values,
            soybean=summary["SOYBEAN"].values,
            whole_grain=summary["WHOLE_GRAIN"].values,
            total_fat_pct=summary[fat_pct_col].values,
            processed_meat=summary["PROCESSED_MEAT"].values,
            red_meat=summary["RED_MEAT"].values,
            refined_grain=summary["REFINED_GRAIN"].values,
        )
        result["SEQN"] = summary["SEQN"].values
        result["RESPONDENTID"] = summary["SEQN"].values
        return result

    method = str(two_day_method or "intake_average").lower()
    day1_summary = _compute_day_summary(1, fped_ind_path, nutrient_ind_path)
    day2_summary = _compute_day_summary(2, fped_ind_path2, nutrient_ind_path2)

    if method in {"score_average", "score", "r"}:
        day1 = _score_summary(day1_summary, fat_pct_col="TOTAL_FAT_PCT")
        day2 = _score_summary(day2_summary, fat_pct_col="TOTAL_FAT_PCT")
        result = _average_day_results(day1, day2, preserve_cols=["RESPONDENTID", "GENDER"])
    elif method in {"intake_average", "intake", "paper"}:
        summary = _average_day_results(day1_summary, day2_summary, preserve_cols=["GENDER"])
        if summary is None or summary.empty:
            result = None
        else:
            energy = pd.to_numeric(summary.get("ENERGY", 0), errors="coerce").fillna(0.0)
            fat = pd.to_numeric(summary.get("TOTAL_FAT", 0), errors="coerce").fillna(0.0)
            summary["TOTAL_FAT_PCT_FROM_AVG"] = np.where(energy > 0, (fat * 9.0 / energy) * 100.0, 0.0)
            result = _score_summary(summary, fat_pct_col="TOTAL_FAT_PCT_FROM_AVG")
    else:
        raise ValueError("two_day_method must be 'intake_average' or 'score_average'")

    return _merge_demo(result, demo_path)
