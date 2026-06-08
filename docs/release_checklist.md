# Release checklist

        This checklist defines the public release process for `server-validation-toolkit`.

        The goal is to keep every release reproducible, public-safe, and easy to review.

        ## 1. Scope review

        Confirm the release scope before creating a tag or GitHub release.

        Required checks:

        - Every included change is linked to a GitHub issue or pull request.
        - Behavior changes are documented.
        - Parser changes include tests.
        - Documentation changes are public-safe.
        - Example data is synthetic.
        - The release does not include company, customer, internal platform, real log, serial number, MAC address, IP address, hostname, firmware version, or vendor-private procedure data.

        ## 2. Safety boundary review

        Confirm that the release does not introduce destructive or network-upload behavior.

        The toolkit must not:

        - flash firmware
        - change BIOS or BMC settings
        - reboot the system
        - power-cycle the system
        - upload logs to external services
        - include vendor-private validation logic
        - include real customer or company diagnostic logs

        ## 3. Local validation

        Run local validation from the repository root.

        ```bash
        PYTHONPATH=src python -m pytest -q
        python -m ruff check .
        ```

        Expected result:

        - all tests pass
        - ruff reports no lint failures
        - working tree remains clean after validation

        ## 4. Example validation

        When examples are changed, regenerate or review the generated outputs.

        Required example checks:

        - `examples/sanitized_diagnostic_bundle/README.md` explains the example.
        - `examples/sanitized_diagnostic_bundle/diagnostic_report.md` renders correctly.
        - PCIe, storage, and IPMI summaries render as Markdown tables.
        - The `.tar.gz` bundle contains only public-safe synthetic files.
        - No real identifiers or private platform details appear in the example.

        ## 5. Changelog update

        Update `CHANGELOG.md` before release.

        The changelog should include:

        - release version
        - release date
        - added features
        - changed behavior
        - fixed bugs
        - safety notes
        - documentation updates

        Keep changelog entries factual and tied to merged pull requests.

        ## 6. CI review

        Confirm GitHub Actions CI is green before merge or release.

        Required CI matrix:

        - Python 3.10
        - Python 3.11
        - Python 3.12

        Do not release from a failing or pending CI state.

        ## 7. Version review

        Confirm `pyproject.toml` and package metadata match the intended release.

        Required checks:

        - `version` is correct.
        - `requires-python` remains accurate.
        - classifiers match supported Python versions.
        - CLI entry point still works.
        - README installation instructions remain accurate.

        ## 8. Tag and release

        After all checks pass, create a Git tag and GitHub release.

        Example:

        ```bash
        git checkout main
        git pull --ff-only origin main
        git tag v1.0.1
        git push origin v1.0.1
        gh release create v1.0.1 --title "v1.0.1" --notes-file CHANGELOG.md
        ```

        Review generated release notes before publishing.

        ## 9. Post-release verification

        After publishing:

        - Confirm the release appears on GitHub.
        - Confirm the tag points to the intended commit.
        - Confirm README links still work.
        - Confirm the changelog matches the release.
        - Open follow-up issues for known limitations.

        ## 10. AI-assisted release support

        AI coding agents may help draft changelog entries, summarize merged pull requests, prepare release notes, and review checklist completeness.

        Human maintainer review is required before release. AI-generated release text must be checked against actual commits, issues, pull requests, and CI results.
        