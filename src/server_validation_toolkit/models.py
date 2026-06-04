"""Data models used by the diagnostic collector."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommandSpec:
    """Describe one diagnostic command.

    Args:
        name: Stable command name used for output file naming.
        command: Command and arguments to execute.
        timeout_seconds: Maximum allowed execution time.
        optional: Whether missing command should be treated as a skip instead of an error.
    """

    name: str
    command: tuple[str, ...]
    timeout_seconds: int = 30
    optional: bool = True


@dataclass(frozen=True)
class CommandResult:
    """Store command execution result.

    Args:
        spec: Original command specification.
        return_code: Process return code. None means the command was not executed.
        stdout: Standard output text.
        stderr: Standard error text.
        skipped_reason: Reason when the command was skipped.
    """

    spec: CommandSpec
    return_code: int | None
    stdout: str
    stderr: str
    skipped_reason: str | None = None

    @property
    def output_file_name(self) -> str:
        """Return a stable text file name for this command result."""

        return f"{self.spec.name}.txt"


@dataclass(frozen=True)
class CollectionSummary:
    """Describe one completed collection run.

    Args:
        output_dir: Directory containing the collected files.
        total_commands: Total command count.
        executed_commands: Number of commands that were executed.
        skipped_commands: Number of commands that were skipped.
        failed_commands: Number of commands that returned non-zero.
    """

    output_dir: Path
    total_commands: int
    executed_commands: int
    skipped_commands: int
    failed_commands: int
