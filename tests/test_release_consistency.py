from __future__ import annotations

import io
import json
import re
import sys
import tomllib
from pathlib import Path

from dietaryindex import __version__
from dietaryindex.cli import _json_dump
from dietaryindex.reference.index_registry import INDEX_SPEC_REGISTRY
from dietaryindex.service.compute import GENERAL_FUNCTION_MAP
from dietaryindex.service.registry import INDEX_MODE_CONFIG, INDEX_PARAMS, get_index_catalog


ROOT = Path(__file__).resolve().parents[1]
RELEASE_VERSION = "0.3.0"


def test_release_version_is_consistent_across_public_metadata():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    installer = (ROOT / "packaging" / "windows" / "DietaryIndexLocal.iss").read_text(encoding="utf-8")
    frontend_package = json.loads((ROOT / "web_frontend" / "package.json").read_text(encoding="utf-8"))
    electron_package = json.loads((ROOT / "electron_app" / "package.json").read_text(encoding="utf-8"))
    api_source = (ROOT / "dietaryindex_api" / "app.py").read_text(encoding="utf-8")

    assert __version__ == RELEASE_VERSION
    assert pyproject["project"]["version"] == RELEASE_VERSION
    assert pyproject["project"]["requires-python"] == ">=3.10"
    assert f'version: "{RELEASE_VERSION}"' in citation
    assert f'#define AppVersion "{RELEASE_VERSION}"' in installer
    assert frontend_package["version"] == RELEASE_VERSION
    assert electron_package["version"] == RELEASE_VERSION
    assert "version=__version__" in api_source


def test_base_index_registries_and_modes_are_identical():
    specs = {item["index_key"]: item for item in INDEX_SPEC_REGISTRY}
    assert len(specs) == 32
    assert set(specs) == set(INDEX_MODE_CONFIG)
    for index_key, spec in specs.items():
        assert tuple(spec["supported_modes"]) == tuple(INDEX_MODE_CONFIG[index_key])


def test_all_40_service_entries_have_callable_implementations():
    assert len(INDEX_PARAMS) == 40
    assert len(get_index_catalog()) == 40
    missing = {
        config["function"]
        for config in INDEX_PARAMS.values()
        if config["function"] not in GENERAL_FUNCTION_MAP
    }
    assert missing == set()


def test_all_40_service_entries_expose_canonical_score_scales():
    spec_scales = {item["index_key"]: item["score_scale"] for item in INDEX_SPEC_REGISTRY}
    catalog = {item["index_key"]: item for item in get_index_catalog()}
    assert {key: catalog[key]["score_scale"] for key in spec_scales} == spec_scales
    assert {key: catalog[key]["score_scale"] for key in (
        "HEI2020_V1", "HEI2020_V2", "MEDI_V1", "MEDI_V2",
        "ACS2020_V1", "ACS2020_V2", "PHDI_V1", "PHDI_V2",
    )} == {
        "HEI2020_V1": "0-100",
        "HEI2020_V2": "0-100",
        "MEDI_V1": "0-11",
        "MEDI_V2": "0-55",
        "ACS2020_V1": "0-12",
        "ACS2020_V2": "0-12",
        "PHDI_V1": "0-140",
        "PHDI_V2": "0-140",
    }


def test_nextjs_groups_cover_every_service_entry_once():
    source = (ROOT / "web_frontend" / "lib" / "index-groups.ts").read_text(encoding="utf-8")
    frontend_keys = re.findall(r'"([A-Z][A-Z0-9_]*)"', source)
    assert len(frontend_keys) == len(set(frontend_keys))
    assert set(frontend_keys) == set(INDEX_PARAMS)


def test_public_score_ranges_match_implementation_metadata():
    expected_maxima = {
        "ACS2020": 12,
        "ACS2020_V1": 12,
        "ACS2020_V2": 12,
        "PHDI": 140,
        "PHDI_V1": 140,
        "PHDI_V2": 140,
        "MEDI": 11,
        "MEDI_V1": 11,
        "MEDI_V2": 55,
    }
    for index_key, expected in expected_maxima.items():
        assert INDEX_PARAMS[index_key]["max_score"] == expected

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "(docs/INDEX_SUPPORT_MATRIX.md)" in readme
    support_matrix = (ROOT / "docs" / "INDEX_SUPPORT_MATRIX.md").read_text(encoding="utf-8")
    matrix_rows = [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in support_matrix.splitlines()
        if line.startswith("| `")
    ]
    documented_scales = {row[0].strip("`"): row[2] for row in matrix_rows}
    for index_key in ("ACS2020", "PHDI"):
        assert documented_scales[index_key] == f"0-{expected_maxima[index_key]}"


def test_cli_json_output_is_safe_on_windows_gbk(monkeypatch):
    raw = io.BytesIO()
    gbk_stdout = io.TextIOWrapper(raw, encoding="gbk")
    monkeypatch.setattr(sys, "stdout", gbk_stdout)

    _json_dump({"author": "Malmö", "label": "中文"})
    gbk_stdout.flush()

    decoded = raw.getvalue().decode("gbk")
    assert json.loads(decoded) == {"author": "Malmö", "label": "中文"}
