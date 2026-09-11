"""Dry-run friendly cleanup helper for DietaryIndex runtime files."""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from dietaryindex_api.settings import load_settings


def _age_cutoff(days: int) -> datetime:
    return datetime.now(UTC) - timedelta(days=days)


def _is_older_than(path: Path, cutoff: datetime) -> bool:
    modified = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
    return modified < cutoff


def _collect_targets(runtime_dir: Path, log_dir: Path, cutoff: datetime) -> list[Path]:
    targets: list[Path] = []

    uploads = runtime_dir / "uploads"
    results = runtime_dir / "results"

    for folder in (uploads, results):
        if folder.exists():
            for path in folder.iterdir():
                if path.name == ".gitkeep":
                    continue
                if _is_older_than(path, cutoff):
                    targets.append(path)

    if log_dir.exists():
        for pattern in ("*.log", "*.err.log"):
            for path in log_dir.glob(pattern):
                if _is_older_than(path, cutoff):
                    targets.append(path)

    return sorted(targets)


def _remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Clean old runtime uploads, exported results, and application log files.",
    )
    parser.add_argument("--days", type=int, default=7, help="Delete files older than this many days.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually delete files. Without this flag the command only prints a dry-run preview.",
    )
    parser.add_argument(
        "--runtime-dir",
        type=Path,
        help="Override the configured runtime-data directory.",
    )
    args = parser.parse_args()

    runtime_dir = (
        args.runtime_dir.expanduser().resolve()
        if args.runtime_dir is not None
        else load_settings().runtime_dir
    )
    cutoff = _age_cutoff(args.days)
    targets = _collect_targets(runtime_dir, runtime_dir.parent / "logs", cutoff)

    if not targets:
        print("No cleanup targets found.")
        return 0

    print(f"Runtime directory: {runtime_dir}")
    print(f"Found {len(targets)} cleanup target(s) older than {args.days} day(s):")
    for path in targets:
        print(f" - {path}")

    if not args.apply:
        print("Dry run only. Re-run with --apply to delete.")
        return 0

    for path in targets:
        _remove_path(path)
    print("Cleanup completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
