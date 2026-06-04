"""Archive creation helpers."""

from __future__ import annotations

import tarfile
from pathlib import Path


def create_tar_gz(input_dir: Path, output_path: Path) -> Path:
    """Create a gzip-compressed tar archive.

    Args:
        input_dir: Directory to archive.
        output_path: Destination `.tar.gz` path.

    Returns:
        Archive path pointing to the created compressed file.

    Raises:
        FileNotFoundError: If the input directory does not exist.
        NotADirectoryError: If the input path is not a directory.
        ValueError: If the output path does not end with `.tar.gz`.
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_dir}")
    if output_path.suffixes[-2:] != [".tar", ".gz"]:
        raise ValueError("Output path must end with .tar.gz")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(input_dir, arcname=input_dir.name)

    return output_path
