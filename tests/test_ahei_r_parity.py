import numpy as np
import pandas as pd

from dietaryindex.adapters.nhanes_fped_ind import compute_ahei_nhanes_fped
from dietaryindex.core.ahei import compute_ahei


def test_compute_ahei_drops_trans_component_when_all_missing():
    data = pd.DataFrame({"id": [1, 2]})
    result = compute_ahei(
        data=data,
        respondent_id=data["id"],
        gender=np.array([1, 2]),
        total_kcal=np.array([2000.0, 1800.0]),
        vegetable=np.array([2.0, 3.0]),
        fruit=np.array([1.0, 2.0]),
        whole_grain=np.array([40.0, 50.0]),
        nut_legume=np.array([0.5, 1.0]),
        n3_fat=np.array([100.0, 120.0]),
        pufa=np.array([6.0, 7.0]),
        ssb_fruit_juice=np.array([0.2, 0.1]),
        red_processed_meat=np.array([0.5, 0.3]),
        trans_fat=np.array([np.nan, np.nan]),
        sodium=np.array([1800.0, 1600.0]),
        alcohol=np.array([1.0, 0.8]),
    )

    assert result["AHEI_TRANS"].isna().all()

    expected = (
        result["AHEI_VEG"]
        + result["AHEI_FRT"]
        + result["AHEI_WGRAIN"]
        + result["AHEI_NUTSLEG"]
        + result["AHEI_N3FAT"]
        + result["AHEI_PUFA"]
        + result["AHEI_SSB_FRTJ"]
        + result["AHEI_REDPROC_MEAT"]
        + result["AHEI_SODIUM"]
        + result["AHEI_ALCOHOL"]
    )
    np.testing.assert_allclose(result["AHEI_ALL"], expected)


def test_compute_ahei_nhanes_fped_uses_missing_trans_component_not_zero():
    fped_iff = pd.DataFrame(
        {
            "SEQN": [1, 1, 2, 2],
            "DR1ILINE": [1, 2, 1, 2],
            "DR1IFDCD": [100, 92410310, 100, 92410310],
            "V_TOTAL": [1.0, 0.0, 2.0, 0.0],
            "F_TOTAL": [0.5, 1.0, 0.5, 0.0],
            "G_WHOLE": [20.0, 0.0, 30.0, 0.0],
            "PF_NUTSDS": [0.2, 0.0, 0.4, 0.0],
            "PF_LEGUMES": [0.3, 0.0, 0.1, 0.0],
            "PF_SOY": [0.0, 0.0, 0.0, 0.0],
            "PF_MEAT": [0.4, 0.0, 0.2, 0.0],
            "PF_CUREDMEAT": [0.1, 0.0, 0.1, 0.0],
            "PF_ORGAN": [0.0, 0.0, 0.0, 0.0],
            "V_POTATO": [0.0, 0.0, 0.0, 0.0],
            "F_NJ_TOTAL": [0.5, 1.0, 0.5, 0.0],
            "ADD_SUGARS": [0.0, 6.5, 0.0, 6.5],
            "A_DRINKS": [0.5, 0.0, 0.2, 0.0],
        }
    )
    nutrient_iff = pd.DataFrame(
        {
            "SEQN": [1, 1, 2, 2],
            "DR1ILINE": [1, 2, 1, 2],
            "DR1IKCAL": [1000.0, 900.0, 1200.0, 1000.0],
            "DR1ISODI": [800.0, 700.0, 900.0, 850.0],
            "DR1IALCO": [0.5, 0.0, 0.2, 0.0],
            "DR1IPFAT": [5.0, 4.0, 6.0, 5.0],
            "DR1IP182": [4.0, 3.0, 5.0, 4.0],
            "DR1IP183": [0.5, 0.4, 0.6, 0.5],
            "DR1IP184": [0.0, 0.0, 0.0, 0.0],
            "DR1IP204": [0.0, 0.0, 0.0, 0.0],
            "DR1IP205": [0.05, 0.04, 0.06, 0.05],
            "DR1IP225": [0.0, 0.0, 0.0, 0.0],
            "DR1IP226": [0.08, 0.07, 0.09, 0.08],
        }
    )
    demo = pd.DataFrame({"SEQN": [1, 2], "RIAGENDR": [1, 2]})

    result = compute_ahei_nhanes_fped(
        fped_ind_path=fped_iff,
        nutrient_ind_path=nutrient_iff,
        demo_path=demo,
    )

    assert result["AHEI_TRANS"].isna().all()
    assert result["AHEI_ALL"].notna().all()
