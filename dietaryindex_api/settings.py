"""Runtime settings for DietaryIndex API and deployment helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_ALLOWED_EXTENSIONS = (".csv", ".xlsx", ".xls", ".xpt", ".sas7bdat", ".txt")


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    runtime_dir: Path
    api_key: str
    require_api_key: bool
    max_upload_bytes: int
    allowed_extensions: tuple[str, ...]
    log_level: str


def _default_runtime_dir() -> Path:
    """Keep generated uploads and results outside the source tree."""
    if os.name == "nt":
        data_root = Path(
            os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local")
        )
    else:
        xdg_data_home = os.getenv("XDG_DATA_HOME", "").strip()
        data_root = Path(xdg_data_home) if xdg_data_home else Path.home() / ".local" / "share"
    return data_root / "DietaryIndexLocal" / "runtime_data"


def load_settings() -> Settings:
    runtime_dir = Path(
        os.getenv("DIETARYINDEX_RUNTIME_DIR", _default_runtime_dir())
    ).expanduser().resolve()
    api_key = os.getenv("DIETARYINDEX_API_KEY", "").strip()
    require_api_key = _as_bool(
        os.getenv("DIETARYINDEX_REQUIRE_API_KEY"),
        default=bool(api_key),
    )
    max_upload_mb = max(1, int(os.getenv("DIETARYINDEX_MAX_UPLOAD_MB", "100")))
    allowed_extensions = tuple(
        sorted(
            {
                item.strip().lower() if item.strip().startswith(".") else f".{item.strip().lower()}"
                for item in os.getenv(
                    "DIETARYINDEX_ALLOWED_EXTENSIONS",
                    ",".join(DEFAULT_ALLOWED_EXTENSIONS),
                ).split(",")
                if item.strip()
            }
        )
    )
    return Settings(
        runtime_dir=runtime_dir,
        api_key=api_key,
        require_api_key=require_api_key,
        max_upload_bytes=max_upload_mb * 1024 * 1024,
        allowed_extensions=allowed_extensions,
        log_level=os.getenv("DIETARYINDEX_LOG_LEVEL", "INFO").upper(),
    )


settings = load_settings()
