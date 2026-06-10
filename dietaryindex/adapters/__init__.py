from dietaryindex.adapters.nhanes_fped import compute_dii_nhanes_fped
from dietaryindex.adapters.nhanes_fped_other import (
    compute_hei2015_nhanes_fped,
    compute_hei2020_nhanes_fped,
    compute_med_nhanes_fped,
    compute_dashi_nhanes_fped,
)
from dietaryindex.adapters.nhanes_fped_ind import (
    compute_dash_nhanes_fped,
    compute_ahei_nhanes_fped,
    compute_medi_nhanes_fped,
    compute_di_gm_nhanes_fped,
)
from dietaryindex.adapters.nhanes_mped import compute_dii_nhanes_mped
from dietaryindex.adapters.nhanes_mped_other import (
    compute_hei2015_nhanes_mped,
    compute_hei2020_nhanes_mped,
    compute_med_nhanes_mped,
    compute_dashi_nhanes_mped,
    compute_ahei_nhanes_mped,
    compute_medi_nhanes_mped,
    compute_dash_nhanes_mped,
    compute_di_gm_nhanes_mped,
)
from dietaryindex.adapters.asa24 import compute_dii_asa24
from dietaryindex.adapters.dhq3 import compute_dii_dhq3, compute_ahei_dhq3
from dietaryindex.adapters.block import compute_dii_block, compute_ahei_block, compute_aheip_block

__all__ = [
    "compute_dii_nhanes_fped",
    "compute_hei2015_nhanes_fped",
    "compute_hei2020_nhanes_fped",
    "compute_med_nhanes_fped",
    "compute_dashi_nhanes_fped",
    "compute_dash_nhanes_fped",
    "compute_ahei_nhanes_fped",
    "compute_medi_nhanes_fped",
    "compute_di_gm_nhanes_fped",
    "compute_dii_nhanes_mped",
    "compute_hei2015_nhanes_mped",
    "compute_hei2020_nhanes_mped",
    "compute_med_nhanes_mped",
    "compute_dashi_nhanes_mped",
    "compute_ahei_nhanes_mped",
    "compute_medi_nhanes_mped",
    "compute_dash_nhanes_mped",
    "compute_di_gm_nhanes_mped",
    "compute_dii_asa24",
    "compute_dii_dhq3",
    "compute_ahei_dhq3",
    "compute_dii_block",
    "compute_ahei_block",
    "compute_aheip_block",
]
