"""Tests for diagnostic collection workflow."""

from __future__ import annotations

from pathlib import Path

from server_validation_toolkit.collector import collect_logs
from server_validation_toolkit.models import CommandSpec


def test_collect_logs_sanitize_uses_shutil_move(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Verify sanitize flow uses shutil.move for safer path movement."""

    moved_paths: list[tuple[str, str]] = []

    def fake_move(source: str, destination: str) -> str:
        moved_paths.append((source, destination))
        Path(source).rename(destination)
        return destination

    monkeypatch.setattr("server_validation_toolkit.collector.shutil.move", fake_move)

    output_dir = tmp_path / "logs"
    summary = collect_logs(
        output_dir,
        sanitize=True,
        command_specs=(
            CommandSpec(
                "echo_test",
                ("python3", "-c", "print('serial=abc123456789')"),
            ),
        ),
    )

    assert summary.output_dir == output_dir
    assert moved_paths
    assert (output_dir / "echo_test.txt").exists()
    assert "abc123456789" not in (output_dir / "echo_test.txt").read_text(
        encoding="utf-8"
    )
