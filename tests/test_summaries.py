"""Tests for hardware diagnostic summary parsers."""

from __future__ import annotations

from pathlib import Path

from server_validation_toolkit.summaries import (
    build_markdown_report,
    format_storage_summary,
    parse_ipmi_sensors,
    parse_lsblk_disks,
    parse_lspci_links,
)


def test_parse_lspci_links() -> None:
    """Verify standard lspci output link capabilities are correctly matched."""

    raw = """
00:01.0 PCI bridge [0604]: Example Device [1234:5678]
        LnkCap: Port #0, Speed 32GT/s, Width x16, ASPM L1
        LnkSta: Speed 16GT/s, Width x8
01:00.0 Non-Volatile memory controller [0108]: Example NVMe [abcd:0001]
        LnkCap: Port #0, Speed 16GT/s, Width x4
        LnkSta: Speed 16GT/s, Width x4
    """

    records = parse_lspci_links(raw)

    assert len(records) == 2
    assert records[0].bdf == "00:01.0"
    assert records[0].capability_speed == "32GT/s"
    assert records[0].capability_width == "x16"
    assert records[0].status_speed == "16GT/s"
    assert records[0].status_width == "x8"


def test_parse_lsblk_text_with_redacted_identifiers() -> None:
    """Verify sanitizer-redacted lsblk text maps storage attributes."""

    raw = """
$ lsblk -o NAME,MODEL,SERIAL,SIZE,TYPE,MOUNTPOINT,FSTYPE,TRAN,VENDOR
return_code: 0
----- stdout -----
NAME   MODEL            SERIAL            SIZE TYPE MOUNTPOINT FSTYPE TRAN   VENDOR
sda    SAMSUNG MZ7L31T9 <IDENTIFIER_REDACTED>   1.8T disk                     sata   ATA
└─sda1                                   1.8T part /mnt/data  ext4
nvme0n1 Micron 7450 Pro  <IDENTIFIER_REDACTED> 931.5G disk                     pcie   NVME
----- stderr -----
    """

    records = parse_lsblk_disks(raw)

    assert len(records) == 2
    assert records[0].name == "sda"
    assert records[0].model == "SAMSUNG MZ7L31T9"
    assert records[0].size == "1.8T"
    assert records[0].transport == "SATA"
    assert records[1].name == "nvme0n1"
    assert records[1].model == "Micron 7450 Pro"
    assert records[1].size == "931.5G"
    assert records[1].transport == "PCIE"


def test_parse_lsblk_json() -> None:
    """Verify lsblk JSON output is parsed when available."""

    raw = """
$ lsblk -J -o NAME,MODEL,SERIAL,SIZE,TYPE,MOUNTPOINT,FSTYPE,TRAN,VENDOR
return_code: 0
----- stdout -----
{
  "blockdevices": [
    {"name": "sda", "model": "Generic SSD", "size": "1.0T", "type": "disk", "tran": "sata"},
    {"name": "sda1", "size": "1.0T", "type": "part"},
    {"name": "nvme0n1", "model": "NVMe Drive", "size": "3.5T", "type": "disk", "tran": "pcie"}
  ]
}
----- stderr -----
    """

    records = parse_lsblk_disks(raw)

    assert len(records) == 2
    assert records[0].name == "sda"
    assert records[0].model == "Generic SSD"
    assert records[0].transport == "SATA"
    assert records[1].name == "nvme0n1"
    assert records[1].transport == "PCIE"


def test_format_storage_summary_escapes_markdown_separator() -> None:
    """Verify Markdown table output remains valid for unusual model names."""

    raw = """
NAME   MODEL            SERIAL            SIZE TYPE MOUNTPOINT FSTYPE TRAN   VENDOR
sda    Model|WithPipe   <IDENTIFIER_REDACTED>   1.8T disk                     sata   ATA
    """

    summary = format_storage_summary(parse_lsblk_disks(raw))

    assert "Model\\|WithPipe" in summary


def test_parse_ipmi_sensors() -> None:
    """Verify basic ipmitool sensor list rows are parsed."""

    raw = """
$ ipmitool sensor list
return_code: 0
----- stdout -----
CPU Temp         | 42.000     | degrees C  | ok
Fan1             | 7800.000   | RPM        | ok
P12V             | 12.100     | Volts      | ok
----- stderr -----
    """

    records = parse_ipmi_sensors(raw)

    assert len(records) == 3
    assert records[0].name == "CPU Temp"
    assert records[0].value == "42.000"
    assert records[0].unit == "degrees C"
    assert records[0].status == "ok"


