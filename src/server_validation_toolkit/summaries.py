"""Summary parsers for collected diagnostic logs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from server_validation_toolkit.utils import read_text


@dataclass(frozen=True)
class PcieLinkRecord:
    """Represent one PCIe link record.

    Args:
        bdf: PCIe bus-device-function address.
        description: Device description line.
        capability_speed: Advertised maximum link speed.
        capability_width: Advertised maximum link width.
        status_speed: Current link speed.
        status_width: Current link width.
    """

    bdf: str
    description: str
    capability_speed: str | None
    capability_width: str | None
    status_speed: str | None
    status_width: str | None


@dataclass(frozen=True)
class StorageDeviceRecord:
    """Represent one block storage device record.

    Args:
        name: Block device node name.
        model: Device model text.
        size: Capacity text.
        transport: Storage transport text.
    """

    name: str
    model: str
    size: str
    transport: str


@dataclass(frozen=True)
class IpmiSensorRecord:
    """Represent one IPMI sensor record.

    Args:
        name: Sensor name.
        value: Sensor reading value.
        unit: Sensor unit.
        status: Sensor status text.
    """

    name: str
    value: str
    unit: str
    status: str


BDF_LINE_PATTERN = re.compile(r"^(?P<bdf>[0-9a-fA-F]{2}:[0-9a-fA-F]{2}\.[0-7])\s+(?P<desc>.+)$")
LNKCAP_PATTERN = re.compile(r"LnkCap:.*Speed\s+(?P<speed>[^,]+),\s+Width\s+(?P<width>x\d+)")
LNKSTA_PATTERN = re.compile(r"LnkSta:.*Speed\s+(?P<speed>[^,]+),\s+Width\s+(?P<width>x\d+)")
SIZE_PATTERN = re.compile(r"^\d+(?:\.\d+)?[KMGTP]?$", re.IGNORECASE)
STORAGE_TRANSPORTS = {"sata", "pcie", "usb", "nvme", "sas", "spi", "mmc", "virtio"}


def parse_lspci_links(text: str) -> list[PcieLinkRecord]:
    """Parse basic PCIe link capability and status records from lspci output.

    Args:
        text: Raw `lspci -nnvv` text.

    Returns:
        Parsed PCIe link records.
    """

    records: list[PcieLinkRecord] = []
    current_bdf: str | None = None
    current_desc: str | None = None
    capability_speed: str | None = None
    capability_width: str | None = None
    status_speed: str | None = None
    status_width: str | None = None

    def flush_current() -> None:
        if current_bdf and current_desc:
            records.append(
                PcieLinkRecord(
                    bdf=current_bdf,
                    description=current_desc,
                    capability_speed=capability_speed,
                    capability_width=capability_width,
                    status_speed=status_speed,
                    status_width=status_width,
                )
            )

    for line in text.splitlines():
        bdf_match = BDF_LINE_PATTERN.match(line)
        if bdf_match:
            flush_current()
            current_bdf = bdf_match.group("bdf")
            current_desc = bdf_match.group("desc")
            capability_speed = None
            capability_width = None
            status_speed = None
            status_width = None
            continue

        cap_match = LNKCAP_PATTERN.search(line)
        if cap_match:
            capability_speed = cap_match.group("speed").strip()
            capability_width = cap_match.group("width").strip()
            continue

        status_match = LNKSTA_PATTERN.search(line)
        if status_match:
            status_speed = status_match.group("speed").strip()
            status_width = status_match.group("width").strip()

    flush_current()
    return records


def format_pcie_summary(records: list[PcieLinkRecord]) -> str:
    """Format PCIe records as a Markdown table.

    Args:
        records: PCIe link records.

    Returns:
        Markdown table text.
    """

    lines = [
        "| BDF | Current | Capability | Device |",
        "|---|---:|---:|---|",
    ]

    for record in records:
        current = _format_link(record.status_speed, record.status_width)
        capability = _format_link(record.capability_speed, record.capability_width)
        lines.append(
            f"| `{_escape_markdown(record.bdf)}` | {current} | "
            f"{capability} | {_escape_markdown(record.description)} |"
        )

    return "\n".join(lines) + "\n"


def summarize_pcie_file(input_path: Path) -> str:
    """Read an lspci file and return a PCIe Markdown summary.

    Args:
        input_path: Path to `lspci -nnvv` output.

    Returns:
        Markdown table summary.
    """

    return format_pcie_summary(parse_lspci_links(read_text(input_path)))


def parse_lsblk_disks(text: str) -> list[StorageDeviceRecord]:
    """Parse block storage root disk records from collected lsblk text.

    Args:
        text: Raw collected `lsblk` command output.

    Returns:
        Storage records for root block devices with TYPE `disk`.
    """

    json_records = _try_parse_lsblk_json(text)
    if json_records:
        return json_records

    records: list[StorageDeviceRecord] = []

    for line in text.splitlines():
        tokens = line.split()
        if "disk" not in tokens:
            continue

        disk_index = tokens.index("disk")
        if disk_index < 2:
            continue

        size_index = _find_size_index(tokens, disk_index)
        if size_index is None:
            continue

        name = _clean_tree_prefix(tokens[0])
        size = tokens[size_index]
        transport = _find_transport(tokens[disk_index + 1 :])
        model_tokens = [
            token
            for token in tokens[1:size_index]
            if not (token.startswith("<") and token.endswith(">") and "REDACTED" in token)
        ]
        model = " ".join(model_tokens).strip() or "Unknown"

        records.append(
            StorageDeviceRecord(
                name=name,
                model=model,
                size=size,
                transport=transport,
            )
        )

    return records


def format_storage_summary(records: list[StorageDeviceRecord]) -> str:
    """Format storage records as a Markdown table.

    Args:
        records: Storage device records.

    Returns:
        Markdown table text.
    """

    lines = [
        "| Device | Size | Transport | Model |",
        "|---|---:|---|---|",
    ]

    for record in records:
        lines.append(
            f"| `{_escape_markdown(record.name)}` | {_escape_markdown(record.size)} | "
            f"{_escape_markdown(record.transport)} | {_escape_markdown(record.model)} |"
        )

    return "\n".join(lines) + "\n"


def summarize_storage_file(input_path: Path) -> str:
    """Read an lsblk log file and return a storage Markdown summary.

    Args:
        input_path: Path to collected `lsblk` output.

    Returns:
        Markdown table summary.
    """

    return format_storage_summary(parse_lsblk_disks(read_text(input_path)))


def parse_ipmi_sensors(text: str) -> list[IpmiSensorRecord]:
    """Parse IPMI sensor records from `ipmitool sensor list` text.

    Args:
        text: Raw collected `ipmitool sensor list` output.

    Returns:
        Parsed IPMI sensor records.
    """

    records: list[IpmiSensorRecord] = []

    for line in text.splitlines():
        if "|" not in line:
            continue

        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 4:
            continue

        name, value, unit, status = parts[:4]
        if not name or name.startswith("$") or name.lower() in {"sensor", "name"}:
            continue

        records.append(
            IpmiSensorRecord(
                name=name,
                value=value or "N/A",
                unit=unit or "N/A",
                status=status or "N/A",
            )
        )

    return records


def format_ipmi_summary(records: list[IpmiSensorRecord]) -> str:
    """Format IPMI sensor records as a Markdown table.

    Args:
        records: IPMI sensor records.

    Returns:
        Markdown table text.
    """

    lines = [
        "| Sensor | Reading | Unit | Status |",
        "|---|---:|---|---|",
    ]

    for record in records:
        lines.append(
            f"| {_escape_markdown(record.name)} | {_escape_markdown(record.value)} | "
            f"{_escape_markdown(record.unit)} | {_escape_markdown(record.status)} |"
        )

    return "\n".join(lines) + "\n"


def summarize_ipmi_file(input_path: Path) -> str:
    """Read an IPMI sensor log and return a Markdown summary.

    Args:
        input_path: Path to collected `ipmitool sensor list` output.

    Returns:
        Markdown table summary.
    """

    return format_ipmi_summary(parse_ipmi_sensors(read_text(input_path)))


def build_markdown_report(input_dir: Path) -> str:
    """Build a combined Markdown report from a collected log directory.

    Args:
        input_dir: Directory containing collected diagnostic logs.

    Returns:
        Combined Markdown report.

    Raises:
        FileNotFoundError: If the input directory does not exist.
        NotADirectoryError: If the input path is not a directory.
    """

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_dir}")

    lines = [
        "# Server Validation Diagnostic Report",
        "",
        "This report is generated from local diagnostic logs.",
        "Review the original files before sharing publicly.",
        "",
    ]

    manifest_path = input_dir / "manifest.json"
    if manifest_path.exists():
        lines.extend(["## Manifest", "", _format_manifest(manifest_path), ""])

    pcie_path = input_dir / "lspci_nnvv.txt"
    if pcie_path.exists():
        lines.extend(["## PCIe Summary", "", summarize_pcie_file(pcie_path), ""])

    storage_path = input_dir / "lsblk_json.txt"
    if not storage_path.exists():
        storage_path = input_dir / "lsblk.txt"
    if storage_path.exists():
        lines.extend(["## Storage Summary", "", summarize_storage_file(storage_path), ""])

    ipmi_path = input_dir / "ipmitool_sensor_list.txt"
    if ipmi_path.exists():
        lines.extend(["## IPMI Sensor Summary", "", summarize_ipmi_file(ipmi_path), ""])

    return "\n".join(lines).rstrip() + "\n"


def _try_parse_lsblk_json(text: str) -> list[StorageDeviceRecord]:
    """Parse lsblk JSON output when a JSON object is present."""

    json_start = text.find("{")
    if json_start < 0:
        return []

    try:
        payload, _ = json.JSONDecoder().raw_decode(text[json_start:])
    except json.JSONDecodeError:
        return []

    block_devices = payload.get("blockdevices")
    if not isinstance(block_devices, list):
        return []

    records: list[StorageDeviceRecord] = []
    for device in _walk_blockdevices(block_devices):
        if device.get("type") != "disk":
            continue

        records.append(
            StorageDeviceRecord(
                name=str(device.get("name") or "Unknown"),
                model=str(device.get("model") or "Unknown").strip() or "Unknown",
                size=str(device.get("size") or "Unknown"),
                transport=str(device.get("tran") or "N/A").upper(),
            )
        )

    return records


def _walk_blockdevices(devices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return flattened block devices from lsblk JSON."""

    flattened: list[dict[str, Any]] = []
    for device in devices:
        flattened.append(device)
        children = device.get("children")
        if isinstance(children, list):
            flattened.extend(_walk_blockdevices(children))
    return flattened


