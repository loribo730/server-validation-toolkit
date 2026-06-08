# Roadmap

This roadmap describes the public maintenance direction for server-validation-toolkit.

## Current focus

- Keep diagnostic parsing examples public-safe and reproducible.
- Improve parser test coverage for common hardware validation text outputs.
- Maintain sanitized examples that do not expose private platform data.
- Document AI-assisted maintenance workflows with human review.

## Short-term goals

- Add more parser fixtures with fake and sanitized data only.
- Improve documentation for local validation commands.
- Keep release notes and changelog entries clear and auditable.

## Medium-term goals

- Add more structured examples for server validation workflows.
- Expand tests around parser edge cases and malformed input.
- Keep the project usable without private customer or company data.

## AI-assisted maintenance

AI tools may be used to draft tests, documentation, and maintenance plans.
All AI-assisted changes must be reviewed before merge.
Generated content must not introduce real logs, serial numbers, MAC addresses, IP addresses, hostnames, company names, customer names, or vendor-private data.

## Out of scope

- Private company validation logs.
- Customer-specific platform data.
- Vendor-private debug procedures.
- Production system instructions tied to non-public environments.
