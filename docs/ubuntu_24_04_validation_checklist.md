# Ubuntu 24.04 Real-Machine Validation Checklist

This checklist is used to validate server-validation-toolkit on Ubuntu 24.04 LTS real hardware without exposing private or vendor-specific data.

## Scope

The validation should confirm that the toolkit can:

- Collect diagnostic logs.
- Sanitize sensitive identifiers.
- Package sanitized logs.
- Generate PCIe, storage, and IPMI summaries.
- Generate a combined Markdown report.

## Environment

Record only public-safe environment details:

- Ubuntu version.
- Kernel version.
- Python version.
- server-validation-toolkit version.
- Whether local BMC/IPMI access is available.

Do not record:

- Serial numbers.
- MAC addresses.
- IP addresses.
- Hostnames.
- Customer names.
- Vendor-private hardware topology.
- Internal SOP content.
- Private firmware or BIOS release identifiers.

## Pre-checks

Run:

    python3 --version
    svt --version
    lspci --version
    lsblk --version

Optional, if IPMI is available:

    ipmitool -V

## Collection test

Run:

    svt collect --output ./svt-output

Expected result:

- The output directory is created.
- Command outputs are saved.
- Missing optional tools are reported as command errors instead of crashing the toolkit.

## Sanitization test

Run:

    svt sanitize ./svt-output --output ./svt-sanitized

Expected result:

- A sanitized output directory is created.
- Sensitive identifiers are redacted where recognized.
- The original collected directory is not modified.

## Summary generation test

Run:

    svt pcie-summary ./svt-sanitized/lspci.txt --output ./pcie-summary.md
    svt storage-summary ./svt-sanitized/lsblk.txt --output ./storage-summary.md
    svt ipmi-summary ./svt-sanitized/ipmi_sensor.txt --output ./ipmi-summary.md

Expected result:

- Markdown summary files are generated.
- Missing or incomplete logs are handled without destructive behavior.
- No private identifiers are introduced into generated summaries.

## Report generation test

Run:

    svt report ./svt-sanitized --output ./report.md

Expected result:

- A combined Markdown report is generated.
- Report content remains public-safe after sanitization review.

## Package test

Run:

    svt package ./svt-sanitized --output ./svt-bundle.tar.gz

Expected result:

- A compressed diagnostic bundle is created.
- The bundle contains sanitized content only.

## Final privacy review

Before sharing any output, manually inspect:

- Raw logs.
- Sanitized logs.
- Markdown summaries.
- Final report.
- Compressed bundle content.

The sanitizer is best-effort and does not replace human review.
