# server-validation-toolkit

`server-validation-toolkit` is a lightweight Ubuntu Server diagnostic collection toolkit for hardware validation, lab debugging, reproducible log capture, safe log sharing, and Markdown report generation.

It is designed for public open-source use. It does **not** contain company-specific platform data, customer logs, private hardware topology, internal firmware versions, proprietary validation procedures, or non-English documentation.

## Features

- Collect common Ubuntu Server diagnostic logs.
- Capture PCIe, USB, storage, NVMe, CPU, memory, OS, and BMC/IPMI snapshots.
- Sanitize sensitive identifiers before logs are shared.
- Package collected logs into a `.tar.gz` bundle.
- Generate PCIe, storage, and IPMI Markdown summaries.
- Build a combined Markdown diagnostic report from collected logs.

## Safety boundary

This toolkit does not:

- Flash firmware.
- Change BIOS or BMC settings.
- Reboot the system.
- Power-cycle the system.
- Upload logs to any external service.
- Include vendor-private validation logic.

## Supported environment

Target environment:

- Ubuntu 22.04 LTS
- Ubuntu 24.04 LTS
- Python 3.10+

Optional system tools:

```bash
sudo apt update
sudo apt install -y pciutils usbutils dmidecode ipmitool nvme-cli smartmontools util-linux
```

## Installation for development

```bash
git clone https://github.com/YOUR_NAME/server-validation-toolkit.git
cd server-validation-toolkit
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## CLI usage

```bash
svt collect --output ./logs
svt collect --sanitize --output ./logs
svt sanitize --input ./logs --output ./logs_sanitized
svt package --input ./logs_sanitized --output diagnostic_bundle.tar.gz
svt pcie-summary --input ./logs_sanitized/lspci_nnvv.txt
svt storage-summary --input ./logs_sanitized/lsblk.txt
svt ipmi-summary --input ./logs_sanitized/ipmitool_sensor_list.txt
svt report --input ./logs_sanitized --output diagnostic_report.md
```

## Data safety

The sanitizer masks common sensitive data patterns:

- IPv4 addresses
- MAC addresses
- UUID-like identifiers
- Long serial-like hexadecimal values
- Hostname lines
- Product serial lines from common hardware tools

Sanitization is best-effort. Review logs before sharing them publicly.

## Known limitations

- Best-effort sanitization: The sanitizer uses regular-expression heuristics and cannot guarantee masking every non-standard vendor asset tag or proprietary serial format.
- Root privileges: Commands such as `dmidecode` and `smartctl` may require `sudo`; otherwise, the collected output may contain command errors instead of hardware data.
- Hardware dependency: IPMI snapshots require a working local BMC interface and Linux IPMI drivers such as `ipmi_devintf` and `ipmi_si`.
- Parser scope: PCIe, storage, and IPMI parsers target common Linux command output. Corrupted or heavily modified logs may not produce complete records.
- No destructive actions: The toolkit intentionally avoids firmware flashing, reboot, power cycle, and remote upload behavior.

## Verification

```bash
ruff check .
pytest -q
svt --version
svt collect --sanitize --output ./test_run_logs
svt pcie-summary --input ./test_run_logs/lspci_nnvv.txt
svt storage-summary --input ./test_run_logs/lsblk.txt
svt ipmi-summary --input ./test_run_logs/ipmitool_sensor_list.txt
svt report --input ./test_run_logs --output ./diagnostic_report.md
svt package --input ./test_run_logs --output diagnostic_bundle.tar.gz
```


## AI-assisted maintenance

This project may use AI coding agents, including Codex, to assist with issue triage, parser test generation, synthetic example data, changelog drafting, release checklist review, and safe refactoring.

All AI-assisted changes must remain public-safe, pass tests and CI, and be reviewed by a human maintainer before merge.

See [AI maintenance workflow](docs/ai_maintenance_workflow.md) for the project policy.

## Roadmap

- v1.0.0: Public release baseline with collect, sanitize, package, PCIe summary, storage summary, IPMI summary, and combined report generation.
- v1.1.0: Optional plugin-based command profiles.
- v1.2.0: Optional JSON report export.

## License

MIT License.

## Usage examples

Collect diagnostic logs into a local output directory:

    svt collect --output ./svt-output

Sanitize collected logs before sharing:

    svt sanitize ./svt-output --output ./svt-sanitized

Create a compressed diagnostic bundle:

    svt package ./svt-sanitized --output ./svt-bundle.tar.gz

Generate a PCIe summary:

    svt pcie-summary ./svt-sanitized/lspci.txt --output ./pcie-summary.md

Generate a storage summary:

    svt storage-summary ./svt-sanitized/lsblk.txt --output ./storage-summary.md

Generate an IPMI sensor summary:

    svt ipmi-summary ./svt-sanitized/ipmi_sensor.txt --output ./ipmi-summary.md

Generate a combined Markdown report:

    svt report ./svt-sanitized --output ./report.md
