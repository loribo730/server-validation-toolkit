# Sanitized diagnostic bundle example

        This directory contains a small public-safe example diagnostic bundle for `server-validation-toolkit`.

        It demonstrates sanitized diagnostic logs, generated PCIe/storage/IPMI summaries, a final combined Markdown report, and a compressed `.tar.gz` diagnostic bundle.

        All sample data is synthetic. It does not contain real serial numbers, MAC addresses, IP addresses, hostnames, customer names, private hardware topology, internal firmware versions, or vendor-private validation data.

        ## Contents

        - `logs/manifest.json`
        - `logs/lspci_nnvv.txt`
        - `logs/lsblk_json.txt`
        - `logs/ipmitool_sensor_list.txt`
        - `summaries/pcie_summary.md`
        - `summaries/storage_summary.md`
        - `summaries/ipmi_summary.md`
        - `diagnostic_report.md`
        