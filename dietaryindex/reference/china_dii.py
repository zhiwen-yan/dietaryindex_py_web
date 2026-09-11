"""China-DII reference table.

Primary source:
Chen Y, Luo Z, Cheng L, et al. Development and Validation of the China Dietary
Inflammatory Index. Nutrients. 2025;17(10):1687.

Implementation note:
The paper text describes a 27-parameter China-DII. However, the published
reference table (Table 4) explicitly reports reference means and SDs for 23
dietary components. This implementation reproduces the reference table exactly
as published rather than imputing unpublished component values.
"""

from __future__ import annotations

from dietaryindex.reference.dii_global import DII_REFERENCE


_CHINA_DII_TABLE4 = {
    "KCAL": {"china_mean": 1869.00, "china_sd": 532.64},
    "PROTEIN": {"china_mean": 65.66, "china_sd": 21.09},
    "CARB": {"china_mean": 271.00, "china_sd": 91.51},
    "TOTALFAT": {"china_mean": 64.14, "china_sd": 24.94},
    "CHOLES": {"china_mean": 328.19, "china_sd": 194.62},
    "SATFAT": {"china_mean": 18.42, "china_sd": 8.60},
    "MUFA": {"china_mean": 30.74, "china_sd": 12.01},
    "PUFA": {"china_mean": 19.04, "china_sd": 6.00},
    "FIBER": {"china_mean": 12.42, "china_sd": 5.88},
    "FOLICACID": {"china_mean": 139.20, "china_sd": 58.22},
    "VITA": {"china_mean": 376.13, "china_sd": 294.38},
    "THIAMIN": {"china_mean": 0.92, "china_sd": 0.31},
    "RIBOFLAVIN": {"china_mean": 0.81, "china_sd": 0.31},
    "NIACIN": {"china_mean": 13.31, "china_sd": 3.56},
    "VITB6": {"china_mean": 0.51, "china_sd": 0.27},
    "VITB12": {"china_mean": 0.98, "china_sd": 0.84},
    "VITC": {"china_mean": 80.35, "china_sd": 35.90},
    "VITD": {"china_mean": 3.74, "china_sd": 2.93},
    "VITE": {"china_mean": 26.31, "china_sd": 11.26},
    "ZN": {"china_mean": 9.67, "china_sd": 2.96},
    "MG": {"china_mean": 280.13, "china_sd": 72.59},
    "IRON": {"china_mean": 19.01, "china_sd": 6.34},
    "SE": {"china_mean": 42.91, "china_sd": 16.03},
}


CHINA_DII_REFERENCE = {
    key: {
        "inflammatory_score": DII_REFERENCE[key]["inflammatory_score"],
        "china_mean": value["china_mean"],
        "china_sd": value["china_sd"],
    }
    for key, value in _CHINA_DII_TABLE4.items()
}

CHINA_DII_VARIABLE_ORDER = tuple(CHINA_DII_REFERENCE.keys())


__all__ = [
    "CHINA_DII_REFERENCE",
    "CHINA_DII_VARIABLE_ORDER",
]
