import numpy as np
import pandas as pd

from dietaryindex import (
    compute_phdi_nhanes_fped,
    compute_phdi_nhanes_mped,
    compute_phdi_asa24,
    compute_phdi_dhq3,
    compute_phdi_block,
)


def _synthetic_phdi_inputs():
    demo = pd.DataFrame(
        {
            "SEQN": [1, 2],
            "RIAGENDR": [2, 1],
            "RIDAGEYR": [44, 19],
        }
    )
    nutrient = pd.DataFrame(
        {
            "SEQN": [1, 2],
            "DR1DRSTZ": [1, 1],
            "DR1TKCAL": [2000.0, 2000.0],
            "DR1TSFAT": [10.0, 10.0],
            "DR1TMFAT": [20.0, 20.0],
            "DR1TPFAT": [10.0, 10.0],
            "DR1TSUGR": [0.0, 0.0],
        }
    )
    fped = pd.DataFrame(
        {
            "SEQN": [1, 2],
            "DR1T_G_WHOLE": [75.0 / 16.0, 75.0 / 16.0],
            "DR1T_F_CITMLB": [0.0, 0.0],
            "DR1T_F_OTHER": [200.0 / 150.0, 200.0 / 150.0],
            "DR1T_F_JUICE": [0.0, 0.0],
            "DR1T_V_TOTAL": [300.0 / 150.0 + 50.0 / 150.0, 1.0],
            "DR1T_V_STARCHY_TOTAL": [50.0 / 150.0, 0.0],
            "DR1T_V_LEGUMES": [0.0, 0.0],
            "DR1T_D_TOTAL": [250.0 / 245.0, 0.0],
            "DR1T_PF_MEAT": [14.0 / 28.35, 0.0],
            "DR1T_PF_CUREDMEAT": [0.0, 0.0],
            "DR1T_PF_ORGAN": [0.0, 0.0],
            "DR1T_PF_POULT": [29.0 / 28.35, 0.0],
            "DR1T_PF_EGGS": [12.0 / 28.35, 0.0],
            "DR1T_PF_SEAFD_HI": [15.0 / 28.35, 0.0],
            "DR1T_PF_SEAFD_LOW": [0.0, 0.0],
            "DR1T_PF_LEGUMES": [100.0 / 28.35, 0.0],
            "DR1T_PF_SOY": [50.0 / 28.35, 0.0],
            "DR1T_PF_NUTSDS": [50.0 / 28.35, 0.0],
            "DR1T_OILS": [0.0, 0.0],
            "DR1T_SOLID_FATS": [5.0, 5.0],
            "DR1T_ADD_SUGARS": [0.0, 0.0],
        }
    )
    return fped, nutrient, demo


def test_compute_phdi_nhanes_fped_synthetic_max_score():
    fped, nutrient, demo = _synthetic_phdi_inputs()
    out = compute_phdi_nhanes_fped(
        fped_path=fped,
        nutrient_path=nutrient,
        demo_path=demo,
    )

    assert out["SEQN"].tolist() == [1]
    assert np.isclose(out.loc[0, "PHDI_ALL"], 140.0)
    assert np.isclose(out.loc[0, "PHDI_140_RECONSTRUCTED"], 140.0)
    assert out.loc[0, "PHDI_LEGUMES"] == 5.0
    assert out.loc[0, "PHDI_SOY"] == 5.0


