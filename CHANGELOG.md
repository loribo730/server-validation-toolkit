# Changelog

        All notable public-safe changes to `server-validation-toolkit` are documented in this file.

        This project follows a simple release-note format focused on hardware validation utility, safety boundaries, parser behavior, documentation, and maintenance workflow.

        ## [Unreleased]

        Planned maintenance areas:

        - Improve parser coverage for additional Linux diagnostic output variants.
        - Add more public-safe synthetic examples.
        - Prepare package publishing checks.
        - Improve release automation and documentation.
        - Keep all examples synthetic and safe for public repositories.

        ## [1.0.1] - 2026-06-08

        Maintenance release direction for public project readiness.

        ### Added

        - Added PCIe parser test coverage for missing link fields, redacted identifiers, domain-prefixed BDF addresses, bridge devices, and degraded link speed or width cases.
        - Added a public-safe sanitized diagnostic bundle example under `examples/sanitized_diagnostic_bundle/`.
        - Added generated PCIe, storage, and IPMI Markdown summaries for the sanitized example bundle.
        - Added a generated Markdown diagnostic report for the sanitized example bundle.
        - Added `docs/ai_maintenance_workflow.md` to document how AI coding agents can assist project maintenance.

        ### Changed

        - Extended PCIe BDF parsing to support `lspci -D` style domain-prefixed BDF addresses.
        - Documented AI-assisted maintenance boundaries and required human review workflow.

        ### Safety

        - Preserved the non-destructive project boundary.
        - No firmware flashing, BIOS/BMC setting changes, reboot, power-cycle, or remote upload behavior was added.
        - No company, customer, internal platform, real log, serial number, MAC address, IP address, hostname, firmware version, or vendor-private procedure data was added.

        ## [1.0.0] - 2026-06-04

        Initial public release baseline.

        ### Added

        - Added Ubuntu Server diagnostic log collection.
        - Added best-effort sanitization for common sensitive identifiers.
        - Added diagnostic bundle packaging.
        - Added PCIe summary generation.
        - Added storage summary generation.
        - Added IPMI sensor summary generation.
        - Added combined Markdown diagnostic report generation.
        - Added CLI entry point through `svt`.
        - Added pytest and ruff validation workflow.
        - Added GitHub Actions CI for supported Python versions.

        ### Safety

        - Defined the project as public open-source use only.
        - Excluded company-specific platform data, customer logs, private hardware topology, internal firmware versions, and proprietary validation procedures.
        - Documented non-destructive behavior in README.md.
        