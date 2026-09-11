import pandas as pd


def _assert_scores(result, column, expected):
    actual = dict(zip(result["SEQN"].astype(int), result[column].astype(float)))
    assert actual == expected


def test_di_gm_nhanes_fped_iff_scores_special_foods_and_nutrients():
    from dietaryindex import compute_di_gm_nhanes_fped

    nutrient = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "DR1ILINE": [1, 1, 1, 1],
            "DR1DRSTZ": [1, 1, 1, 1],
            "DR1IFDCD": [63105010, 99999999, 63105010, 99999999],
            "DR1IGRMS": [100.0, 0.0, 80.0, 0.0],
            "DR1IKCAL": [2000.0, 2000.0, 2000.0, 2000.0],
            "DR1IFIBE": [30.0, 5.0, 25.0, 5.0],
            "DR1ITFAT": [10.0, 100.0, 10.0, 100.0],
        }
    )
    fped = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "RIAGENDR": [2, 2, 1, 1],
            "DR1ILINE": [1, 1, 1, 1],
            "DR1IFDCD": [63105010, 99999999, 63105010, 99999999],
            "DR1IGRMS": [100.0, 0.0, 80.0, 0.0],
            "DR1I_G_WHOLE": [0.0, 0.0, 0.0, 0.0],
            "DR1I_G_REFINED": [0.0, 0.0, 0.0, 0.0],
            "DR1I_PF_CUREDMEAT": [0.0, 0.0, 0.0, 0.0],
            "DR1I_PF_MEAT": [0.0, 0.0, 0.0, 0.0],
        }
    )

    result = compute_di_gm_nhanes_fped(fped_ind_path=fped, nutrient_ind_path=nutrient)

    _assert_scores(result, "DI_GM_AVOCADO", {1: 1.0, 2: 0.0, 3: 1.0, 4: 0.0})
    _assert_scores(result, "DI_GM_FIBER", {1: 1.0, 2: 0.0, 3: 1.0, 4: 0.0})
    _assert_scores(result, "DI_GM_TOTAL_FAT_PERCENTAGE", {1: 1.0, 2: 0.0, 3: 1.0, 4: 0.0})
    assert result["DI_GM_TOTAL"].between(0, 14).all()


def test_di_gm_nhanes_fped_defaults_to_intake_average_before_scoring():
    from dietaryindex import compute_di_gm_nhanes_fped

    nutrient1 = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "DR1ILINE": [1, 1, 1, 1],
            "DR1DRSTZ": [1, 1, 1, 1],
            "DR1IFDCD": [63105010, 99999999, 63105010, 99999999],
            "DR1IGRMS": [100.0, 0.0, 80.0, 0.0],
            "DR1IKCAL": [2000.0, 2000.0, 2000.0, 2000.0],
            "DR1IFIBE": [30.0, 5.0, 25.0, 5.0],
            "DR1ITFAT": [10.0, 100.0, 10.0, 100.0],
        }
    )
    fped1 = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "RIAGENDR": [2, 2, 1, 1],
            "DR1ILINE": [1, 1, 1, 1],
            "DR1IFDCD": [63105010, 99999999, 63105010, 99999999],
            "DR1IGRMS": [100.0, 0.0, 80.0, 0.0],
            "DR1I_G_WHOLE": [0.0, 0.0, 0.0, 0.0],
            "DR1I_G_REFINED": [0.0, 0.0, 0.0, 0.0],
            "DR1I_PF_CUREDMEAT": [0.0, 0.0, 0.0, 0.0],
            "DR1I_PF_MEAT": [0.0, 0.0, 0.0, 0.0],
        }
    )
    nutrient2 = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "DR2ILINE": [1, 1, 1, 1],
            "DR2DRSTZ": [1, 1, 1, 1],
            "DR2IFDCD": [99999999, 63105010, 99999999, 63105010],
            "DR2IGRMS": [0.0, 100.0, 0.0, 80.0],
            "DR2IKCAL": [2000.0, 2000.0, 2000.0, 2000.0],
            "DR2IFIBE": [5.0, 30.0, 5.0, 25.0],
            "DR2ITFAT": [100.0, 10.0, 100.0, 10.0],
        }
    )
    fped2 = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "RIAGENDR": [2, 2, 1, 1],
            "DR2ILINE": [1, 1, 1, 1],
            "DR2IFDCD": [99999999, 63105010, 99999999, 63105010],
            "DR2IGRMS": [0.0, 100.0, 0.0, 80.0],
            "DR2I_G_WHOLE": [0.0, 0.0, 0.0, 0.0],
            "DR2I_G_REFINED": [0.0, 0.0, 0.0, 0.0],
            "DR2I_PF_CUREDMEAT": [0.0, 0.0, 0.0, 0.0],
            "DR2I_PF_MEAT": [0.0, 0.0, 0.0, 0.0],
        }
    )

    intake_average = compute_di_gm_nhanes_fped(
        fped_ind_path=fped1,
        nutrient_ind_path=nutrient1,
        fped_ind_path2=fped2,
        nutrient_ind_path2=nutrient2,
    )
    score_average = compute_di_gm_nhanes_fped(
        fped_ind_path=fped1,
        nutrient_ind_path=nutrient1,
        fped_ind_path2=fped2,
        nutrient_ind_path2=nutrient2,
        two_day_method="score_average",
    )

    _assert_scores(intake_average, "DI_GM_AVOCADO", {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0})
    _assert_scores(score_average, "DI_GM_AVOCADO", {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5})


