"""Focused tests for the newly added phase 2-4 index implementations."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dietaryindex import (
    compute_cdai,
    compute_chei,
    compute_china_dii,
    compute_dbi,
    compute_edii,
    compute_gdqs,
    compute_wish,
    compute_obs,
    compute_dqii,
    compute_inq,
    compute_mar,
    compute_mind,
    compute_nar,
    compute_neap,
    compute_nrf,
    compute_pral,
)


def test_mind_reaches_full_score_when_all_targets_are_met():
    result = compute_mind(
        data=None,
        respondent_id=[1],
        green_leafy_vegetables=[7],
        other_vegetables=[1.2],
        nuts=[5],
        berries=[2],
        beans=[4],
        whole_grains=[3],
        fish=[1],
        poultry=[2],
        olive_oil_primary=[1],
        wine=[1.0],
        red_meats=[1],
        butter_margarine=[0.5],
        cheese=[0],
        pastries_sweets=[1],
        fried_fast_food=[0],
    )
    assert result.loc[0, "MIND_ALL"] == 15.0


def test_chei_can_reach_full_score_with_target_density_inputs():
    result = compute_chei(
        data=None,
        respondent_id=[1],
        gender=[1],
        total_grains=[2.5],
        whole_grains_mixed_beans=[0.6],
        tubers=[0.3],
        total_vegetables=[1.9],
        dark_vegetables=[0.9],
        fruits=[1.1],
        dairy=[0.5],
        soybeans=[0.4],
        fish_seafood=[0.6],
        poultry=[0.3],
        eggs=[0.5],
        seeds_nuts=[0.4],
        red_meat=[0.2],
        cooking_oils=[15.0],
        sodium=[900.0],
        added_sugars_pct_energy=[8.0],
        alcohol=[0.0],
    )
    assert result.loc[0, "CHEI_ALL"] == 100.0


def test_mind_uses_the_original_table_boundary_semantics():
    eps = 1e-9
    result = compute_mind(
        data=None,
        respondent_id=list(range(1, 9)),
        green_leafy_vegetables=[2.0, 2.0 + eps, 6.0, 7.0, 7.0, 7.0, 7.0, 7.0],
        other_vegetables=[1.0] * 8,
        nuts=[5.0, 5.0, 5.0, 0.25 - eps, 0.25, 5.0, 5.0, 5.0],
        berries=[2.0] * 8,
        beans=[4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0 + eps, 4.0],
        whole_grains=[3.0] * 8,
        fish=[1.0] * 8,
        poultry=[2.0] * 8,
        olive_oil_primary=[1.0] * 8,
        wine=[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 + eps, 1.0],
        red_meats=[0.0] * 8,
        butter_margarine=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0],
        cheese=[0.0] * 8,
        pastries_sweets=[0.0] * 8,
        fried_fast_food=[0.0] * 8,
    )

    assert result.loc[0, "MIND_GREEN_LEAFY_VEG"] == 0.0
    assert result.loc[1, "MIND_GREEN_LEAFY_VEG"] == 0.5
    assert result.loc[2, "MIND_GREEN_LEAFY_VEG"] == 1.0
    assert result.loc[3, "MIND_NUTS"] == 0.0
    assert result.loc[4, "MIND_NUTS"] == 0.5
    assert result.loc[5, "MIND_BEANS"] == 0.5
    assert result.loc[6, "MIND_BEANS"] == 1.0
    assert result.loc[6, "MIND_WINE"] == 0.0
    assert result.loc[7, "MIND_BUTTER_MARGARINE"] == 0.5


def test_dqii_can_reach_full_score_when_all_domains_hit_targets():
    result = compute_dqii(
        data=None,
        respondent_id=[1],
        age=[30],
        gender=[1],
        total_kcal=[2200.0],
        grain=[9.0],
        vegetable=[4.0],
        fruit=[3.0],
        meat=[0.5],
        poultry=[0.5],
        fish=[0.5],
        dairy=[0.5],
        legumes=[0.5],
        egg=[0.5],
        fiber=[25.0],
        protein=[70.0],
        iron=[8.0],
        calcium=[1000.0],
        vitamin_c=[90.0],
        carbohydrate=[330.0],
        total_fat=[48.0],
        saturated_fat=[10.0],
        mufa=[12.0],
        pufa=[12.0],
        cholesterol=[200.0],
        sodium=[2000.0],
        empty_calorie_pct_energy=[2.0],
    )
    assert result.loc[0, "DQII_VARIETY"] == 20.0
    assert result.loc[0, "DQII_ADEQUACY"] == 40.0
    assert result.loc[0, "DQII_MODERATION"] == 30.0
    assert result.loc[0, "DQII_BALANCE"] == 10.0
    assert result.loc[0, "DQII_ALL"] == 100.0


def test_dbi_hits_zero_imbalance_at_reference_targets():
    result = compute_dbi(
        data=None,
        respondent_id=[1],
        gender=[1],
        cereals=[300.0],
        vegetables=[350.0],
        fruits=[300.0],
        dairy=[300.0],
        soybean=[40.0],
        meat=[50.0],
        fish_shrimp=[80.0],
        egg=[40.0],
        oil=[20.0],
        salt=[5.0],
        alcohol=[0.0],
        water=[1300.0],
        rice_products=[80.0],
        wheat_products=[80.0],
        coarse_grains_tubers=[80.0],
        dark_vegetables=[80.0],
        light_vegetables=[80.0],
        red_meat_products=[30.0],
        poultry_game=[30.0],
    )
    assert result.loc[0, "DBI_DQD"] == 0.0
    assert result.loc[0, "DBI_LBS"] == 0.0
    assert result.loc[0, "DBI_HBS"] == 0.0
    assert result.loc[0, "DBI_TS"] == 0.0


def test_dbi_uses_five_level_fish_and_sex_specific_alcohol_bands():
    fish = [0, 30, 45, 60, 75, 0, 30, 45, 60, 75]
    alcohol = [25, 50, 75, 100, 101, 15, 30, 45, 60, 61]
    n = len(fish)
    result = compute_dbi(
        data=None,
        respondent_id=np.arange(1, n + 1),
        gender=[1] * 5 + [2] * 5,
        cereals=[300] * n,
        vegetables=[350] * n,
        fruits=[300] * n,
        dairy=[300] * n,
        soybean=[40] * n,
        meat=[50] * n,
        fish_shrimp=fish,
        egg=[40] * n,
        oil=[20] * n,
        salt=[5] * n,
        alcohol=alcohol,
        water=[1300] * n,
        rice_products=[80] * n,
        wheat_products=[80] * n,
        coarse_grains_tubers=[80] * n,
        dark_vegetables=[80] * n,
        light_vegetables=[80] * n,
        red_meat_products=[30] * n,
        poultry_game=[30] * n,
    )
    assert result["DBI_FISH_SHRIMP"].tolist() == [-4, -3, -2, -1, 0] * 2
    assert result["DBI_ALCOHOL"].tolist() == [0, 1, 2, 3, 4] * 2


def test_gdqs_reaches_full_score_with_maximizing_pattern():
    result = compute_gdqs(
        data=None,
        respondent_id=[1],
        citrus_fruits=[80.0],
        deep_orange_fruits=[130.0],
        other_fruits=[120.0],
        dark_green_leafy_vegetables=[40.0],
        cruciferous_vegetables=[40.0],
        deep_orange_vegetables=[50.0],
        other_vegetables=[120.0],
        legumes=[50.0],
        deep_orange_tubers=[70.0],
        nuts_seeds=[20.0],
        whole_grains=[20.0],
        liquid_oils=[10.0],
        fish_shellfish=[80.0],
        poultry_game_meat=[50.0],
        low_fat_dairy=[150.0],
        eggs=[40.0],
        high_fat_dairy=[200.0],
        red_meat=[20.0],
        processed_meat=[0.0],
        refined_grains_baked_goods=[0.0],
        sweets_ice_cream=[0.0],
        sugar_sweetened_beverages=[0.0],
        juice=[0.0],
        white_roots_tubers=[0.0],
        purchased_deep_fried_foods=[0.0],
    )
    assert result.loc[0, "GDQS_POS"] == 32.0
    assert result.loc[0, "GDQS_NEG"] == 17.0
    assert result.loc[0, "GDQS_ALL"] == 49.0


def test_wish_reaches_full_score_with_target_pattern():
    result = compute_wish(
        data=None,
        respondent_id=[1],
        whole_grains=[130.0],
        vegetables=[320.0],
        fruit=[220.0],
        legumes=[80.0],
        unsaturated_oils=[45.0],
        fish=[40.0],
        dairy=[300.0],
        nuts=[55.0],
        poultry=[20.0],
        eggs=[10.0],
        red_meat=[10.0],
        saturated_oils=[10.0],
        added_sugars=[20.0],
    )
    assert result.loc[0, "WISH_HEALTHY"] == 100.0
    assert result.loc[0, "WISH_LESS_HEALTHY"] == 30.0
    assert result.loc[0, "WISH_LOW_ENV"] == 60.0
    assert result.loc[0, "WISH_HIGH_ENV"] == 70.0
    assert result.loc[0, "WISH_ALL"] == 130.0


def test_nutrient_density_family_returns_expected_reference_scores():
    energy = np.array([2000.0])
    protein = np.array([56.0])
    fiber = np.array([31.0])
    vitamin_a = np.array([900.0])
    vitamin_c = np.array([90.0])
    vitamin_e = np.array([15.0])
    calcium = np.array([1300.0])
    iron = np.array([8.0])
    magnesium = np.array([420.0])
    potassium = np.array([4700.0])
    saturated_fat = np.array([22.0])
    added_sugar = np.array([50.0])
    sodium = np.array([2300.0])

    nrf = compute_nrf(
        data=None,
        respondent_id=[1],
        energy=energy,
        protein=[50.0],
        fiber=[25.0],
        vitamin_a=[1500.0],
        vitamin_c=[60.0],
        vitamin_e=[20.0],
        calcium=[1000.0],
        iron=[18.0],
        magnesium=[400.0],
        potassium=[3500.0],
        saturated_fat=[20.0],
        added_sugar=added_sugar,
        sodium=[2400.0],
    )
    nar = compute_nar(
        data=None,
        respondent_id=[1],
        protein=protein,
        fiber=fiber,
        vitamin_a=vitamin_a,
        vitamin_c=vitamin_c,
        vitamin_e=vitamin_e,
        calcium=calcium,
        iron=iron,
        magnesium=magnesium,
        potassium=potassium,
    )
    mar = compute_mar(
        data=None,
        respondent_id=[1],
        protein=protein,
        fiber=fiber,
        vitamin_a=vitamin_a,
        vitamin_c=vitamin_c,
        vitamin_e=vitamin_e,
        calcium=calcium,
        iron=iron,
        magnesium=magnesium,
        potassium=potassium,
    )
    inq = compute_inq(
        data=None,
        respondent_id=[1],
        energy=energy,
        protein=protein,
        fiber=fiber,
        vitamin_a=vitamin_a,
        vitamin_c=vitamin_c,
        vitamin_e=vitamin_e,
        calcium=calcium,
        iron=iron,
        magnesium=magnesium,
        potassium=potassium,
    )

    assert nrf.loc[0, "NRF_NR9_SUM"] == 900.0
    assert nrf.loc[0, "NRF_LIM3_SUM"] == 300.0
    assert nrf.loc[0, "NRF_ALL"] == 600.0

    nrf_excess = compute_nrf(
        data=None,
        respondent_id=[1],
        energy=[2000.0],
        protein=[50.0],
        fiber=[25.0],
        vitamin_a=[1500.0],
        vitamin_c=[60.0],
        vitamin_e=[20.0],
        calcium=[1000.0],
        iron=[18.0],
        magnesium=[400.0],
        potassium=[3500.0],
        saturated_fat=[40.0],
        added_sugar=[100.0],
        sodium=[4800.0],
    )
    assert nrf_excess.loc[0, "NRF_LIM3_SUM"] == 300.0
    assert nrf_excess.loc[0, "NRF_ALL"] == 600.0

    nrf_excess_uncapped = compute_nrf(
        data=None,
        respondent_id=[1],
        energy=[2000.0],
        protein=[50.0],
        fiber=[25.0],
        vitamin_a=[1500.0],
        vitamin_c=[60.0],
        vitamin_e=[20.0],
        calcium=[1000.0],
        iron=[18.0],
        magnesium=[400.0],
        potassium=[3500.0],
        saturated_fat=[40.0],
        added_sugar=[100.0],
        sodium=[4800.0],
        version="nrf9.3_2009_metric_uncapped_lim",
    )
    assert nrf_excess_uncapped.loc[0, "NRF_LIM3_SUM"] == 600.0
    assert nrf_excess_uncapped.loc[0, "NRF_ALL"] == 300.0
    assert nar.loc[0, "NAR_ALL"] == 1.0
    assert mar.loc[0, "MAR_ALL"] == 100.0
    assert inq.loc[0, "INQ_ALL"] == 1.0


def test_nrf_requires_the_complete_fixed_9_plus_3_panel():
    result = compute_nrf(
        data=None,
        respondent_id=[1, 2],
        energy=[2000.0, 2000.0],
        protein=[50.0, np.nan],
        fiber=[25.0, 25.0],
        vitamin_a=[1500.0, 1500.0],
        vitamin_c=[60.0, 60.0],
        vitamin_e=[20.0, 20.0],
        calcium=[1000.0, 1000.0],
        iron=[18.0, 18.0],
        magnesium=[400.0, 400.0],
        potassium=[3500.0, 3500.0],
        saturated_fat=[20.0, 20.0],
        added_sugar=[50.0, 50.0],
        sodium=[2400.0, 2400.0],
    )
    assert result.loc[0, "NRF_ALL"] == 600.0
    assert np.isnan(result.loc[1, "NRF_NR9_SUM"])
    assert np.isnan(result.loc[1, "NRF_ALL"])


def test_pral_and_neap_match_hand_calculated_formulae():
    pral = compute_pral(
        data=None,
        respondent_id=[1],
        protein=[70.0],
        phosphorus=[1000.0],
        potassium=[3000.0],
        magnesium=[350.0],
        calcium=[900.0],
    )
    neap = compute_neap(
        data=None,
        respondent_id=[1],
        protein=[70.0],
        potassium=[3000.0],
    )
    expected_pral = 0.49 * 70 + 0.037 * 1000 - 0.021 * 3000 - 0.026 * 350 - 0.013 * 900
    expected_neap = 54.5 * (70 / (3000.0 / 39.0983)) - 10.2
    assert abs(pral.loc[0, "PRAL_ALL"] - expected_pral) < 1e-9
    assert abs(neap.loc[0, "NEAP_ALL"] - expected_neap) < 1e-9


def test_cdai_returns_zero_for_row_at_sample_means():
    result = compute_cdai(
        data=None,
        respondent_id=[1, 2, 3],
        zinc=[1.0, 2.0, 3.0],
        selenium=[1.0, 2.0, 3.0],
        total_carotenoids=[1.0, 2.0, 3.0],
        vitamin_a=[1.0, 2.0, 3.0],
        vitamin_c=[1.0, 2.0, 3.0],
        vitamin_e=[1.0, 2.0, 3.0],
    )
    assert abs(result.loc[1, "CDAI_ALL"]) < 1e-9


def test_obs_can_reach_full_score_for_top_profile_within_each_sex():
    result = compute_obs(
        data=None,
        respondent_id=[1, 2, 3, 4, 5, 6],
        gender=[1, 1, 1, 2, 2, 2],
        fiber=[1, 2, 3, 1, 2, 3],
        carotene_re=[1, 2, 3, 1, 2, 3],
        vitamin_b2=[1, 2, 3, 1, 2, 3],
        niacin=[1, 2, 3, 1, 2, 3],
        total_folate=[1, 2, 3, 1, 2, 3],
        calcium=[1, 2, 3, 1, 2, 3],
        zinc=[1, 2, 3, 1, 2, 3],
        magnesium=[1, 2, 3, 1, 2, 3],
        copper=[1, 2, 3, 1, 2, 3],
        selenium=[1, 2, 3, 1, 2, 3],
        vitamin_b6=[1, 2, 3, 1, 2, 3],
        vitamin_b12=[1, 2, 3, 1, 2, 3],
        vitamin_c=[1, 2, 3, 1, 2, 3],
        vitamin_e=[1, 2, 3, 1, 2, 3],
        iron=[3, 2, 1, 3, 2, 1],
        total_fat=[3, 2, 1, 3, 2, 1],
        bmi=[3, 2, 1, 3, 2, 1],
        cotinine=[3, 2, 1, 3, 2, 1],
        physical_activity_met=[300, 900, 3000, 300, 900, 3000],
        alcohol_drinks_per_day=[3.0, 1.0, 0.0, 2.0, 0.5, 0.0],
        alcohol_drinks_per_year=[100, 100, 0, 100, 100, 0],
    )
    assert result.loc[2, "OBS_DIET"] == 32.0
    assert result.loc[2, "OBS_LIFESTYLE"] == 8.0
    assert result.loc[2, "OBS_ALL"] == 40.0
    assert result.loc[5, "OBS_DIET"] == 32.0
    assert result.loc[5, "OBS_LIFESTYLE"] == 8.0
    assert result.loc[5, "OBS_ALL"] == 40.0


def test_obs_physical_activity_uses_published_600_and_3000_met_cutoffs():
    from dietaryindex.core.obs import _score_physical_activity

    assert _score_physical_activity([599, 600, 2999.9, 3000]).tolist() == [0.0, 1.0, 1.0, 2.0]


def test_edii_matches_published_weighted_sum_formula():
    values = {
        "processed_meat": 1.0,
        "red_meat": 0.5,
        "organ_meat": 0.25,
        "other_fish": 0.3,
        "other_vegetables": 2.0,
        "refined_grains": 3.0,
        "high_energy_beverages": 1.5,
        "low_energy_beverages": 0.4,
        "tomatoes": 1.2,
        "beer": 0.5,
        "wine": 0.25,
        "tea": 2.0,
        "coffee": 1.0,
        "dark_yellow_vegetables": 0.5,
        "leafy_green_vegetables": 1.5,
        "snacks": 1.0,
        "fruit_juice": 0.75,
        "pizza": 0.1,
    }
    result = compute_edii(data=None, respondent_id=[1], **{k: [v] for k, v in values.items()})
    expected = (
        165.03 * values["processed_meat"]
        + 140.19 * values["red_meat"]
        + 144.61 * values["organ_meat"]
        + 252.45 * values["other_fish"]
        + 136.14 * values["other_vegetables"]
        + 81.21 * values["refined_grains"]
        + 156.85 * values["high_energy_beverages"]
        + 94.77 * values["low_energy_beverages"]
        + 167.92 * values["tomatoes"]
        - 136.99 * values["beer"]
        - 249.70 * values["wine"]
        - 42.25 * values["tea"]
        - 83.18 * values["coffee"]
        - 165.37 * values["dark_yellow_vegetables"]
        - 190.29 * values["leafy_green_vegetables"]
        - 45.08 * values["snacks"]
        - 58.95 * values["fruit_juice"]
        - 1175.21 * values["pizza"]
    ) / 1000.0
    assert abs(result.loc[0, "EDII_ALL"] - expected) < 1e-9


def test_china_dii_is_zero_at_published_reference_means():
    result = compute_china_dii(
        data=None,
        respondent_id=[1],
        KCAL=[1869.00],
        PROTEIN=[65.66],
        CARB=[271.00],
        TOTALFAT=[64.14],
        CHOLES=[328.19],
        SATFAT=[18.42],
        MUFA=[30.74],
        PUFA=[19.04],
        FIBER=[12.42],
        FOLICACID=[139.20],
        VITA=[376.13],
        THIAMIN=[0.92],
        RIBOFLAVIN=[0.81],
        NIACIN=[13.31],
        VITB6=[0.51],
        VITB12=[0.98],
        VITC=[80.35],
        VITD=[3.74],
        VITE=[26.31],
        ZN=[9.67],
        MG=[280.13],
        IRON=[19.01],
        SE=[42.91],
    )
    assert abs(result.loc[0, "CHINADII_ALL"]) < 1e-12


def test_china_dii_matches_centered_percentile_formula_for_shifted_components():
    centered_percentile_at_one_sd = norm.cdf(1.0) * 2.0 - 1.0
    result = compute_china_dii(
        data=None,
        respondent_id=[1],
        KCAL=[1869.00],
        PROTEIN=[65.66 + 21.09],
        CARB=[271.00 + 91.51],
        TOTALFAT=[64.14],
        CHOLES=[328.19],
        SATFAT=[18.42],
        MUFA=[30.74],
        PUFA=[19.04],
        FIBER=[12.42 - 5.88],
        FOLICACID=[139.20],
        VITA=[376.13],
        THIAMIN=[0.92],
        RIBOFLAVIN=[0.81],
        NIACIN=[13.31],
        VITB6=[0.51],
        VITB12=[0.98],
        VITC=[80.35],
        VITD=[3.74],
        VITE=[26.31],
        ZN=[9.67],
        MG=[280.13],
        IRON=[19.01],
        SE=[42.91],
    )
    expected = centered_percentile_at_one_sd * 0.021
    expected += centered_percentile_at_one_sd * 0.097
    expected += (-centered_percentile_at_one_sd) * (-0.663)
    assert abs(result.loc[0, "CHINADII_ALL"] - expected) < 1e-9


if __name__ == "__main__":
    tests = [
        test_mind_reaches_full_score_when_all_targets_are_met,
        test_chei_can_reach_full_score_with_target_density_inputs,
        test_dqii_can_reach_full_score_when_all_domains_hit_targets,
        test_dbi_hits_zero_imbalance_at_reference_targets,
        test_gdqs_reaches_full_score_with_maximizing_pattern,
        test_wish_reaches_full_score_with_target_pattern,
        test_nutrient_density_family_returns_expected_reference_scores,
        test_pral_and_neap_match_hand_calculated_formulae,
        test_cdai_returns_zero_for_row_at_sample_means,
        test_obs_can_reach_full_score_for_top_profile_within_each_sex,
        test_edii_matches_published_weighted_sum_formula,
        test_china_dii_is_zero_at_published_reference_means,
        test_china_dii_matches_centered_percentile_formula_for_shifted_components,
    ]
    passed = 0
    for fn in tests:
        fn()
        passed += 1
        print(f"[PASS] {fn.__name__}")
    print(f"Phase 2-4 tests: {passed}/{len(tests)} passed")
