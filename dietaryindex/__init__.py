"""
dietaryindex - Python implementation of comprehensive dietary quality indices.

Based on the dietaryindex R package by James Zhan.
Source: https://github.com/jamesjiadazhan/dietaryindex

Core indices:
    DII      - Dietary Inflammatory Index
    HEI2015  - Healthy Eating Index 2015
    HEI2020  - Healthy Eating Index 2020 (含幼儿版)
    AHEI     - Alternative Healthy Eating Index
    AHEIP    - AHEI for Pregnancy
    DASH     - Dietary Approaches to Stop Hypertension
    DASHI    - DASH nutrient-based
    MED      - Mediterranean Diet
    MEDI     - Mediterranean Diet (PREDIMED)
    ACS2020  - American Cancer Society 2020 (V1 + V2)
    PHDI     - Planetary Health Diet Index
    DI_GM    - Dietary Index for Gut Microbiota
    PDI      - Plant-based Diet Index family (PDI / hPDI / uPDI)
    MIND     - Mediterranean-DASH Intervention for Neurodegenerative Delay
    DQI_I    - Diet Quality Index-International
    CHEI     - Chinese Healthy Eating Index
    DBI      - Diet Balance Index-07
    GDQS     - Global Diet Quality Score
    NRF/NAR/MAR/INQ - Nutrient-density and adequacy family
    PRAL/NEAP - Acid-load family
    CDAI     - Composite Dietary Antioxidant Index

DII adapters (one-step):
    DII_NHANES_FPED - NHANES FPED (2005+)
    DII_NHANES_MPED - NHANES MPED (1999-2004)
    DII_ASA24       - ASA24
    DII_DHQ3        - DHQ3
    DII_BLOCK       - BLOCK FFQ

Reference:
    Zhan, J. et al. "dietaryindex: A User-Friendly and Versatile R Package
    for Standardizing Dietary Pattern Analysis in Epidemiological
    and Clinical Studies."
"""

__version__ = "0.3.0"

