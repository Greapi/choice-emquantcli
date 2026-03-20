#!/usr/bin/env python3
"""Validate commit messages with conventional type and Chinese subject."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

ALLOWED_TYPES = "feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert"
COMMIT_PATTERN = re.compile(
    rf"^(?P<type>{ALLOWED_TYPES})(?P<scope>\([a-z0-9][a-z0-9._/-]*\))?(?P<breaking>!)?:\s+(?P<subject>.+)$"
)
HAS_CJK_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


def run_git_log(commit_range: str) -> list[tuple[str, str]]:
    cmd = ["git", "log", "--format=%H%x09%s", commit_range]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    rows = [line for line in result.stdout.splitlines() if line.strip()]
    commits: list[tuple[str, str]] = []
    for row in rows:
        sha, subject = row.split("\t", 1)
        commits.append((sha, subject))
    return commits


def validate_commit_subject(message: str) -> str | None:
    match = COMMIT_PATTERN.match(message)
    if not match:
        return (
            "格式不符合 Conventional Commits。要求: "
            "`type(scope)?: 中文描述` 或 `type!: 中文描述`。"
        )

    subject = match.group("subject")
    if not HAS_CJK_PATTERN.search(subject):
        return "描述必须包含中文字符（可混合英文术语和数字，但不能是纯英文）。"

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate commit messages.")
    parser.add_argument(
        "--range",
        required=True,
        help="Git revision range to validate, e.g. base..head or a single sha.",
    )
    args = parser.parse_args()

    commits = run_git_log(args.range)
    if not commits:
        print(f"No commits found for range: {args.range}")
        return 0

    errors = []
    for sha, subject in commits:
        reason = validate_commit_subject(subject)
        if reason:
            errors.append((sha, subject, reason))

    if errors:
        print("Found invalid commit messages:")
        for sha, subject, reason in errors:
            print(f"- {sha[:7]} {subject}")
            print(f"  -> {reason}")
        return 1

    print(f"All {len(commits)} commit messages are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
