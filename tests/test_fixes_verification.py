"""Verification unit tests for the 8 confirmed bug fixes."""

import numpy as np
import pandas as pd
import pytest

from dietaryindex import (
    compute_hei2020,
    compute_hei2015,
    compute_dqii,
    compute_chei,
    compute_cdai,
    compute_mind,
    compute_dii,
    compute_china_dii,
    compute_edii,
    compute_pral,
    compute_medi,
    compute_medi_v2,
)
from dietaryindex.core.hei2020 import _compute_hei2020_core
from dietaryindex.reference.index_params import INDEX_PARAMS
from dietaryindex.service.compute import GENERAL_FUNCTION_MAP


def test_issue_1_function_map_registration():
    """Issue 1: PHDI_V2, MEDI_V2, ACS2020_V2 registered in GENERAL_FUNCTION_MAP."""
    assert "compute_medi_v2" in GENERAL_FUNCTION_MAP
    assert "compute_acs2020_v2" in GENERAL_FUNCTION_MAP
    assert "compute_phdi_v2" in GENERAL_FUNCTION_MAP

    for key in ["PHDI_V2", "MEDI_V2", "ACS2020_V2"]:
        cfg = INDEX_PARAMS[key]
        assert cfg["function"] in GENERAL_FUNCTION_MAP


def test_issue_2_hei2020_v1_sodium_scoring():
    """HEI2020 V1 accepts total g/day and converts to g/1000 kcal like R 2.1."""
    res = _compute_hei2020_core(
        age=[30],
        total_kcal=[2000],
        total_fruit=[1.0], whole_fruit=[0.5],
        total_vegetable=[1.5], green_and_bean=[0.3],
        total_protein=[3.0], seafood_plant_protein=[1.0],
        whole_grain=[2.0], dairy=[1.5], fatty_acid=[3.0],
        refined_grain=[2.0], sodium=[3.0], added_sugar=[5.0], saturated_fat=[7.0],
        version="v1",
    )
    score_na = res["HEI2020_SODIUM"][0]
    expected = 10.0 * (2.0 - 1.5) / (2.0 - 1.1)
    assert np.isclose(score_na, expected, atol=1e-3)


def test_hei2020_age_below_one_matches_r_missing_state():
    result = _compute_hei2020_core(
        age=[0.5],
        total_kcal=[1000],
        total_fruit=[1], whole_fruit=[1],
        total_vegetable=[1], green_and_bean=[1],
        total_protein=[1], seafood_plant_protein=[1],
        whole_grain=[1], dairy=[1], fatty_acid=[1],
        refined_grain=[1], sodium=[1], added_sugar=[1], saturated_fat=[1],
        version="v1",
    )
    assert np.isnan(result["HEI2020_ALL"][0])
    assert np.isnan(result["HEI2020_SODIUM"][0])


