"""Diagnostic command collector."""

from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path

from server_validation_toolkit.commands import DEFAULT_COMMANDS
from server_validation_toolkit.models import CollectionSummary, CommandResult, CommandSpec
from server_validation_toolkit.sanitizer import sanitize_directory
from server_validation_toolkit.utils import ensure_directory, utc_timestamp, write_json


def is_command_available(command: tuple[str, ...]) -> bool:
    """Check whether the command executable exists.

    Args:
        command: Command tuple where index 0 is the executable.

    Returns:
        True when the executable is available.
    """
    return shutil.which(command[0]) is not None


def run_command(spec: CommandSpec) -> CommandResult:
    """Run a diagnostic command.

    The collector deliberately uses ``check=False`` because diagnostic collection
    should continue even when one optional system tool returns a non-zero status.
    The return code and stderr are preserved in the output file for later review.

    Args:
        spec: Command specification containing executable, arguments, timeout,
            and optional-command metadata.

    Returns:
        CommandResult object containing return code, stdout, stderr, or skip reason.
    """
    if not is_command_available(spec.command):
        return CommandResult(
            spec=spec,
            return_code=None,
            stdout="",
            stderr="",
            skipped_reason=f"Command not found: {spec.command[0]}",
        )

    try:
        completed = subprocess.run(
            spec.command,
            check=False,
            capture_output=True,
            text=True,
            timeout=spec.timeout_seconds,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            spec=spec,
            return_code=None,
            stdout=exc.stdout or "",
            stderr=exc.stderr or f"Timed out after {spec.timeout_seconds} seconds",
        )

    return CommandResult(
        spec=spec,
        return_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def write_command_result(output_dir: Path, result: CommandResult) -> None:
    """Write command result to disk.

    Args:
        output_dir: Output directory.
        result: Command execution result.
    """
    output_path = output_dir / result.output_file_name
    command_line = " ".join(result.spec.command)

    content = [
        f"$ {command_line}",
        "",
        f"return_code: {result.return_code}",
    ]

    if result.skipped_reason:
        content.extend(["", f"skipped_reason: {result.skipped_reason}"])

    content.extend(["", "----- stdout -----", result.stdout.rstrip(), "", "----- stderr -----"])
    content.append(result.stderr.rstrip())
    output_path.write_text("\n".join(content).rstrip() + "\n", encoding="utf-8")


def collect_logs(
    output_dir: Path,
    *,
    sanitize: bool = False,
    command_specs: tuple[CommandSpec, ...] = DEFAULT_COMMANDS,
) -> CollectionSummary:
    """Collect diagnostic logs.

    Args:
        output_dir: Directory where logs will be written.
        sanitize: Whether to sanitize output in place after collection.
        command_specs: Commands to execute.

    Returns:
        Collection summary containing output path and command status counts.
    """
    ensure_directory(output_dir)

    results = [run_command(spec) for spec in command_specs]
    for result in results:
        write_command_result(output_dir, result)

    skipped_commands = sum(result.skipped_reason is not None for result in results)
    executed_commands = len(results) - skipped_commands
    failed_commands = sum(result.return_code not in {0, None} for result in results)

    manifest = {
        "created_at_utc": utc_timestamp(),
        "tool": "server-validation-toolkit",
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "total_commands": len(results),
        "executed_commands": executed_commands,
        "skipped_commands": skipped_commands,
        "failed_commands": failed_commands,
        "commands": [
            {
                "name": result.spec.name,
                "command": list(result.spec.command),
                "return_code": result.return_code,
                "skipped_reason": result.skipped_reason,
            }
            for result in results
        ],
    }
    write_json(output_dir / "manifest.json", manifest)

    error_lines = []
    for result in results:
        if result.skipped_reason or result.return_code not in {0, None}:
            error_lines.append(
                f"{result.spec.name}: return_code={result.return_code}, "
                f"skipped={result.skipped_reason}"
            )

    (output_dir / "command_errors.txt").write_text(
        "\n".join(error_lines).rstrip() + "\n",
        encoding="utf-8",
    )

    if sanitize:
        temporary_dir = output_dir.with_name(f"{output_dir.name}_unsanitized")
        if temporary_dir.exists():
            shutil.rmtree(temporary_dir)

        # Use shutil.move to support cross-device filesystem boundaries.
        shutil.move(str(output_dir), str(temporary_dir))
        sanitize_directory(temporary_dir, output_dir)

    return CollectionSummary(
        output_dir=output_dir,
        total_commands=len(results),
        executed_commands=executed_commands,
        skipped_commands=skipped_commands,
        failed_commands=failed_commands,
    )
