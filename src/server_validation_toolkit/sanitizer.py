"""Best-effort sanitizer for diagnostic logs."""

from __future__ import annotations

import re
import shutil
from collections.abc import Iterable
from pathlib import Path

from server_validation_toolkit.utils import ensure_directory, read_text

SANITIZER_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        "<IPv4_REDACTED>",
    ),
    (
        re.compile(r"\b[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}\b"),
        "<MAC_REDACTED>",
    ),
    (
        re.compile(
            r"\b[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-"
            r"[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}\b"
        ),
        "<UUID_REDACTED>",
    ),
    (
        re.compile(r"(?i)\b(serial number|serial|asset tag|uuid)\s*[:=]\s*\S+"),
        r"\1: <IDENTIFIER_REDACTED>",
    ),
    (
        re.compile(r"(?i)\b(hostname|host name|node name)\s*[:=]\s*\S+"),
        r"\1: <HOST_REDACTED>",
    ),
    (
        re.compile(r"\b[0-9A-Fa-f]{16,}\b"),
        "<HEX_IDENTIFIER_REDACTED>",
    ),
)


def sanitize_text(text: str) -> str:
    """Mask common sensitive identifiers in text.

    Args:
        text: Raw diagnostic text.

    Returns:
        Sanitized text.
    """

    sanitized = text
    for pattern, replacement in SANITIZER_PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized


def iter_text_files(input_dir: Path) -> Iterable[Path]:
    """Yield text-like files under a directory.

    Args:
        input_dir: Directory to scan.

    Yields:
        Candidate text file paths.
    """

    for path in sorted(input_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in {"", ".txt", ".log", ".json", ".md"}:
            yield path


def sanitize_directory(input_dir: Path, output_dir: Path) -> int:
    """Sanitize a directory while preserving relative paths.

    Args:
        input_dir: Source directory.
        output_dir: Destination directory.

    Returns:
        Number of sanitized text files.
    """

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    ensure_directory(output_dir)

    sanitized_count = 0
    text_files_set = set(iter_text_files(input_dir))

    for source_path in sorted(input_dir.rglob("*")):
        relative_path = source_path.relative_to(input_dir)
        destination_path = output_dir / relative_path

        if source_path.is_dir():
            ensure_directory(destination_path)
            continue

        ensure_directory(destination_path.parent)
        if source_path in text_files_set:
            destination_path.write_text(
                sanitize_text(read_text(source_path)),
                encoding="utf-8",
            )
            sanitized_count += 1
        else:
            shutil.copy2(source_path, destination_path)

    return sanitized_count