def test_issue_3_dqii_protein_variety_tiers():
    """Issue 3: DQI-I protein source variety >=3 -> 5.0 pts, 2 -> 3.0 pts, 1 -> 1.0 pt."""
    df = pd.DataFrame({
        "id": [1, 2],
        "age": [30, 30],
        "gender": [1, 1],
        "total_kcal": [2000, 2000],
        "grain": [1, 1],
        "vegetable": [1, 1],
        "fruit": [1, 1],
        "meat": [1, 1],
        "poultry": [1, 1],
        "fish": [1, 0],
        "dairy": [0, 0],
        "legumes": [0, 0],
        "egg": [0, 0],
        "fiber": [np.nan, 20],
        "protein": [60, 60],
        "iron": [15, 15],
        "calcium": [800, 800],
        "vitamin_c": [100, 100],
        "carbohydrate": [250, 250],
        "total_fat": [60, 60],
        "saturated_fat": [20, 20],
        "mufa": [20, 20],
        "pufa": [15, 15],
        "cholesterol": [200, 200],
        "sodium": [2000, 2000],
        "empty_calorie_pct_energy": [10, 10],
    })
    res = compute_dqii(
        df,
        df["id"],
        df["age"],
        df["gender"],
        df["total_kcal"],
        df["grain"],
        df["vegetable"],
        df["fruit"],
        df["meat"],
        df["poultry"],
        df["fish"],
        df["dairy"],
        df["legumes"],
        df["egg"],
        df["fiber"],
        df["protein"],
        df["iron"],
        df["calcium"],
        df["vitamin_c"],
        df["carbohydrate"],
        df["total_fat"],
        df["saturated_fat"],
        df["mufa"],
        df["pufa"],
        df["cholesterol"],
        df["sodium"],
        df["empty_calorie_pct_energy"],
    )
    # Row 0 has 3 sources (meat, poultry, fish) -> 5.0 pts
    assert res["DQII_VAR_PROTEIN"].iloc[0] == 5.0
    # Row 1 has 2 sources (meat, poultry) -> 3.0 pts
    assert res["DQII_VAR_PROTEIN"].iloc[1] == 3.0
    assert pd.isna(res["DQII_ALL"].iloc[0])


def test_issue_4_missing_value_handling():
    """Issue 4: Verify NaN propagation for MIND, DII, CHINA-DII, EDII, and PRAL."""
    # MIND all NaN
    mind_res = compute_mind(
        data=None,
        respondent_id=[1],
        green_leafy_vegetables=[1.0],
        other_vegetables=[np.nan],
        nuts=[np.nan],
        berries=[np.nan],
        beans=[np.nan],
        whole_grains=[np.nan],
        fish=[np.nan],
        poultry=[np.nan],
        olive_oil_primary=[np.nan],
        wine=[np.nan],
        red_meats=[np.nan],
        butter_margarine=[np.nan],
        cheese=[np.nan],
        pastries_sweets=[np.nan],
        fried_fast_food=[np.nan],
    )
    assert pd.isna(mind_res["MIND_ALL"].iloc[0])

    # DII all NaN
    dii_df = pd.DataFrame({"RESPONDENTID": [1], "ALCOHOL": [np.nan], "FIBER": [np.nan]})
    dii_res = compute_dii(
        data=dii_df,
        respondent_id="RESPONDENTID",
        ALCOHOL=dii_df["ALCOHOL"],
        FIBER=dii_df["FIBER"],
    )
    assert pd.isna(dii_res["DII_ALL"].iloc[0])
    assert dii_res["Components_Used"].iloc[0] == 0

    # CHINA-DII all NaN
    china_df = pd.DataFrame({"RESPONDENTID": [1], "ENERGY": [np.nan]})
    china_res = compute_china_dii(
        data=china_df,
        respondent_id="RESPONDENTID",
        KCAL=china_df["ENERGY"],
    )
    assert pd.isna(china_res["CHINADII_ALL"].iloc[0])
    assert china_res["Components_Used"].iloc[0] == 0
    assert pd.isna(china_res["CHINADII_KCAL"].iloc[0])

    # EDII all NaN
    edii_res = compute_edii(
        data=None,
        respondent_id=[1],
        processed_meat=[1.0],
        red_meat=[np.nan],
        organ_meat=[np.nan],
        other_fish=[np.nan],
        other_vegetables=[np.nan],
        refined_grains=[np.nan],
        high_energy_beverages=[np.nan],
        low_energy_beverages=[np.nan],
        tomatoes=[np.nan],
        beer=[np.nan],
        wine=[np.nan],
        tea=[np.nan],
        coffee=[np.nan],
        dark_yellow_vegetables=[np.nan],
        leafy_green_vegetables=[np.nan],
        snacks=[np.nan],
        fruit_juice=[np.nan],
        pizza=[np.nan],
    )
    assert pd.isna(edii_res["EDII_ALL"].iloc[0])

    # PRAL missing nutrient
    pral_res = compute_pral(
        data=None,
        respondent_id=[1],
        protein=[50.0],
        phosphorus=[800.0],
        potassium=[2000.0],
        magnesium=[np.nan],  # missing magnesium
        calcium=[600.0],
    )
    assert pd.isna(pral_res["PRAL_ALL"].iloc[0])