def test_di_gm_nhanes_mped_scores_special_foods_fiber_and_total_fat():
    from dietaryindex import compute_di_gm_nhanes_mped

    equiv = pd.DataFrame(
        {
            "DRDIFDCD": [63105010, 99999999],
            "G_WHL": [0.0, 0.0],
            "G_NWHL": [0.0, 0.0],
            "M_FRANK": [0.0, 0.0],
            "M_MEAT": [0.0, 0.0],
        }
    )
    nutrient_ind = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "DRDIFDCD": [63105010, 99999999, 63105010, 99999999],
            "DRXIGRMS": [100.0, 0.0, 80.0, 0.0],
            "DRXIKCAL": [2000.0, 2000.0, 2000.0, 2000.0],
            "DRXIFIBE": [30.0, 5.0, 25.0, 5.0],
            "DRXITFAT": [10.0, 100.0, 10.0, 100.0],
        }
    )
    demo = pd.DataFrame({"SEQN": [1, 2, 3, 4], "RIAGENDR": [2, 2, 1, 1]})

    result = compute_di_gm_nhanes_mped(
        mped_per_100_gram_path=equiv,
        nutrient_ind_path=nutrient_ind,
        demo_path=demo,
    )

    _assert_scores(result, "DI_GM_AVOCADO", {1: 1.0, 2: 0.0, 3: 1.0, 4: 0.0})
    _assert_scores(result, "DI_GM_FIBER", {1: 1.0, 2: 0.0, 3: 1.0, 4: 0.0})
    _assert_scores(result, "DI_GM_TOTAL_FAT_PERCENTAGE", {1: 1.0, 2: 0.0, 3: 1.0, 4: 0.0})
    assert result["DI_GM_TOTAL"].between(0, 14).all()


