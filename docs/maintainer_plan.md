# Maintainer Plan

This document describes how AI coding assistants can support routine open-source maintenance.

## Maintenance tasks suitable for AI assistance

- Triage issues into bug, enhancement, documentation, or question.
- Review pull requests for unsafe log examples.
- Generate tests for sanitizer and parser edge cases.
- Draft changelog entries from merged pull requests.
- Improve parser robustness for Linux command output variants.
- Update documentation when CLI behavior changes.

## Tasks requiring human review

- Security-related changes.
- Any change that modifies collected command scope.
- Any change that touches sanitization rules.
- Any submitted diagnostic sample.
- Any parser behavior that may expose raw identifiers.