def _find_size_index(tokens: list[str], disk_index: int) -> int | None:
    """Find the size token before the disk type token."""

    for index in range(disk_index - 1, 0, -1):
        if SIZE_PATTERN.match(tokens[index]):
            return index
    return None


def _find_transport(tokens: list[str]) -> str:
    """Find the first known storage transport token."""

    for token in tokens:
        normalized = token.lower()
        if normalized in STORAGE_TRANSPORTS:
            return normalized.upper()
    return "N/A"


def _format_link(speed: str | None, width: str | None) -> str:
    """Format speed and width values."""

    if not speed and not width:
        return "N/A"
    return f"{speed or 'N/A'} / {width or 'N/A'}"


def _format_manifest(manifest_path: Path) -> str:
    """Format selected manifest fields as a Markdown table."""

    try:
        manifest = json.loads(read_text(manifest_path))
    except json.JSONDecodeError:
        return "_Manifest could not be parsed._\n"

    rows = [
        ("Created at UTC", manifest.get("created_at_utc", "N/A")),
        ("Tool", manifest.get("tool", "N/A")),
        ("Platform", manifest.get("platform", "N/A")),
        ("Python", manifest.get("python_version", "N/A")),
        ("Total commands", manifest.get("total_commands", "N/A")),
        ("Skipped commands", manifest.get("skipped_commands", "N/A")),
        ("Failed commands", manifest.get("failed_commands", "N/A")),
    ]

    lines = ["| Field | Value |", "|---|---|"]
    for field, value in rows:
        lines.append(f"| {_escape_markdown(str(field))} | {_escape_markdown(str(value))} |")
    return "\n".join(lines) + "\n"


def _clean_tree_prefix(text: str) -> str:
    """Remove lsblk tree drawing prefixes from a device token."""

    return re.sub(r"^[├└│`\-─ ]+", "", text)


def _escape_markdown(text: str) -> str:
    """Escape Markdown table separator characters."""

    return text.replace("|", "\\|")
