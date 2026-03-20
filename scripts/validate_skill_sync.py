#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from emq.core.skill_sync import (
    collect_cli_spec,
    default_skill_docs,
    validate_skill_command_references,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate that emq skill command examples stay in sync with CLI options."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional markdown files to validate. Defaults to packaged emq-cli skill docs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = list(args.paths) if args.paths else default_skill_docs()

    spec = collect_cli_spec()
    errors = validate_skill_command_references(paths, spec)
    if errors:
        print("skill sync validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    checked = ", ".join(str(path) for path in paths)
    print(f"skill sync validation passed: {checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