def test_di_gm_nhanes_mped_defaults_to_intake_average_before_scoring():
    from dietaryindex import compute_di_gm_nhanes_mped

    equiv = pd.DataFrame(
        {
            "DRDIFDCD": [63105010, 99999999],
            "G_WHL": [0.0, 0.0],
            "G_NWHL": [0.0, 0.0],
            "M_FRANK": [0.0, 0.0],
            "M_MEAT": [0.0, 0.0],
        }
    )
    day1 = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "DRDIFDCD": [63105010, 99999999, 63105010, 99999999],
            "DRXIGRMS": [100.0, 0.0, 80.0, 0.0],
            "DRXIKCAL": [2000.0, 2000.0, 2000.0, 2000.0],
            "DRXIFIBE": [30.0, 5.0, 25.0, 5.0],
            "DRXITFAT": [10.0, 100.0, 10.0, 100.0],
        }
    )
    day2 = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "DRDIFDCD": [99999999, 63105010, 99999999, 63105010],
            "DRXIGRMS": [0.0, 100.0, 0.0, 80.0],
            "DRXIKCAL": [2000.0, 2000.0, 2000.0, 2000.0],
            "DRXIFIBE": [5.0, 30.0, 5.0, 25.0],
            "DRXITFAT": [100.0, 10.0, 100.0, 10.0],
        }
    )
    demo = pd.DataFrame({"SEQN": [1, 2, 3, 4], "RIAGENDR": [2, 2, 1, 1]})

    result = compute_di_gm_nhanes_mped(
        mped_per_100_gram_path=equiv,
        nutrient_ind_path=day1,
        nutrient_ind_path2=day2,
        demo_path=demo,
    )

    _assert_scores(result, "DI_GM_AVOCADO", {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0})
    _assert_scores(result, "DI_GM_FIBER", {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0})
    _assert_scores(result, "DI_GM_TOTAL_FAT_PERCENTAGE", {1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0})


def test_di_gm_nhanes_mped_can_score_each_day_before_averaging_for_r_parity():
    from dietaryindex import compute_di_gm_nhanes_mped

    equiv = pd.DataFrame(
        {
            "DRDIFDCD": [63105010, 99999999],
            "G_WHL": [0.0, 0.0],
            "G_NWHL": [0.0, 0.0],
            "M_FRANK": [0.0, 0.0],
            "M_MEAT": [0.0, 0.0],
        }
    )
    day1 = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "DRDIFDCD": [63105010, 99999999, 63105010, 99999999],
            "DRXIGRMS": [100.0, 0.0, 80.0, 0.0],
            "DRXIKCAL": [2000.0, 2000.0, 2000.0, 2000.0],
            "DRXIFIBE": [30.0, 5.0, 25.0, 5.0],
            "DRXITFAT": [10.0, 100.0, 10.0, 100.0],
        }
    )
    day2 = pd.DataFrame(
        {
            "SEQN": [1, 2, 3, 4],
            "DRDIFDCD": [99999999, 63105010, 99999999, 63105010],
            "DRXIGRMS": [0.0, 100.0, 0.0, 80.0],
            "DRXIKCAL": [2000.0, 2000.0, 2000.0, 2000.0],
            "DRXIFIBE": [5.0, 30.0, 5.0, 25.0],
            "DRXITFAT": [100.0, 10.0, 100.0, 10.0],
        }
    )
    demo = pd.DataFrame({"SEQN": [1, 2, 3, 4], "RIAGENDR": [2, 2, 1, 1]})

    result = compute_di_gm_nhanes_mped(
        mped_per_100_gram_path=equiv,
        nutrient_ind_path=day1,
        nutrient_ind_path2=day2,
        demo_path=demo,
        two_day_method="score_average",
    )

    _assert_scores(result, "DI_GM_AVOCADO", {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5})
    _assert_scores(result, "DI_GM_FIBER", {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5})
    _assert_scores(result, "DI_GM_TOTAL_FAT_PERCENTAGE", {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5})


if __name__ == "__main__":
    test_di_gm_nhanes_fped_iff_scores_special_foods_and_nutrients()
    test_di_gm_nhanes_fped_defaults_to_intake_average_before_scoring()
    test_di_gm_nhanes_mped_scores_special_foods_fiber_and_total_fat()
    test_di_gm_nhanes_mped_defaults_to_intake_average_before_scoring()
    test_di_gm_nhanes_mped_can_score_each_day_before_averaging_for_r_parity()
    print("DI-GM adapter tests passed")
