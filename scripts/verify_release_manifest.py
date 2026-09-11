"""Verify v0.2.0 release artifacts against the checked-in manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "release_manifest_0.2.0.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures: list[str] = []
    for artifact in manifest["artifacts"]:
        path = ROOT / artifact["path"]
        if not path.is_file():
            failures.append(f"missing: {path}")
            continue
        actual_size = path.stat().st_size
        actual_hash = sha256(path)
        if actual_size != artifact["bytes"]:
            failures.append(f"size mismatch: {path} ({actual_size} != {artifact['bytes']})")
        if actual_hash != artifact["sha256"].upper():
            failures.append(f"SHA-256 mismatch: {path} ({actual_hash})")
        print(f"PASS {artifact['path']} bytes={actual_size} sha256={actual_hash}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Release manifest verified ({len(manifest['artifacts'])} artifacts).")


if __name__ == "__main__":
    main()
