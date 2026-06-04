"""Shared utility helpers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_directory(path: Path) -> None:
    """Create a directory when it does not already exist.

    Args:
        path: Directory path to create.
    """

    path.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: dict[str, Any]) -> None:
    """Write JSON with stable formatting.

    Args:
        path: Output JSON path.
        data: JSON-serializable dictionary.
    """

    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    """Read text using replacement for invalid bytes.

    Args:
        path: Input text file path.

    Returns:
        Decoded text content.
    """

    return path.read_text(encoding="utf-8", errors="replace")
