"""Reference data and metadata registries for dietaryindex."""

from dietaryindex.reference.china_dii import CHINA_DII_REFERENCE, CHINA_DII_VARIABLE_ORDER
from dietaryindex.reference.dii_global import DII_REFERENCE, DII_VARIABLE_ORDER
from dietaryindex.reference.edii_reference import EDII_REFERENCE, EDII_VARIABLE_ORDER
from dietaryindex.reference.fisi_nrv import (
    FISI_FLAVONOID_COMPONENTS,
    fisi_component_names,
    load_fisi_nrv,
)
from dietaryindex.reference.index_registry import (
    INDEX_FAMILY_REGISTRY,
    INDEX_SPEC_REGISTRY,
    OUTPUT_NAMING_RULES,
    get_family_blueprint_table,
    get_index_spec_table,
    get_output_naming_rules,
)

__all__ = [
    "CHINA_DII_REFERENCE",
    "CHINA_DII_VARIABLE_ORDER",
    "DII_REFERENCE",
    "DII_VARIABLE_ORDER",
    "EDII_REFERENCE",
    "EDII_VARIABLE_ORDER",
    "FISI_FLAVONOID_COMPONENTS",
    "INDEX_FAMILY_REGISTRY",
    "INDEX_SPEC_REGISTRY",
    "OUTPUT_NAMING_RULES",
    "get_family_blueprint_table",
    "fisi_component_names",
    "get_index_spec_table",
    "get_output_naming_rules",
    "load_fisi_nrv",
]