from dietaryindex.core.dii import compute_dii
from dietaryindex.core.hei2015 import compute_hei2015
from dietaryindex.core.hei2020 import compute_hei2020, compute_hei2020_v2
from dietaryindex.core.ahei import compute_ahei
from dietaryindex.core.aheip import compute_aheip
from dietaryindex.core.dash import compute_dash
from dietaryindex.core.dashi import compute_dashi
from dietaryindex.core.med import compute_med
from dietaryindex.core.medi import compute_medi, compute_medi_v2
from dietaryindex.core.acs2020 import compute_acs2020_v1, compute_acs2020_v2
from dietaryindex.core.phdi import compute_phdi, compute_phdi_v2
from dietaryindex.core.di_gm import compute_di_gm
from dietaryindex.core.fisi import compute_fisi
from dietaryindex.core.pdi import compute_pdi, compute_hpdi, compute_updi
from dietaryindex.core.mind import compute_mind
from dietaryindex.core.dqii import compute_dqii
from dietaryindex.core.chei import compute_chei
from dietaryindex.core.dbi import compute_dbi
from dietaryindex.core.gdqs import compute_gdqs
from dietaryindex.core.wish import compute_wish
from dietaryindex.core.obs import compute_obs
from dietaryindex.core.edii import compute_edii
from dietaryindex.core.china_dii import compute_china_dii
from dietaryindex.core.nutrient_indices import (
    compute_nrf,
    compute_nar,
    compute_mar,
    compute_inq,
    compute_pral,
    compute_neap,
    compute_cdai,
)
from dietaryindex.core._scoring import (
    fit_reference_cutoffs,
    get_reference_cutoffs,
    get_reference_group_columns,
    reference_table_to_wide,
    score_healthy,
    score_median_healthy,
    score_median_unhealthy,
    score_median_with_cutoff,
    score_quantile_with_cutoffs,
    score_quartile_healthy,
    score_quartile_unhealthy,
    score_decile_sodium,
    score_quintile_healthy,
    score_quintile_unhealthy,
    score_series_with_reference,
    score_unhealthy,
)
from dietaryindex.reference.dii_global import DII_REFERENCE, DII_VARIABLE_ORDER
from dietaryindex.reference.china_dii import CHINA_DII_REFERENCE, CHINA_DII_VARIABLE_ORDER
from dietaryindex.reference.edii_reference import EDII_REFERENCE, EDII_VARIABLE_ORDER
from dietaryindex.reference.index_registry import (
    INDEX_FAMILY_REGISTRY,
    INDEX_SPEC_REGISTRY,
    OUTPUT_NAMING_RULES,
    get_family_blueprint_table,
    get_index_spec_table,
    get_output_naming_rules,
)
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
from dietaryindex.adapters.phdi import (
    compute_phdi_nhanes_fped,
    compute_phdi_nhanes_mped,
    compute_phdi_asa24,
    compute_phdi_dhq3,
    compute_phdi_block,
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
from dietaryindex.adapters.fisi import (
    compute_fisi_nhanes,
    compute_fisi26_nhanes,
    compute_fisi1_nhanes,
    compute_flav_fisi_nhanes,
)
from dietaryindex.service import (
    auto_map_fields,
    build_result_payload,
    get_fii_detail,
    get_fii_summary,
    get_index_catalog,
    get_index_detail,
    get_mode_definitions,
    get_mode_file_specs,
    get_mode_requirements,
    load_dataframe_from_path,
    preview_file,
    run_compute,
    search_fii,
    summarize_asa24,
    suggest_mapping,
    validate_auto_mapping,
    validate_mapping,
)

__all__ = [
    "compute_dii",
    "compute_hei2015",
    "compute_hei2020",
    "compute_hei2020_v2",
    "compute_ahei",
    "compute_aheip",
    "compute_dash",
    "compute_dashi",
    "compute_med",
    "compute_medi",
    "compute_medi_v2",
    "compute_acs2020_v1",
    "compute_acs2020_v2",
    "compute_phdi",
    "compute_phdi_v2",
    "compute_di_gm",
    "compute_fisi",
    "compute_pdi",
    "compute_hpdi",
    "compute_updi",
    "compute_mind",
    "compute_dqii",
    "compute_chei",
    "compute_dbi",
    "compute_gdqs",
    "compute_wish",
    "compute_obs",
    "compute_edii",
    "compute_china_dii",
    "compute_nrf",
    "compute_nar",
    "compute_mar",
    "compute_inq",
    "compute_pral",
    "compute_neap",
    "compute_cdai",
    "DII_REFERENCE",
    "DII_VARIABLE_ORDER",
    "CHINA_DII_REFERENCE",
    "CHINA_DII_VARIABLE_ORDER",
    "EDII_REFERENCE",
    "EDII_VARIABLE_ORDER",
    "INDEX_FAMILY_REGISTRY",
    "INDEX_SPEC_REGISTRY",
    "OUTPUT_NAMING_RULES",
    "fit_reference_cutoffs",
    "get_family_blueprint_table",
    "get_index_spec_table",
    "get_output_naming_rules",
    "get_reference_cutoffs",
    "get_reference_group_columns",
    "reference_table_to_wide",
    "score_healthy",
    "score_unhealthy",
    "score_quantile_with_cutoffs",
    "score_quintile_healthy",
    "score_quintile_unhealthy",
    "score_series_with_reference",
    "score_median_with_cutoff",
    "score_median_healthy",
    "score_median_unhealthy",
    "score_quartile_healthy",
    "score_quartile_unhealthy",
    "score_decile_sodium",
    # DII adapters
    "compute_dii_nhanes_fped",
    "compute_dii_nhanes_mped",
    "compute_dii_asa24",
    "compute_dii_dhq3",
    "compute_dii_block",
    # DII other adapters
    "compute_ahei_dhq3",
    # HEI2015/HEI2020/MED/DASHI adapters
    "compute_hei2015_nhanes_fped",
    "compute_hei2020_nhanes_fped",
    "compute_med_nhanes_fped",
    "compute_dashi_nhanes_fped",
    # DASH/AHEI/MEDI/DI_GM iff-level adapters
    "compute_dash_nhanes_fped",
    "compute_ahei_nhanes_fped",
    "compute_medi_nhanes_fped",
    "compute_di_gm_nhanes_fped",
    "compute_phdi_nhanes_fped",
    "compute_phdi_nhanes_mped",
    "compute_phdi_asa24",
    "compute_phdi_dhq3",
    "compute_phdi_block",
    # MPED adapters
    "compute_hei2015_nhanes_mped",
    "compute_hei2020_nhanes_mped",
    "compute_med_nhanes_mped",
    "compute_dashi_nhanes_mped",
    "compute_ahei_nhanes_mped",
    "compute_medi_nhanes_mped",
    "compute_dash_nhanes_mped",
    "compute_di_gm_nhanes_mped",
    # BLOCK adapters
    "compute_ahei_block",
    "compute_aheip_block",
    # FISI/FII adapters
    "compute_fisi_nhanes",
    "compute_fisi26_nhanes",
    "compute_fisi1_nhanes",
    "compute_flav_fisi_nhanes",
    # unified service layer
    "get_index_catalog",
    "get_index_detail",
    "get_mode_definitions",
    "get_mode_file_specs",
    "get_mode_requirements",
    "auto_map_fields",
    "preview_file",
    "load_dataframe_from_path",
    "summarize_asa24",
    "suggest_mapping",
    "validate_auto_mapping",
    "validate_mapping",
    "run_compute",
    "build_result_payload",
    "get_fii_summary",
    "search_fii",
    "get_fii_detail",
]