def test_fixed_component_scores_reject_partial_rows():
    """CHEI and CDAI totals require their complete published component panels."""
    one = [1.0]
    chei = compute_chei(
        data=None, respondent_id=[1], gender=[1], total_grains=one,
        whole_grains_mixed_beans=one, tubers=one, total_vegetables=one,
        dark_vegetables=one, fruits=one, dairy=one, soybeans=one,
        fish_seafood=one, poultry=one, eggs=one, seeds_nuts=one,
        red_meat=one, cooking_oils=one, sodium=[np.nan],
        added_sugars_pct_energy=one, alcohol=one,
    )
    assert pd.isna(chei["CHEI_ALL"].iloc[0])

    cdai = compute_cdai(
        data=None, respondent_id=[1, 2], zinc=[1.0, 2.0], selenium=[1.0, 2.0],
        total_carotenoids=[1.0, 2.0], vitamin_a=[1.0, 2.0],
        vitamin_c=[np.nan, 2.0], vitamin_e=[1.0, 2.0],
    )
    assert pd.isna(cdai["CDAI_ALL"].iloc[0])


def test_issue_5_acs2020_max_score():
    """Issue 5: ACS2020 max score in params config is 12."""
    assert INDEX_PARAMS["ACS2020"]["max_score"] == 12
    assert INDEX_PARAMS["ACS2020_V1"]["max_score"] == 12
    assert INDEX_PARAMS["ACS2020_V2"]["max_score"] == 12


def test_issue_6_medi_olive_oil_in_noetoh():
    """MEDI NOETOH fields preserve the Dietaryindex R 2.1 definition."""
    res_v1 = compute_medi(
        data=None,
        respondent_id=[1],
        olive_oil=[5],
        fruit=[3],
        vegetable=[2],
        legumes=[1],
        nuts=[1],
        fish_seafood=[1],
        alcohol=[10],
        ssb=[0],
        sweets=[0],
        discret_fat=[0],
        red_processed_meat=[0],
    )
    assert res_v1["MEDI_OLIVE_OIL"].iloc[0] == 1
    assert res_v1["MEDI_ALL"].iloc[0] == 11
    assert res_v1["MEDI_NOETOH"].iloc[0] == 9  # R 2.1 excludes alcohol and olive oil

    res_v2 = compute_medi_v2(
        data=None,
        respondent_id=[1],
        olive_oil=[4],
        fruit=[3],
        vegetable=[2],
        legumes=[1],
        nuts=[1],
        fish_seafood=[1],
        alcohol=[10],
        ssb=[0],
        sweets=[0],
        discret_fat=[0],
        red_processed_meat=[0],
    )
    assert res_v2["MEDI_V2_NOETOH"].iloc[0] == 45.0


def test_issue_7_hei_zero_energy():
    """Issue 7: Zero total energy zeroes out all subscores including sodium and sat fat."""
    res_2020 = _compute_hei2020_core(
        age=[30],
        total_kcal=[0.0],  # 0 energy
        total_fruit=[1.0], whole_fruit=[0.5],
        total_vegetable=[1.5], green_and_bean=[0.3],
        total_protein=[3.0], seafood_plant_protein=[1.0],
        whole_grain=[2.0], dairy=[1.5], fatty_acid=[3.0],
        refined_grain=[2.0], sodium=[1.5], added_sugar=[5.0], saturated_fat=[7.0],
        version="v1",
    )
    assert res_2020["HEI2020_SODIUM"][0] == 0.0
    assert res_2020["HEI2020_SATFAT"][0] == 0.0
    assert res_2020["HEI2020_ALL"][0] == 0.0
