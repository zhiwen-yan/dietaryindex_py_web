from pathlib import Path

import pandas as pd

from dietaryindex.adapters import nhanes_fped_ind as adapter


EXPECTED_CODEBOOK_SIZES = {
    "dash_ssb_fndds_1718_codes.csv": 312,
    "dash_skim_milk_fndds_1718_codes.csv": 7,
    "dash_lowf_cheese_fndds_1718_codes.csv": 4,
    "medi_ssb_fndds_1718_codes.csv": 312,
    "medi_sweets_fndds_1718_codes.csv": 990,
    "medi_fat_oil_fndds_1718_codes.csv": 70,
    "medi_olive_oil_fndds_1718_codes.csv": 1,
    "di_gm_avocado_fndds_1718_codes.csv": 1,
    "di_gm_broccoli_fndds_1718_codes.csv": 15,
    "di_gm_chickpea_fndds_1718_codes.csv": 6,
    "di_gm_coffee_fndds_1718_codes.csv": 110,
    "di_gm_cranberry_fndds_1718_codes.csv": 3,
    "di_gm_fermented_dairy_fndds_1718_codes.csv": 121,
    "di_gm_green_tea_fndds_1718_codes.csv": 14,
    "di_gm_soybean_fndds_1718_codes.csv": 8,
}


def test_vendored_codebooks_are_complete_and_unique():
    data_dir = Path(adapter.__file__).resolve().parents[1] / "data"
    for filename, expected_size in EXPECTED_CODEBOOK_SIZES.items():
        table = pd.read_csv(data_dir / filename)
        assert list(table.columns) == ["code"]
        assert len(table) == expected_size
        assert table["code"].notna().all()
        assert table["code"].is_unique


def test_runtime_defaults_use_vendored_codebooks():
    assert len(adapter._DASH_SSB_CODES_DEFAULT) == 312
    assert len(adapter._SWEETS_CODES_DEFAULT) == 990
    assert len(adapter._FAT_OIL_CODES_DEFAULT) == 70
    assert len(adapter._BROCCOLI_CODES_DEFAULT) == 15
    assert len(adapter._COFFEE_CODES_DEFAULT) == 110
    assert len(adapter._FERMENTED_DAIRY_CODES_DEFAULT) == 121
    assert len(adapter._GREEN_TEA_CODES_DEFAULT) == 14

    # These representatives were absent from the old emergency fallbacks and
    # protect the standalone package from silently changing classifications.
    assert 12200100 in adapter._DASH_SSB_CODES_DEFAULT
    assert 11459990 in adapter._SWEETS_CODES_DEFAULT
    assert 22621100 in adapter._FAT_OIL_CODES_DEFAULT
    assert 72203070 in adapter._BROCCOLI_CODES_DEFAULT
    assert 92101901 in adapter._COFFEE_CODES_DEFAULT
    assert 11411390 in adapter._FERMENTED_DAIRY_CODES_DEFAULT
    assert 92309520 in adapter._GREEN_TEA_CODES_DEFAULT
