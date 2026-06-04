# Release Checklist

Use this checklist before publishing a new release.

## Code quality

```bash
ruff check .
pytest -q
```

## CLI smoke test

```bash
svt --version
svt collect --sanitize --output ./test_run_logs
svt pcie-summary --input ./test_run_logs/lspci_nnvv.txt
svt storage-summary --input ./test_run_logs/lsblk.txt
svt ipmi-summary --input ./test_run_logs/ipmitool_sensor_list.txt
svt report --input ./test_run_logs --output ./diagnostic_report.md
svt package --input ./test_run_logs --output diagnostic_bundle.tar.gz
```

## Privacy check

Confirm no private organization names, customer names, hostnames, asset tags, serial numbers,
MAC addresses, IP addresses, credentials, or internal platform names are committed.
