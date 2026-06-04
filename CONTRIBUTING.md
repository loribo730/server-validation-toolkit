# Contributing

Contributions are welcome.

## Scope

This project accepts generic Ubuntu Server diagnostic tooling, parser improvements,
sanitization improvements, tests, and documentation updates.

Please do not submit:

- Customer logs.
- Internal company logs.
- Private hardware topology.
- Proprietary firmware data.
- Non-public validation procedures.
- Secrets, tokens, IP addresses, MAC addresses, or serial numbers.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
```

## Pull requests

A pull request should include:

- A clear reason for the change.
- Tests when behavior changes.
- Documentation updates when user-facing behavior changes.
- Sanitized examples only.
