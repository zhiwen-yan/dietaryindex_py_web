"""Local STDIO MCP server for the DietaryIndex desktop calculation engine."""

from __future__ import annotations

import os
import json
import sys
from pathlib import Path
from typing import Any

# Codex may launch a STDIO server from a different workspace directory, so
# resolve the project root from this file instead of relying on cwd/PYTHONPATH.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from dietaryindex import (
    __version__,
    get_fii_detail,
    get_fii_summary,
    get_index_catalog,
    get_index_detail,
    preview_file,
    run_compute,
    search_fii,
    suggest_mapping,
)
from dietaryindex.service.fii_database import get_fii_peers


SUPPORTED_INPUT_SUFFIXES = {".csv", ".xlsx", ".xls", ".xpt", ".sas7bdat"}
DEFAULT_MAX_INPUT_BYTES = 512 * 1024 * 1024
DEFAULT_MAX_TOTAL_INPUT_BYTES = 2 * 1024 * 1024 * 1024
MAX_FILE_MAP_ITEMS = 32
MAX_STRUCTURED_PAYLOAD_BYTES = 1024 * 1024
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False)
LOCAL_WRITE = ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=False)

mcp = MCPServer(
    "DietaryIndex",
    title="DietaryIndex local calculation server",
    version=__version__,
    instructions=(
        "Use get_index before computing when the index, algorithm version, or data mode is uncertain. "
        "For general mode, preview_dataset then suggest_dataset_mapping before compute_index. "
        "NHANES and questionnaire modes may require multiple named files; follow mode_requirements exactly. "
        "Never invent missing dietary fields or silently substitute a different index."
    ),
)


def _path_from_user(value: str) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(value.strip()))
    if not expanded:
        raise ValueError("A non-empty local path is required.")
    return Path(expanded).resolve()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _default_output_root() -> Path:
    base = Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    return (base / "DietaryIndex" / "runtime_data" / "mcp_results").resolve()


def _configured_input_roots() -> tuple[Path, ...]:
    configured = os.getenv("DIETARYINDEX_MCP_ALLOWED_ROOTS", "").strip()
    raw_roots = configured.split(os.pathsep) if configured else [str(Path.home())]
    roots = tuple(_path_from_user(value) for value in raw_roots if value.strip())
    if not roots:
        raise ValueError("DIETARYINDEX_MCP_ALLOWED_ROOTS does not contain a valid path.")
    return roots


def _configured_output_root() -> Path:
    configured = os.getenv("DIETARYINDEX_MCP_OUTPUT_ROOT", "").strip()
    return _path_from_user(configured) if configured else _default_output_root()


def _positive_size_limit(env_name: str, default: int) -> int:
    configured = os.getenv(env_name, "").strip()
    if not configured:
        return default
    try:
        value = int(configured)
    except ValueError as exc:
        raise ValueError(f"{env_name} must be a positive integer number of bytes.") from exc
    if value < 1:
        raise ValueError(f"{env_name} must be a positive integer number of bytes.")
    return value


def _assert_allowed_input(path: Path) -> None:
    roots = _configured_input_roots()
    if not any(_is_within(path, root) for root in roots):
        allowed = ", ".join(str(root) for root in roots)
        raise ValueError(f"Input path is outside the configured MCP roots: {path}. Allowed roots: {allowed}")


def _resolve_input_file(file_path: str) -> Path:
    path = _path_from_user(file_path)
    _assert_allowed_input(path)
    if not path.is_file():
        raise ValueError(f"Input file does not exist: {path}")
    if path.suffix.lower() not in SUPPORTED_INPUT_SUFFIXES:
        raise ValueError(
            f"Unsupported input type {path.suffix!r}. "
            f"Supported: {', '.join(sorted(SUPPORTED_INPUT_SUFFIXES))}"
        )
    max_bytes = _positive_size_limit("DIETARYINDEX_MCP_MAX_INPUT_BYTES", DEFAULT_MAX_INPUT_BYTES)
    size = path.stat().st_size
    if size > max_bytes:
        raise ValueError(f"Input file is too large ({size} bytes); configured limit is {max_bytes} bytes: {path}")
    return path


def _resolve_file_map(file_paths: dict[str, str] | None) -> dict[str, Path] | None:
    if not file_paths:
        return None
    if len(file_paths) > MAX_FILE_MAP_ITEMS:
        raise ValueError(f"file_paths accepts at most {MAX_FILE_MAP_ITEMS} named files.")
    resolved = {str(key): _resolve_input_file(value) for key, value in file_paths.items()}
    total_bytes = sum(path.stat().st_size for path in resolved.values())
    max_total = _positive_size_limit(
        "DIETARYINDEX_MCP_MAX_TOTAL_INPUT_BYTES",
        DEFAULT_MAX_TOTAL_INPUT_BYTES,
    )
    if total_bytes > max_total:
        raise ValueError(
            f"Combined input size is too large ({total_bytes} bytes); configured limit is {max_total} bytes."
        )
    return resolved


