"""Diet Quality Index-International (DQI-I) scoring."""

from __future__ import annotations

import numpy as np
import pandas as pd


_ENERGY_ANCHORS = (1700.0, 2200.0, 2700.0)
_ADEQUACY_TARGETS = {
    1700.0: {"fruit": 2.0, "vegetable": 3.0, "grain": 6.0, "fiber": 20.0},
    2200.0: {"fruit": 3.0, "vegetable": 4.0, "grain": 9.0, "fiber": 25.0},
    2700.0: {"fruit": 4.0, "vegetable": 5.0, "grain": 11.0, "fiber": 30.0},
}


def _as_series(values, name: str, length: int | None = None) -> pd.Series:
    series = pd.Series(np.asarray(values), name=name)
    if length is not None and len(series) != length:
        raise ValueError(f"{name} length does not match the expected number of rows.")
    return pd.to_numeric(series, errors="coerce")


def _resolve_ids(respondent_id, length: int) -> pd.Series:
    if respondent_id is None:
        return pd.Series(np.arange(1, length + 1), name="RESPONDENTID")
    series = pd.Series(np.asarray(respondent_id), name="RESPONDENTID")
    if len(series) != length:
        raise ValueError("respondent_id length must match the number of rows.")
    return series.reset_index(drop=True)


def _energy_anchor(total_kcal: pd.Series) -> pd.Series:
    distances = pd.DataFrame({anchor: (total_kcal - anchor).abs() for anchor in _ENERGY_ANCHORS})
    values = distances.to_numpy(dtype=float)
    all_missing = np.isnan(values).all(axis=1)
    safe = np.where(np.isnan(values), np.inf, values)
    selected = np.asarray(_ENERGY_ANCHORS, dtype=float)[np.argmin(safe, axis=1)]
    selected[all_missing] = np.nan
    return pd.Series(selected, index=total_kcal.index, dtype=float)


def _target_by_anchor(anchors: pd.Series, key: str) -> pd.Series:
    return anchors.map(lambda anchor: _ADEQUACY_TARGETS.get(float(anchor), {}).get(key, np.nan))


def _gender_flags(gender) -> tuple[pd.Series, pd.Series]:
    raw = pd.Series(np.asarray(gender))
    numeric = pd.to_numeric(raw, errors="coerce")
    text = raw.astype(str).str.strip().str.lower()
    male = numeric.eq(1) | text.isin({"1", "m", "male", "man", "boy", "男"})
    female = numeric.eq(2) | text.isin({"2", "f", "female", "woman", "girl", "女"})
    return male, female


def _calcium_target(age: pd.Series, male: pd.Series, female: pd.Series) -> pd.Series:
    return pd.Series(
        np.select(
            [
                (age >= 1) & (age <= 3),
                (age >= 4) & (age <= 8),
                (age >= 9) & (age <= 18),
                (age >= 19) & (age <= 50),
                (age >= 51) & (age <= 70) & male,
                (age >= 51) & (age <= 70) & female,
                age >= 71,
            ],
            [700.0, 1000.0, 1300.0, 1000.0, 1000.0, 1200.0, 1200.0],
            default=np.nan,
        )
    )


def _iron_target(age: pd.Series, male: pd.Series, female: pd.Series) -> pd.Series:
    return pd.Series(
        np.select(
            [
                (age >= 1) & (age <= 3),
                (age >= 4) & (age <= 8),
                (age >= 9) & (age <= 13),
                (age >= 14) & (age <= 18) & male,
                (age >= 14) & (age <= 18) & female,
                (age >= 19) & (age <= 50) & male,
                (age >= 19) & (age <= 50) & female,
                age >= 51,
            ],
            [7.0, 10.0, 8.0, 11.0, 15.0, 8.0, 18.0, 8.0],
            default=np.nan,
        )
    )


def _vitamin_c_target(age: pd.Series, male: pd.Series, female: pd.Series) -> pd.Series:
    return pd.Series(
        np.select(
            [
                (age >= 1) & (age <= 3),
                (age >= 4) & (age <= 8),
                (age >= 9) & (age <= 13),
                (age >= 14) & (age <= 18) & male,
                (age >= 14) & (age <= 18) & female,
                (age >= 19) & male,
                (age >= 19) & female,
            ],
            [15.0, 25.0, 45.0, 75.0, 65.0, 90.0, 75.0],
            default=np.nan,
        )
    )


def _proportional_score(intake: pd.Series, target: pd.Series, max_score: float) -> pd.Series:
    return pd.Series(
        np.where(
            pd.notna(intake) & pd.notna(target) & (target > 0),
            np.clip(intake / target * max_score, 0.0, max_score),
            np.nan,
        )
    )


def _three_level_score(values: pd.Series, *, good_max: float, mid_max: float, high_score: float, mid_score: float) -> pd.Series:
    result = np.select(
        [values <= good_max, values <= mid_max],
        [high_score, mid_score],
        default=0.0,
    )
    return pd.Series(np.where(values.isna(), np.nan, result), dtype=float)


