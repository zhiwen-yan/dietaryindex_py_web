"""Command-line entrypoint for dietaryindex."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dietaryindex.service import (
    get_index_catalog,
    get_index_detail,
    preview_file,
    run_compute,
    suggest_mapping,
    validate_mapping,
)


MULTI_FILE_ARGS = [
    "fped_path",
    "nutrient_path",
    "demo_path",
    "fped_path2",
    "nutrient_path2",
    "fped_ind_path",
    "nutrient_ind_path",
    "fped_ind_path2",
    "nutrient_ind_path2",
    "other_ingredients1",
    "other_ingredients2",
    "pyramid_path",
    "pyramid_path2",
    "mped_per_100_gram_path",
    "wjfrt",
]


def _json_dump(payload: object) -> None:
    encoding = (getattr(sys.stdout, "encoding", None) or "utf-8").lower().replace("-", "")
    ensure_ascii = not encoding.startswith("utf8")
    print(json.dumps(payload, ensure_ascii=ensure_ascii, indent=2))


def _load_mapping(path: str | None) -> dict:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _collect_file_paths(args: argparse.Namespace) -> dict[str, str]:
    payload = {}
    for key in MULTI_FILE_ARGS:
        value = getattr(args, key, None)
        if value:
            payload[key] = value
    return payload


def cmd_catalog(_args: argparse.Namespace) -> int:
    _json_dump({"items": get_index_catalog()})
    return 0


def cmd_detail(args: argparse.Namespace) -> int:
    _json_dump(get_index_detail(args.index))
    return 0


def cmd_preview(args: argparse.Namespace) -> int:
    _json_dump(preview_file(args.input, rows=args.rows))
    return 0


def cmd_suggest_mapping(args: argparse.Namespace) -> int:
    preview = preview_file(args.input, rows=3)
    _json_dump(suggest_mapping(args.index, preview["columns"]))
    return 0


def cmd_validate_mapping(args: argparse.Namespace) -> int:
    preview = preview_file(args.input, rows=3)
    mapping = _load_mapping(args.mapping_json)
    _json_dump(validate_mapping(args.index, mapping, preview["columns"]))
    return 0


def cmd_compute(args: argparse.Namespace) -> int:
    mapping = {}
    file_path = args.input
    file_paths = _collect_file_paths(args)

    if args.mode == "general":
        if not args.input:
            raise ValueError("--input is required for general mode.")
        preview = preview_file(args.input, rows=3)
        if args.auto_map:
            suggestions = suggest_mapping(args.index, preview["columns"])
            mapping = {
                field: meta["column"]
                for field, meta in suggestions["suggestions"].items()
                if meta["column"]
            }
        else:
            mapping = _load_mapping(args.mapping_json)
    else:
        if not file_path and not file_paths:
            raise ValueError("Provide --input for single-file modes or mode-specific file flags for NHANES modes.")
        if args.mapping_json:
            mapping = _load_mapping(args.mapping_json)

    result = run_compute(
        index_key=args.index,
        mode=args.mode,
        file_path=file_path,
        file_paths=file_paths or None,
        mapping=mapping,
        output_dir=args.output_dir,
    )
    _json_dump(result)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dietaryindex-cli",
        description="CLI for dietaryindex metadata, preview, mapping, and computation.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_catalog = subparsers.add_parser("catalog", help="List all available indices")
    p_catalog.set_defaults(func=cmd_catalog)

    p_detail = subparsers.add_parser("detail", help="Show one index definition")
    p_detail.add_argument("--index", required=True, help="Index key, e.g. HEI2020")
    p_detail.set_defaults(func=cmd_detail)

    p_preview = subparsers.add_parser("preview", help="Preview an input file")
    p_preview.add_argument("--input", required=True, help="Path to CSV / Excel / SAS / XPT file")
    p_preview.add_argument("--rows", type=int, default=10, help="Number of preview rows")
    p_preview.set_defaults(func=cmd_preview)

    p_suggest = subparsers.add_parser("suggest-mapping", help="Suggest a column mapping for one index")
    p_suggest.add_argument("--index", required=True, help="Index key")
    p_suggest.add_argument("--input", required=True, help="Path to input file")
    p_suggest.set_defaults(func=cmd_suggest_mapping)

    p_validate = subparsers.add_parser("validate-mapping", help="Validate a mapping JSON file")
    p_validate.add_argument("--index", required=True, help="Index key")
    p_validate.add_argument("--input", required=True, help="Path to input file")
    p_validate.add_argument("--mapping-json", required=True, help="Path to mapping JSON file")
    p_validate.set_defaults(func=cmd_validate_mapping)

    p_compute = subparsers.add_parser("compute", help="Run unified computation")
    p_compute.add_argument("--index", required=True, help="Index key")
    p_compute.add_argument("--input", help="Primary input file; used by general / ASA24 / DHQ3 / BLOCK modes")
    p_compute.add_argument("--mode", default="general", help="Computation mode, default general")
    p_compute.add_argument("--output-dir", help="Directory for exported result files")
    p_compute.add_argument("--mapping-json", help="Path to mapping JSON file or mode options JSON file")
    p_compute.add_argument(
        "--auto-map",
        action="store_true",
        help="Generate mapping automatically from previewed columns (general mode only)",
    )
    p_compute.add_argument("--fped-path", help="NHANES FPED totals day 1")
    p_compute.add_argument("--nutrient-path", help="NHANES nutrient totals day 1")
    p_compute.add_argument("--demo-path", help="NHANES DEMO file")
    p_compute.add_argument("--fped-path2", help="NHANES FPED totals day 2")
    p_compute.add_argument("--nutrient-path2", help="NHANES nutrient totals day 2")
    p_compute.add_argument("--fped-ind-path", help="NHANES FPED individual foods day 1")
    p_compute.add_argument("--nutrient-ind-path", help="NHANES nutrient individual foods day 1")
    p_compute.add_argument("--fped-ind-path2", help="NHANES FPED individual foods day 2")
    p_compute.add_argument("--nutrient-ind-path2", help="NHANES nutrient individual foods day 2")
    p_compute.add_argument("--other-ingredients1", help="Optional other ingredients day 1 CSV")
    p_compute.add_argument("--other-ingredients2", help="Optional other ingredients day 2 CSV")
    p_compute.add_argument("--pyramid-path", help="NHANES MPED/Pyramid totals day 1")
    p_compute.add_argument("--pyramid-path2", help="NHANES MPED/Pyramid totals day 2")
    p_compute.add_argument("--mped-per-100-gram-path", help="MPED equiv.txt or similar lookup file")
    p_compute.add_argument("--wjfrt", help="Optional WJFRT CSV override")
    p_compute.set_defaults(func=cmd_compute)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
