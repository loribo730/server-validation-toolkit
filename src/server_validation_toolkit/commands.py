"""Default diagnostic command profile.

The command set intentionally uses generic Ubuntu/Linux tools only.
"""

from __future__ import annotations

from server_validation_toolkit.models import CommandSpec

DEFAULT_COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec("uname_a", ("uname", "-a")),
    CommandSpec("os_release", ("cat", "/etc/os-release")),
    CommandSpec("lsb_release_a", ("lsb_release", "-a")),
    CommandSpec("lscpu", ("lscpu",)),
    CommandSpec("free_h", ("free", "-h")),
    CommandSpec(
        "lsblk",
        (
            "lsblk",
            "-o",
            "NAME,MODEL,SERIAL,SIZE,TYPE,MOUNTPOINT,FSTYPE,TRAN,VENDOR",
        ),
    ),
    CommandSpec(
        "lsblk_json",
        (
            "lsblk",
            "-J",
            "-o",
            "NAME,MODEL,SERIAL,SIZE,TYPE,MOUNTPOINT,FSTYPE,TRAN,VENDOR",
        ),
    ),
    CommandSpec("lspci_nn", ("lspci", "-nn")),
    CommandSpec("lspci_nnvv", ("lspci", "-nnvv"), timeout_seconds=60),
    CommandSpec("lsusb_tv", ("lsusb", "-tv")),
    CommandSpec("nvme_list", ("nvme", "list")),
    CommandSpec("smartctl_scan", ("smartctl", "--scan")),
    CommandSpec("dmidecode_system", ("dmidecode", "-t", "system")),
    CommandSpec("dmidecode_bios", ("dmidecode", "-t", "bios")),
    CommandSpec("ipmitool_mc_info", ("ipmitool", "mc", "info")),
    CommandSpec("ipmitool_sensor_list", ("ipmitool", "sensor", "list"), timeout_seconds=60),
    CommandSpec("ipmitool_sel_elist", ("ipmitool", "sel", "elist"), timeout_seconds=60),
    CommandSpec("dmesg_time", ("dmesg", "-T"), timeout_seconds=60),
)
