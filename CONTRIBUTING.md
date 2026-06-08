# Contributing

Thank you for considering a contribution to server-validation-toolkit.

## Public-safe requirement

Do not include company, customer, private platform, real diagnostic log, serial number, real MAC address, real IP address, hostname, credential, token, or vendor-private data.

Use fake or sanitized examples only.

## Contribution workflow

1. Open an issue describing the change.
2. Create a topic branch.
3. Keep the change small and reviewable.
4. Run validation before opening a pull request.
5. Open a pull request and link the related issue.

## Validation

Run source-level validation before submitting changes:

```bash
python3 -m compileall .
```

If the repository has tests available, run them before opening a pull request:

```bash
python3 -m pytest
```

## AI-assisted changes

AI tools, including Codex, may be used to draft documentation, tests, and maintenance changes.
AI-assisted output must be reviewed by a human before merge.
Do not use AI tools to add private company, customer, platform, or diagnostic data.

## Version metadata

Do not change Python version metadata unless compatibility has been tested and intentionally reviewed.
