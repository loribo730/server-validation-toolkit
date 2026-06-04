"""Command line interface for server-validation-toolkit."""

from __future__ import annotations

import argparse
from pathlib import Path

from server_validation_toolkit import __version__
from server_validation_toolkit.archive import create_tar_gz
from server_validation_toolkit.collector import collect_logs
from server_validation_toolkit.sanitizer import sanitize_directory
from server_validation_toolkit.summaries import (
    build_markdown_report,
    summarize_ipmi_file,
    summarize_pcie_file,
    summarize_storage_file,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser.

    Returns:
        Configured argument parser.
    """

    parser = argparse.ArgumentParser(
        prog="svt",
        description="Ubuntu Server hardware validation diagnostic toolkit.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"server-validation-toolkit {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    collect_parser = subparsers.add_parser("collect", help="Collect diagnostic logs.")
    collect_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output directory for collected logs.",
    )
    collect_parser.add_argument(
        "--sanitize",
        action="store_true",
        help="Sanitize collected logs in place.",
    )

    sanitize_parser = subparsers.add_parser("sanitize", help="Sanitize an existing log folder.")
    sanitize_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input log directory.",
    )
    sanitize_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output sanitized directory.",
    )

    package_parser = subparsers.add_parser("package", help="Create a .tar.gz bundle.")
    package_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input directory to package.",
    )
    package_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output .tar.gz file.",
    )

    pcie_parser = subparsers.add_parser("pcie-summary", help="Summarize PCIe links.")
    pcie_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input lspci -nnvv text file.",
    )
    pcie_parser.add_argument(
        "--output",
        type=Path,
        help="Optional Markdown output path.",
    )

    storage_parser = subparsers.add_parser(
        "storage-summary",
        help="Summarize block storage devices.",
    )
    storage_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input lsblk text or JSON log file path.",
    )
    storage_parser.add_argument(
        "--output",
        type=Path,
        help="Optional Markdown output path.",
    )

    ipmi_parser = subparsers.add_parser("ipmi-summary", help="Summarize IPMI sensors.")
    ipmi_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input ipmitool sensor list text file.",
    )
    ipmi_parser.add_argument(
        "--output",
        type=Path,
        help="Optional Markdown output path.",
    )

    report_parser = subparsers.add_parser(
        "report",
        help="Build a combined Markdown report from a collected log directory.",
    )
    report_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Input collected log directory.",
    )
    report_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output Markdown report path.",
    )

    return parser


def main() -> None:
    """Run the CLI entry point."""

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "collect":
        summary = collect_logs(args.output, sanitize=args.sanitize)
        print(f"Output directory: {summary.output_dir}")
        print(f"Total commands: {summary.total_commands}")
        print(f"Executed commands: {summary.executed_commands}")
        print(f"Skipped commands: {summary.skipped_commands}")
        print(f"Failed commands: {summary.failed_commands}")
        return

    if args.command == "sanitize":
        count = sanitize_directory(args.input, args.output)
        print(f"Sanitized files: {count}")
        print(f"Output directory: {args.output}")
        return

    if args.command == "package":
        archive_path = create_tar_gz(args.input, args.output)
        print(f"Archive created: {archive_path}")
        return

    if args.command == "pcie-summary":
        _write_or_print(summarize_pcie_file(args.input), args.output, "PCIe summary")
        return

    if args.command == "storage-summary":
        _write_or_print(summarize_storage_file(args.input), args.output, "Storage summary")
        return

    if args.command == "ipmi-summary":
        _write_or_print(summarize_ipmi_file(args.input), args.output, "IPMI summary")
        return

    if args.command == "report":
        report = build_markdown_report(args.input)
        args.output.write_text(report, encoding="utf-8")
        print(f"Report written: {args.output}")
        return

    parser.error(f"Unsupported command: {args.command}")


def _write_or_print(content: str, output_path: Path | None, label: str) -> None:
    """Write content to a file or print it to stdout."""

    if output_path:
        output_path.write_text(content, encoding="utf-8")
        print(f"{label} written: {output_path}")
        return

    print(content)


if __name__ == "__main__":
    main()