def test_compute_phdi_nhanes_mped_synthetic_max_score():
    demo = pd.DataFrame(
        {
            "SEQN": [1, 2],
            "RIAGENDR": [2, 1],
            "RIDAGEYR": [44, 19],
        }
    )
    nutrient = pd.DataFrame(
        {
            "SEQN": [1, 2],
            "DR1DRSTZ": [1, 1],
            "DR1TKCAL": [2000.0, 2000.0],
            "DR1TSFAT": [10.0, 10.0],
            "DR1TMFAT": [20.0, 20.0],
            "DR1TPFAT": [10.0, 10.0],
            "DR1TSUGR": [0.0, 0.0],
        }
    )
    pyramid = pd.DataFrame(
        {
            "SEQN": [1, 2],
            "G_TOTAL": [8.0, 8.0],
            "G_WHL": [75.0 / 16.0, 75.0 / 16.0],
            "F_CITMLB": [0.0, 0.0],
            "F_OTHER": [200.0 / 150.0, 200.0 / 150.0],
            "V_TOTAL": [300.0 / 150.0 + 50.0 / 150.0 + 100.0 / 28.35, 1.0],
            "V_STARCY": [50.0 / 150.0, 0.0],
            "D_TOTAL": [250.0 / 245.0, 0.0],
            "M_MEAT": [14.0 / 28.35, 0.0],
            "M_FRANK": [0.0, 0.0],
            "M_ORGAN": [0.0, 0.0],
            "M_POULT": [29.0 / 28.35, 0.0],
            "M_EGG": [12.0 / 28.35, 0.0],
            "M_FISH_HI": [15.0 / 28.35, 0.0],
            "M_FISH_LO": [0.0, 0.0],
            "LEGUMES": [100.0 / 28.35, 0.0],
            "M_SOY": [50.0 / 28.35, 0.0],
            "M_NUTSD": [50.0 / 28.35, 0.0],
            "DISCFAT_OIL": [0.0, 0.0],
            "DISCFAT_SOL": [5.0, 5.0],
            "ADD_SUG": [0.0, 0.0],
        }
    )

    out = compute_phdi_nhanes_mped(
        pyramid_path=pyramid,
        nutrient_path=nutrient,
        demo_path=demo,
    )

    assert out["SEQN"].tolist() == [1]
    assert np.isclose(out.loc[0, "PHDI_ALL"], 140.0)
    assert np.isclose(out.loc[0, "PHDI_140_RECONSTRUCTED"], 140.0)
    assert out.loc[0, "PHDI_LEGUMES"] == 5.0
    assert out.loc[0, "PHDI_SOY"] == 5.0


def _synthetic_questionnaire_phdi_inputs():
    return pd.DataFrame(
        {
            "Respondent ID": [1, 2],
            "Sex": [2, 1],
            "Age": [44, 19],
            "Energy (kcal)": [2000.0, 2000.0],
            "Whole grain oz": [75.0 / 16.0, 0.0],
            "Total fruit cups": [200.0 / 150.0, 0.0],
            "Fruit juice cups": [0.0, 0.0],
            "Total vegetable cups": [(300.0 + 50.0 + 100.0) / 150.0, 0.0],
            "Starchy vegetable cups": [50.0 / 150.0, 0.0],
            "Dairy cups": [250.0 / 245.0, 0.0],
            "Red meat oz": [14.0 / 28.35, 0.0],
            "Poultry oz": [29.0 / 28.35, 0.0],
            "Eggs oz": [12.0 / 28.35, 0.0],
            "Fish oz": [15.0 / 28.35, 0.0],
            "Legumes oz": [100.0 / 28.35, 0.0],
            "Soy oz": [50.0 / 28.35, 0.0],
            "Nuts oz": [50.0 / 28.35, 0.0],
            "Added sugars g": [0.0, 0.0],
            "Saturated fat g": [10.0, 10.0],
            "Solid fats g": [5.0, 5.0],
            "Monounsaturated fat g": [20.0, 20.0],
            "Polyunsaturated fat g": [10.0, 10.0],
        }
    )


def test_compute_phdi_questionnaire_synthetic_max_score():
    data = _synthetic_questionnaire_phdi_inputs()
    for func in [compute_phdi_asa24, compute_phdi_dhq3, compute_phdi_block]:
        out = func(data)
        assert out["SEQN"].tolist() == [1, 2]
        assert np.isclose(out.loc[0, "PHDI_ALL"], 140.0)
        assert np.isclose(out.loc[0, "PHDI_140_RECONSTRUCTED"], 140.0)
        assert out.loc[0, "PHDI_LEGUMES"] == 5.0
        assert out.loc[0, "PHDI_SOY"] == 5.0


def run_all():
    tests = [
        test_compute_phdi_nhanes_fped_synthetic_max_score,
        test_compute_phdi_nhanes_mped_synthetic_max_score,
        test_compute_phdi_questionnaire_synthetic_max_score,
    ]
    passed = 0
    for test in tests:
        try:
            test()
            print(f"[PASS] {test.__name__}")
            passed += 1
        except Exception as exc:
            print(f"[FAIL] {test.__name__}: {type(exc).__name__}: {exc}")
            raise
    print(f"PHDI NHANES tests: {passed}/{len(tests)} passed")


if __name__ == "__main__":
    run_all()