def _resolve_output_dir(output_dir: str | None) -> Path:
    root = _configured_output_root()
    target = _path_from_user(output_dir) if output_dir else root
    if not _is_within(target, root):
        raise ValueError(f"Output path must stay within the configured MCP output root: {root}")
    if target.exists() and not target.is_dir():
        raise ValueError(f"Output path exists but is not a directory: {target}")
    target.mkdir(parents=True, exist_ok=True)
    return target


def _validate_structured_payload(name: str, value: dict[str, Any] | None) -> dict[str, Any]:
    payload = value or {}
    try:
        encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must contain JSON-compatible finite values.") from exc
    if len(encoded) > MAX_STRUCTURED_PAYLOAD_BYTES:
        raise ValueError(f"{name} exceeds the {MAX_STRUCTURED_PAYLOAD_BYTES}-byte MCP limit.")
    return payload


@mcp.tool(annotations=READ_ONLY)
def list_indices(query: str = "") -> dict[str, Any]:
    """List supported dietary indices, algorithm modes, output fields, and titles."""
    term = query.strip().lower()
    catalog = get_index_catalog()
    if term:
        catalog = [
            item
            for item in catalog
            if term
            in " ".join(
                str(item.get(key, ""))
                for key in ("index_key", "title_en", "title_zh", "description_en", "description_zh")
            ).lower()
        ]
    return {"count": len(catalog), "indices": catalog}


@mcp.tool(annotations=READ_ONLY)
def get_index(index_key: str) -> dict[str, Any]:
    """Get one index's fields, supported data modes, file requirements, outputs, and references."""
    try:
        return get_index_detail(index_key.strip().upper())
    except KeyError as exc:
        raise ValueError(str(exc)) from exc


@mcp.tool(annotations=READ_ONLY)
def preview_dataset(file_path: str, rows: int = 8, sheet_name: str | int | None = 0) -> dict[str, Any]:
    """Preview a local dietary dataset before mapping or computation."""
    if rows < 1 or rows > 50:
        raise ValueError("rows must be between 1 and 50.")
    return preview_file(_resolve_input_file(file_path), rows=rows, sheet_name=sheet_name)


@mcp.tool(annotations=READ_ONLY)
def suggest_dataset_mapping(index_key: str, file_path: str, sheet_name: str | int | None = 0) -> dict[str, Any]:
    """Suggest a field mapping between a local dataset and one dietary index."""
    preview = preview_file(_resolve_input_file(file_path), rows=3, sheet_name=sheet_name)
    result = suggest_mapping(index_key.strip().upper(), preview["columns"])
    result["source_file"] = str(Path(file_path).expanduser().resolve())
    result["source_columns"] = preview["columns"]
    return result


@mcp.tool(annotations=LOCAL_WRITE)
def compute_index(
    index_key: str,
    mode: str = "general",
    file_path: str | None = None,
    file_paths: dict[str, str] | None = None,
    mapping: dict[str, Any] | None = None,
    options: dict[str, Any] | None = None,
    output_dir: str | None = None,
) -> dict[str, Any]:
    """Compute an index from local files and return summary statistics plus downloadable result paths."""
    resolved_file = _resolve_input_file(file_path) if file_path else None
    resolved_files = _resolve_file_map(file_paths)
    target = _resolve_output_dir(output_dir)
    return run_compute(
        index_key=index_key.strip().upper(),
        mode=mode.strip().lower(),
        file_path=resolved_file,
        file_paths=resolved_files,
        mapping=_validate_structured_payload("mapping", mapping),
        options=_validate_structured_payload("options", options),
        output_dir=target,
    )


@mcp.tool(annotations=READ_ONLY)
def search_fii_foods(
    query: str = "",
    limit: int = 20,
    group: str | None = None,
    direction: str = "all",
    sort_by: str = "best_match",
) -> dict[str, Any]:
    """Search the bundled English USDA FII database by food name or exact FDCD food code."""
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100.")
    foods = search_fii(query, limit, group=group, direction=direction, sort_by=sort_by)
    return {"count": len(foods), "foods": foods, "database": get_fii_summary()}


@mcp.tool(annotations=READ_ONLY)
def get_fii_food(fdcd: int, peer_limit: int = 5) -> dict[str, Any]:
    """Get one FII food by FDCD code and compare anti-/pro-inflammatory peers in its food group."""
    if peer_limit < 1 or peer_limit > 20:
        raise ValueError("peer_limit must be between 1 and 20.")
    food = get_fii_detail(fdcd)
    if food is None:
        raise ValueError(f"Unknown FDCD food code: {fdcd}")
    return {"food": food, "peers": get_fii_peers(fdcd, limit=peer_limit)}


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