def test_build_markdown_report(tmp_path: Path) -> None:
    """Verify combined report includes available summaries."""

    input_dir = tmp_path / "logs"
    input_dir.mkdir()
    (input_dir / "manifest.json").write_text(
        '{"tool": "server-validation-toolkit", "total_commands": 1}',
        encoding="utf-8",
    )
    (input_dir / "lsblk.txt").write_text(
        "sda GenericSSD <IDENTIFIER_REDACTED> 1.0T disk sata\n",
        encoding="utf-8",
    )
    (input_dir / "ipmitool_sensor_list.txt").write_text(
        "CPU Temp | 42.000 | degrees C | ok\n",
        encoding="utf-8",
    )

    report = build_markdown_report(input_dir)

    assert "# Server Validation Diagnostic Report" in report
    assert "## Manifest" in report
    assert "## Storage Summary" in report
    assert "## IPMI Sensor Summary" in report


def test_parse_lsblk_text_without_serial_column() -> None:
    """Verify model text is preserved when the SERIAL column is empty."""

    raw = "sda SAMSUNG 1.8T disk sata ATA"
    records = parse_lsblk_disks(raw)

    assert len(records) == 1
    assert records[0].name == "sda"
    assert records[0].model == "SAMSUNG"
    assert records[0].size == "1.8T"
    assert records[0].transport == "SATA"


def test_parse_lsblk_text_removes_redacted_serial_placeholder() -> None:
    """Verify redacted serial placeholders are not included in the model text."""

    raw = "sda SAMSUNG MZ7L31T9 <IDENTIFIER_REDACTED> 1.8T disk sata ATA"
    records = parse_lsblk_disks(raw)

    assert len(records) == 1
    assert records[0].model == "SAMSUNG MZ7L31T9"

def test_parse_lspci_links_with_missing_link_fields() -> None:
    """Verify devices without link capability or status fields remain parseable."""

    raw = """
02:00.0 Ethernet controller [0200]: Example Network Adapter [1234:1000]
03:00.0 PCI bridge [0604]: Example PCIe Bridge [1234:2000]
        LnkCap: Port #1, Speed 8GT/s, Width x4, ASPM L0s L1
    """

    records = parse_lspci_links(raw)

    assert len(records) == 2
    assert records[0].bdf == "02:00.0"
    assert records[0].capability_speed is None
    assert records[0].capability_width is None
    assert records[0].status_speed is None
    assert records[0].status_width is None
    assert records[1].bdf == "03:00.0"
    assert records[1].capability_speed == "8GT/s"
    assert records[1].capability_width == "x4"
    assert records[1].status_speed is None
    assert records[1].status_width is None


def test_parse_lspci_links_with_redacted_description_identifiers() -> None:
    """Verify sanitized or redacted description text does not break PCIe parsing."""

    raw = """
04:00.0 Non-Volatile memory controller [0108]: Example NVMe <IDENTIFIER_REDACTED>
        LnkCap: Port #0, Speed 16GT/s, Width x4, ASPM L1
        LnkSta: Speed 16GT/s, Width x4
    """

    records = parse_lspci_links(raw)

    assert len(records) == 1
    assert records[0].bdf == "04:00.0"
    assert "<IDENTIFIER_REDACTED>" in records[0].description
    assert records[0].capability_speed == "16GT/s"
    assert records[0].capability_width == "x4"
    assert records[0].status_speed == "16GT/s"
    assert records[0].status_width == "x4"


def test_parse_lspci_links_with_domain_prefixed_bdf() -> None:
    """Verify lspci -D style domain-prefixed BDF addresses are supported."""

    raw = """
0000:05:00.0 PCI bridge [0604]: Example Root Port [1234:3000]
        LnkCap: Port #2, Speed 32GT/s, Width x16, ASPM L1
        LnkSta: Speed 32GT/s, Width x16
    """

    records = parse_lspci_links(raw)

    assert len(records) == 1
    assert records[0].bdf == "0000:05:00.0"
    assert records[0].description.startswith("PCI bridge")
    assert records[0].capability_speed == "32GT/s"
    assert records[0].capability_width == "x16"
    assert records[0].status_speed == "32GT/s"
    assert records[0].status_width == "x16"


def test_parse_lspci_links_preserves_degraded_link_width_and_speed() -> None:
    """Verify negotiated link speed and width can be lower than capability."""

    raw = """
06:00.0 3D controller [0302]: Example Accelerator [1234:4000]
        LnkCap: Port #0, Speed 32GT/s, Width x16, ASPM L1
        LnkSta: Speed 2.5GT/s (downgraded), Width x1 (downgraded)
    """

    records = parse_lspci_links(raw)

    assert len(records) == 1
    assert records[0].bdf == "06:00.0"
    assert records[0].capability_speed == "32GT/s"
    assert records[0].capability_width == "x16"
    assert records[0].status_speed == "2.5GT/s (downgraded)"
    assert records[0].status_width == "x1"
