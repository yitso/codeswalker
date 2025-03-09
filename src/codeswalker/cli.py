# -*- coding: utf-8 -*-
import argparse
import os
import sys
from .scanner import generate_project_context


def main():
    """
    Entry point for the Codeswalker CLI tool.

    This tool generates Markdown documentation for a codebase by scanning files
    in a specified directory. It supports Git ignore rules and custom ignore patterns.
    """
    parser = argparse.ArgumentParser(
        description="Generate Markdown documentation for the codebase."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Target directory to scan."
    )
    parser.add_argument(
        "--ignore",
        "-i",
        type=str,
        default="",
        help="Custom ignore file path or ignore pattern string (supports glob patterns, one per line) to exclude files (e.g., LICENSE)."
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="PROJECT_CONTEXT.md",
        help="Output Markdown file path."
    )
    args = parser.parse_args()

    custom_ignore_rules = []
    if args.ignore:
        if os.path.exists(args.ignore):
            with open(args.ignore, "r", encoding="utf-8") as f:
                custom_ignore_rules = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        else:
            custom_ignore_rules = [rule.strip() for rule in args.ignore.splitlines() if rule.strip()]

    output_md = generate_project_context(args.directory, custom_ignore_rules)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output_md)

    sys.stdout.write(f"Documentation generated at: {os.path.abspath(args.output)}\n")
