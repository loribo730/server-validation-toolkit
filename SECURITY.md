# Security Policy

## Supported versions

Security fixes are accepted for the latest released version.

## Reporting a vulnerability

Please open a private security advisory if available, or contact the maintainer
without attaching sensitive logs.

## Sensitive data policy

Do not upload raw diagnostic logs that contain:

- Public IP addresses.
- Private IP addresses from real deployments.
- MAC addresses.
- Serial numbers.
- Customer names.
- Hostnames.
- Asset tags.
- Internal platform names.
- Credentials or tokens.

Sanitization is best-effort. Always review output before publishing logs.
