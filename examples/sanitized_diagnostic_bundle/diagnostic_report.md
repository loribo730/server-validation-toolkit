# Server Validation Diagnostic Report

This report is generated from local diagnostic logs.
Review the original files before sharing publicly.

## Manifest

| Field | Value |
|---|---|
| Created at UTC | 2026-01-01T00:00:00Z |
| Tool | server-validation-toolkit |
| Platform | example-ubuntu-server |
| Python | 3.12.0 |
| Total commands | 4 |
| Skipped commands | 0 |
| Failed commands | 0 |


## PCIe Summary

| BDF | Current | Capability | Device |
|---|---:|---:|---|
| `00:01.0` | 16GT/s / x8 | 8GT/s / x4 | PCI bridge [0604]: Example Root Port [1234:1000] |


## Storage Summary

| Device | Size | Transport | Model |
|---|---:|---|---|
| `sda` | 960G | SATA | Example SATA SSD |
| `nvme0n1` | 1.9T | NVME | Example NVMe SSD |


## IPMI Sensor Summary

| Sensor | Reading | Unit | Status |
|---|---:|---|---|
| CPU Temp | 42.000 | degrees C | ok |
| System Temp | 31.000 | degrees C | ok |
| Fan1 | 7200.000 | RPM | ok |
| Fan2 | 7100.000 | RPM | ok |
| Voltage 12V | 12.100 | Volts | ok |
