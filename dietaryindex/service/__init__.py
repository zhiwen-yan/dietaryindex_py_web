"""Service-layer helpers for API and app integrations."""

from dietaryindex.service.compute import run_compute
from dietaryindex.service.files import preview_file, load_dataframe_from_path
from dietaryindex.service.fii_database import get_fii_detail, get_fii_summary, search_fii
from dietaryindex.service.mapping import suggest_mapping, validate_mapping
from dietaryindex.service.registry import get_index_catalog, get_index_detail, get_mode_definitions, get_mode_file_specs, get_mode_requirements
from dietaryindex.service.results import build_result_payload
from dietaryindex.service.source_modes import auto_map_fields, summarize_asa24, validate_auto_mapping

__all__ = [
    "build_result_payload",
    "auto_map_fields",
    "get_fii_detail",
    "get_fii_summary",
    "get_index_catalog",
    "get_index_detail",
    "get_mode_definitions",
    "get_mode_file_specs",
    "get_mode_requirements",
    "load_dataframe_from_path",
    "preview_file",
    "run_compute",
    "search_fii",
    "summarize_asa24",
    "suggest_mapping",
    "validate_auto_mapping",
    "validate_mapping",
]
