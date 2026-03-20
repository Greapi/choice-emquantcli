#!/usr/bin/env python3
"""Validate release tag format, version alignment, and monotonic increase."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

TAG_PATTERN = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
PROJECT_VERSION_PATTERN = re.compile(r'^\s*version\s*=\s*"(\d+\.\d+\.\d+)"\s*$')


def parse_semver(value: str) -> tuple[int, int, int] | None:
    match = TAG_PATTERN.match(value if value.startswith("v") else f"v{value}")
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def read_project_version(pyproject_path: Path) -> str:
    in_project_section = False
    for line in pyproject_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project_section = stripped == "[project]"
            continue
        if in_project_section:
            match = PROJECT_VERSION_PATTERN.match(line)
            if match:
                return match.group(1)
    raise RuntimeError("Cannot find [project].version in pyproject.toml")


def get_existing_tags() -> Iterable[str]:
    result = subprocess.run(
        ["git", "tag", "--list", "v*.*.*"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate release tag policy.")
    parser.add_argument("--tag", required=True, help="Release tag name, e.g. v0.2.4")
    parser.add_argument(
        "--pyproject",
        default="pyproject.toml",
        help="Path to pyproject.toml (default: pyproject.toml)",
    )
    args = parser.parse_args()

    tag = args.tag
    tag_match = TAG_PATTERN.match(tag)
    if not tag_match:
        print(f"Invalid tag format: {tag}. Expected format: vX.Y.Z")
        return 1
    current_version = tuple(int(part) for part in tag_match.groups())

    pyproject_version_str = read_project_version(Path(args.pyproject))
    pyproject_version = parse_semver(pyproject_version_str)
    if pyproject_version is None:
        print(f"Invalid pyproject version: {pyproject_version_str}. Expected: X.Y.Z")
        return 1
    if pyproject_version != current_version:
        print(
            "Version mismatch: "
            f"tag={tag} but pyproject.toml has version={pyproject_version_str}"
        )
        return 1

    max_existing = None
    max_existing_tag = None
    for existing_tag in get_existing_tags():
        if existing_tag == tag:
            continue
        parsed = parse_semver(existing_tag)
        if parsed is None:
            continue
        if max_existing is None or parsed > max_existing:
            max_existing = parsed
            max_existing_tag = existing_tag

    if max_existing is not None and current_version <= max_existing:
        print(
            "Tag version must be strictly increasing: "
            f"current={tag}, max_existing={max_existing_tag}"
        )
        return 1

    print(
        "Release tag validation passed: "
        f"{tag} matches pyproject version {pyproject_version_str} and is strictly increasing."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
