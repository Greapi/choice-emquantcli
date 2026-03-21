# AGENTS.md

## Purpose
This document guides AI coding agents working in this repository. Focus on practical, safe, and minimal changes for `emq-cli` (Python 3.10+) with the vendored EmQuant SDK runtime included in-tree.

## Repository Facts
- Project: `emq-cli`
- Python requirement: `>=3.10`
- CLI entrypoint: `emq` (from `emq.cli:main`)
- Main package path: `src/emq`
- Tests path: `tests`
- Docs path: `docs`
- Vendored EmQuant SDK path: `src/emq/vendor/emquantapi/python3`

## Do / Don't
### Do
- Keep diffs minimal and scoped to the request.
- Preserve existing coding style and project patterns.
- Add or adjust tests when behavior changes.
- Keep user-facing behavior and output contracts consistent unless asked to change them.
- When CLI capabilities or command usage change, update `src/emq/skills/emq-cli/SKILL.md` (and related command recipes) in the same change to keep skill guidance in sync.

### Don't
- Do not edit vendored SDK files unless explicitly requested.
- Do not introduce unrelated refactors.
- Do not commit credentials, tokens, or other secrets.

## Standard Workflow
1. Inspect relevant code paths, tests, and docs before changing anything.
2. Implement focused changes only in files required for the task.
3. Run quality checks and tests relevant to the change.
4. Summarize impact, verification status, and unresolved risks.

## Validation Commands
Run these canonical checks during development:

```bash
uv run ruff check .
uv run mypy src
uv run python scripts/validate_skill_sync.py
uv run pytest
```

## Commit & Release Constraints
- Use Conventional Commits for commit messages.
- Commit descriptions must include Chinese characters.
- Release tags must follow `vX.Y.Z`.
- The tag version must match `[project].version` in `pyproject.toml` (without the `v` prefix).

Reference: `docs/commit-and-release.md`

## Output Expectations for Agents
When reporting results, include:
- Changed files
- Why each change was made
- Verification status (which checks were run and outcomes)
- Any unresolved risks, assumptions, or follow-up items
