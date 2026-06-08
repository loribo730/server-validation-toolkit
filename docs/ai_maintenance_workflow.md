# AI maintenance workflow

        This document describes how AI coding agents, including Codex, can assist with maintaining `server-validation-toolkit`.

        The project remains human-reviewed. AI-generated suggestions must be reviewed, tested, and merged through the normal GitHub issue, pull request, and CI workflow.

        ## Goals

        `server-validation-toolkit` is a public-safe Ubuntu Server diagnostic toolkit for hardware validation engineers. The project focuses on reproducible local log collection, sensitive data sanitization, PCIe/storage/IPMI summary generation, and Markdown diagnostic reports.

        AI assistance is used to improve maintenance speed while preserving the project's safety boundary.

        ## AI-assisted maintenance tasks

        ### Issue triage

        AI may help classify new issues into practical maintenance categories:

        - parser coverage
        - sanitized example data
        - documentation
        - packaging
        - release readiness
        - bug reproduction
        - CI failure investigation

        AI may propose labels, clarify missing reproduction steps, and draft follow-up questions. A maintainer must approve final issue updates.

        ### Parser test generation

        AI may generate synthetic test cases for common Linux diagnostic output variants, including:

        - missing PCIe link fields
        - domain-prefixed BDF addresses
        - degraded PCIe link speed or width
        - sanitized device identifiers
        - lsblk JSON and text output variants
        - IPMI sensor formatting variants

        Tests must use synthetic data only. Real customer logs, internal hardware topology, serial numbers, MAC addresses, IP addresses, hostnames, and firmware versions must not be committed.

        ### Synthetic example data

        AI may help draft public-safe example logs and reports for documentation. These examples must remain synthetic and must not identify a real system, company, customer, product program, lab, or vendor-private workflow.

        The example bundle under `examples/sanitized_diagnostic_bundle/` is the preferred reference format for future examples.

        ### Changelog and release preparation

        AI may help draft changelog entries, release notes, and release checklist items. The maintainer must verify that each entry matches committed code and merged pull requests.

        AI may help summarize:

        - merged pull requests
        - closed issues
        - CI status
        - new public-safe examples
        - parser coverage changes
        - documentation changes

        ### Safe refactoring

        AI may suggest refactoring when it improves readability, maintainability, or testability. Refactoring must preserve behavior unless an issue explicitly defines the behavior change.

        Safe refactoring rules:

        - keep changes small
        - avoid unrelated style-only rewrites
        - preserve CLI behavior
        - preserve non-destructive behavior
        - add or update tests when parser behavior changes
        - keep sanitizer behavior conservative
        - run CI before merge

        ## Non-negotiable safety boundaries

        AI must not introduce code that:

        - flashes firmware
        - changes BIOS or BMC settings
        - reboots the system
        - power-cycles the system
        - uploads logs to external services
        - embeds company-specific validation logic
        - embeds customer logs
        - embeds private hardware topology
        - embeds internal firmware versions
        - embeds serial numbers, MAC addresses, IP addresses, or hostnames

        These boundaries match the repository's public-safe design.

        ## Required review workflow

        Every AI-assisted change should follow this workflow:

        1. Open or reuse a GitHub issue.
        2. Create a topic branch.
        3. Make the smallest practical change.
        4. Run local validation.
        5. Open a pull request.
        6. Wait for CI to pass.
        7. Review the diff manually.
        8. Squash merge only after the change is understood.

        Required local validation:

        ```bash
        PYTHONPATH=src python -m pytest -q
        python -m ruff check .
        ```

        ## Maintainer responsibility

        AI is used as an implementation assistant, not as the final authority. The maintainer is responsible for correctness, safety, licensing, documentation quality, and public release decisions.

        Human review is required before any AI-generated code, test, example, or documentation is merged.
        