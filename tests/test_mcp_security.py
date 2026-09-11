from __future__ import annotations

from pathlib import Path

import pytest

from dietaryindex.mcp_server import (
    MAX_FILE_MAP_ITEMS,
    _resolve_file_map,
    _resolve_input_file,
    _resolve_output_dir,
    _validate_structured_payload,
)


def _configure_roots(monkeypatch: pytest.MonkeyPatch, input_root: Path, output_root: Path) -> None:
    monkeypatch.setenv("DIETARYINDEX_MCP_ALLOWED_ROOTS", str(input_root))
    monkeypatch.setenv("DIETARYINDEX_MCP_OUTPUT_ROOT", str(output_root))


def test_input_must_stay_inside_allowed_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    source = allowed / "input.csv"
    source.write_text("value\n1\n", encoding="utf-8")
    outside = tmp_path / "outside.csv"
    outside.write_text("value\n2\n", encoding="utf-8")
    _configure_roots(monkeypatch, allowed, tmp_path / "outputs")

    assert _resolve_input_file(str(source)) == source.resolve()
    with pytest.raises(ValueError, match="outside the configured MCP roots"):
        _resolve_input_file(str(outside))


def test_input_size_limit_is_enforced(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "large.csv"
    source.write_bytes(b"123456")
    _configure_roots(monkeypatch, tmp_path, tmp_path / "outputs")
    monkeypatch.setenv("DIETARYINDEX_MCP_MAX_INPUT_BYTES", "5")

    with pytest.raises(ValueError, match="too large"):
        _resolve_input_file(str(source))


def test_file_map_count_and_combined_size_are_bounded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _configure_roots(monkeypatch, tmp_path, tmp_path / "outputs")
    paths = {}
    for index in range(MAX_FILE_MAP_ITEMS + 1):
        source = tmp_path / f"{index}.csv"
        source.write_text("x\n1\n", encoding="utf-8")
        paths[str(index)] = str(source)
    with pytest.raises(ValueError, match="at most"):
        _resolve_file_map(paths)

    monkeypatch.setenv("DIETARYINDEX_MCP_MAX_TOTAL_INPUT_BYTES", "3")
    with pytest.raises(ValueError, match="Combined input size"):
        _resolve_file_map({"one": paths["0"]})


def test_output_must_stay_inside_dedicated_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    output_root = tmp_path / "outputs"
    _configure_roots(monkeypatch, tmp_path, output_root)

    nested = _resolve_output_dir(str(output_root / "run-1"))
    assert nested.is_dir()
    with pytest.raises(ValueError, match="must stay within"):
        _resolve_output_dir(str(tmp_path / "elsewhere"))


def test_structured_payload_rejects_non_finite_values() -> None:
    with pytest.raises(ValueError, match="JSON-compatible finite values"):
        _validate_structured_payload("options", {"bad": float("nan")})
