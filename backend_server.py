"""Loopback-only FastAPI sidecar used by the Electron desktop host."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the DietaryIndex desktop API sidecar.")
    parser.add_argument("--port", type=int, required=True)
    return parser.parse_args()


def main() -> int:
    options = parse_args()
    if not 1 <= options.port <= 65535:
        raise SystemExit("--port must be between 1 and 65535")

    import uvicorn

    # Import after argument parsing so the Electron-supplied environment (runtime
    # directory and per-launch API key) is loaded by dietaryindex_api.settings.
    from dietaryindex_api.app import app

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=options.port,
        log_level="warning",
        access_log=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
