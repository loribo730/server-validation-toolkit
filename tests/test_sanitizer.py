"""Tests for log sanitization."""

from __future__ import annotations

from server_validation_toolkit.sanitizer import sanitize_text


def test_sanitize_ipv4_mac_uuid_and_serial() -> None:
    raw = """
    host ip: 192.168.100.25
    mac: AA:BB:CC:DD:EE:FF
    UUID: 123e4567-e89b-12d3-a456-426614174000
    Serial Number: ABC123456789
    hostname: lab-server-01
    token: 0123456789abcdef0123456789abcdef
    """

    sanitized = sanitize_text(raw)

    assert "192.168.100.25" not in sanitized
    assert "AA:BB:CC:DD:EE:FF" not in sanitized
    assert "123e4567-e89b-12d3-a456-426614174000" not in sanitized
    assert "ABC123456789" not in sanitized
    assert "lab-server-01" not in sanitized
    assert "0123456789abcdef0123456789abcdef" not in sanitized
    assert "<IPv4_REDACTED>" in sanitized
    assert "<MAC_REDACTED>" in sanitized


def test_sanitize_directory_scans_text_files_once(tmp_path, monkeypatch) -> None:
    """Verify directory text file discovery is not repeated per file."""

    from server_validation_toolkit import sanitizer

    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()

    for index in range(5):
        (input_dir / f"file_{index}.txt").write_text(
            f"serial=abc{index}\n",
            encoding="utf-8",
        )

    call_count = 0
    original_iter_text_files = sanitizer.iter_text_files

    def counted_iter_text_files(path):
        nonlocal call_count
        call_count += 1
        yield from original_iter_text_files(path)

    monkeypatch.setattr(sanitizer, "iter_text_files", counted_iter_text_files)

    sanitized_count = sanitizer.sanitize_directory(input_dir, output_dir)

    assert sanitized_count == 5
    assert call_count == 1