def compute_dqii(
    data,
    respondent_id,
    age,
    gender,
    total_kcal,
    grain,
    vegetable,
    fruit,
    meat,
    poultry,
    fish,
    dairy,
    legumes,
    egg,
    fiber,
    protein,
    iron,
    calcium,
    vitamin_c,
    carbohydrate,
    total_fat,
    saturated_fat,
    mufa,
    pufa,
    cholesterol,
    sodium,
    empty_calorie_pct_energy,
):
    """Compute the Diet Quality Index-International (DQI-I).

    Food-group inputs are expected as servings/day. Macronutrients are entered
    as g/day and translated to percent energy by `total_kcal`. The current
    general-mode implementation expects `empty_calorie_pct_energy` as a
    precomputed percentage of total energy.
    """

    age_s = _as_series(age, "age")
    ids = _resolve_ids(respondent_id, len(age_s))
    male, female = _gender_flags(gender)

    total_kcal_s = _as_series(total_kcal, "total_kcal", len(ids))
    grain_s = _as_series(grain, "grain", len(ids))
    vegetable_s = _as_series(vegetable, "vegetable", len(ids))
    fruit_s = _as_series(fruit, "fruit", len(ids))
    meat_s = _as_series(meat, "meat", len(ids))
    poultry_s = _as_series(poultry, "poultry", len(ids))
    fish_s = _as_series(fish, "fish", len(ids))
    dairy_s = _as_series(dairy, "dairy", len(ids))
    legumes_s = _as_series(legumes, "legumes", len(ids))
    egg_s = _as_series(egg, "egg", len(ids))
    fiber_s = _as_series(fiber, "fiber", len(ids))
    protein_s = _as_series(protein, "protein", len(ids))
    iron_s = _as_series(iron, "iron", len(ids))
    calcium_s = _as_series(calcium, "calcium", len(ids))
    vitamin_c_s = _as_series(vitamin_c, "vitamin_c", len(ids))
    carbohydrate_s = _as_series(carbohydrate, "carbohydrate", len(ids))
    total_fat_s = _as_series(total_fat, "total_fat", len(ids))
    saturated_fat_s = _as_series(saturated_fat, "saturated_fat", len(ids))
    mufa_s = _as_series(mufa, "mufa", len(ids))
    pufa_s = _as_series(pufa, "pufa", len(ids))
    cholesterol_s = _as_series(cholesterol, "cholesterol", len(ids))
    sodium_s = _as_series(sodium, "sodium", len(ids))
    empty_calorie_s = _as_series(empty_calorie_pct_energy, "empty_calorie_pct_energy", len(ids))

    out = pd.DataFrame({"RESPONDENTID": ids})

    overall_groups = pd.DataFrame(
        {
            "grain": grain_s >= 1.0,
            "vegetable": vegetable_s >= 1.0,
            "fruit": fruit_s >= 1.0,
            "animal": (meat_s + poultry_s + fish_s + egg_s) >= 1.0,
            "dairy_legumes": (dairy_s + legumes_s) >= 1.0,
        }
    )
    out["DQII_VAR_OVERALL"] = overall_groups.sum(axis=1) * 3.0
    overall_input_complete = pd.concat(
        [grain_s, vegetable_s, fruit_s, meat_s, poultry_s, fish_s, egg_s, dairy_s, legumes_s],
        axis=1,
    ).notna().all(axis=1)
    out.loc[~overall_input_complete, "DQII_VAR_OVERALL"] = np.nan

    protein_source_count = pd.DataFrame(
        {
            "meat": meat_s >= 0.5,
            "poultry": poultry_s >= 0.5,
            "fish": fish_s >= 0.5,
            "dairy": dairy_s >= 0.5,
            "legumes": legumes_s >= 0.5,
            "egg": egg_s >= 0.5,
        }
    ).sum(axis=1)
    out["DQII_VAR_PROTEIN"] = np.select(
        [protein_source_count >= 3, protein_source_count >= 2, protein_source_count >= 1],
        [5.0, 3.0, 1.0],
        default=0.0,
    )
    protein_input_complete = pd.concat(
        [meat_s, poultry_s, fish_s, dairy_s, legumes_s, egg_s], axis=1
    ).notna().all(axis=1)
    out.loc[~protein_input_complete, "DQII_VAR_PROTEIN"] = np.nan
    out["DQII_VARIETY"] = out[["DQII_VAR_OVERALL", "DQII_VAR_PROTEIN"]].sum(axis=1, min_count=2)

    anchors = _energy_anchor(total_kcal_s)
    fruit_target = _target_by_anchor(anchors, "fruit")
    vegetable_target = _target_by_anchor(anchors, "vegetable")
    grain_target = _target_by_anchor(anchors, "grain")
    fiber_target = _target_by_anchor(anchors, "fiber")
    protein_pct = np.where(total_kcal_s > 0, protein_s * 4.0 / total_kcal_s * 100.0, np.nan)

    out["DQII_ADEQ_FRUIT"] = _proportional_score(fruit_s, fruit_target, 5.0)
    out["DQII_ADEQ_VEGETABLE"] = _proportional_score(vegetable_s, vegetable_target, 5.0)
    out["DQII_ADEQ_GRAIN"] = _proportional_score(grain_s, grain_target, 5.0)
    out["DQII_ADEQ_FIBER"] = _proportional_score(fiber_s, fiber_target, 5.0)
    out["DQII_ADEQ_PROTEIN"] = _proportional_score(pd.Series(protein_pct), pd.Series([10.0] * len(ids)), 5.0)
    out["DQII_ADEQ_IRON"] = _proportional_score(iron_s, _iron_target(age_s, male, female), 5.0)
    out["DQII_ADEQ_CALCIUM"] = _proportional_score(calcium_s, _calcium_target(age_s, male, female), 5.0)
    out["DQII_ADEQ_VITC"] = _proportional_score(vitamin_c_s, _vitamin_c_target(age_s, male, female), 5.0)
    adequacy_cols = [col for col in out.columns if col.startswith("DQII_ADEQ_")]
    out["DQII_ADEQUACY"] = out[adequacy_cols].sum(axis=1, min_count=len(adequacy_cols))

    total_fat_pct = np.where(total_kcal_s > 0, total_fat_s * 9.0 / total_kcal_s * 100.0, np.nan)
    saturated_fat_pct = np.where(total_kcal_s > 0, saturated_fat_s * 9.0 / total_kcal_s * 100.0, np.nan)
    out["DQII_MOD_TOTALFAT"] = _three_level_score(pd.Series(total_fat_pct), good_max=20.0, mid_max=30.0, high_score=6.0, mid_score=3.0)
    out["DQII_MOD_SATFAT"] = _three_level_score(pd.Series(saturated_fat_pct), good_max=7.0, mid_max=10.0, high_score=6.0, mid_score=3.0)
    out["DQII_MOD_CHOLESTEROL"] = _three_level_score(cholesterol_s, good_max=300.0, mid_max=400.0, high_score=6.0, mid_score=3.0)
    out["DQII_MOD_SODIUM"] = _three_level_score(sodium_s, good_max=2400.0, mid_max=3400.0, high_score=6.0, mid_score=3.0)
    out["DQII_MOD_EMPTYCAL"] = _three_level_score(empty_calorie_s, good_max=3.0, mid_max=10.0, high_score=6.0, mid_score=3.0)
    moderation_cols = [col for col in out.columns if col.startswith("DQII_MOD_")]
    out["DQII_MODERATION"] = out[moderation_cols].sum(axis=1, min_count=len(moderation_cols))

    carbohydrate_pct = np.where(total_kcal_s > 0, carbohydrate_s * 4.0 / total_kcal_s * 100.0, np.nan)
    fat_pct = np.where(total_kcal_s > 0, total_fat_s * 9.0 / total_kcal_s * 100.0, np.nan)
    out["DQII_BAL_MACRO"] = np.select(
        [
            (carbohydrate_pct >= 55.0) & (carbohydrate_pct <= 65.0)
            & (protein_pct >= 10.0) & (protein_pct <= 15.0)
            & (fat_pct >= 15.0) & (fat_pct <= 25.0),
            (carbohydrate_pct >= 52.0) & (carbohydrate_pct <= 68.0)
            & (protein_pct >= 9.0) & (protein_pct <= 16.0)
            & (fat_pct >= 13.0) & (fat_pct <= 27.0),
            (carbohydrate_pct >= 50.0) & (carbohydrate_pct <= 70.0)
            & (protein_pct >= 8.0) & (protein_pct <= 17.0)
            & (fat_pct >= 12.0) & (fat_pct <= 30.0),
        ],
        [6.0, 4.0, 2.0],
        default=0.0,
    )
    macro_input_complete = pd.concat(
        [total_kcal_s, carbohydrate_s, protein_s, total_fat_s], axis=1
    ).notna().all(axis=1) & (total_kcal_s > 0)
    out.loc[~macro_input_complete, "DQII_BAL_MACRO"] = np.nan

    p_to_s = np.where(saturated_fat_s > 0, pufa_s / saturated_fat_s, np.nan)
    m_to_s = np.where(saturated_fat_s > 0, mufa_s / saturated_fat_s, np.nan)
    out["DQII_BAL_FATTYACID"] = np.select(
        [
            (p_to_s >= 1.0) & (p_to_s <= 1.5) & (m_to_s >= 1.0) & (m_to_s <= 1.5),
            (p_to_s >= 0.8) & (p_to_s <= 1.7) & (m_to_s >= 0.8) & (m_to_s <= 1.7),
        ],
        [4.0, 2.0],
        default=0.0,
    )
    fatty_input_complete = pd.concat(
        [saturated_fat_s, pufa_s, mufa_s], axis=1
    ).notna().all(axis=1) & (saturated_fat_s > 0)
    out.loc[~fatty_input_complete, "DQII_BAL_FATTYACID"] = np.nan
    out["DQII_BALANCE"] = out[["DQII_BAL_MACRO", "DQII_BAL_FATTYACID"]].sum(axis=1, min_count=2)
    total_cols = ["DQII_VARIETY", "DQII_ADEQUACY", "DQII_MODERATION", "DQII_BALANCE"]
    out["DQII_ALL"] = out[total_cols].sum(axis=1, min_count=len(total_cols))
    return out
