"""Tests for archive creation."""

from __future__ import annotations

import tarfile
from pathlib import Path

from server_validation_toolkit.archive import create_tar_gz


def test_create_tar_gz(tmp_path: Path) -> None:
    input_dir = tmp_path / "logs"
    input_dir.mkdir()
    (input_dir / "sample.txt").write_text("hello\n", encoding="utf-8")

    output_path = tmp_path / "bundle.tar.gz"
    result = create_tar_gz(input_dir, output_path)

    assert result == output_path
    assert output_path.exists()

    with tarfile.open(output_path, "r:gz") as tar:
        names = tar.getnames()

    assert "logs/sample.txt" in names
