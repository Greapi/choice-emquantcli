# emq-cli

`emq` is a domain-oriented command line tool for EmQuantAPI with vendored runtime libraries.

## Requirements

- Python 3.10+

## Platform Support

- macOS: `x86_64`, `arm64` (universal wheel)
- Linux: `x86_64` only
- Windows: `amd64` only

Linux `arm64/aarch64` is not supported by the vendored EmQuant Linux SDK at this time.

## Quick Start

```bash
pip install emq-cli
emq --help
```

Login once (credentials from flags or env):

```bash
export EMQ_USER='your_user'
export EMQ_PASS='your_pass'
emq auth login
```

Sample market query:

```bash
emq market series 000001.SZ CLOSE --start 2025-01-01 --end 2025-12-31 --output table
```

Quick portfolio order:

```bash
emq portfolio qorder --code MYPORT --stock 300059.SZ --volume 1000 --price 10.5 --date 2025-01-15
```

## Command Domains

- `auth`: `login`, `logout`, `status`
- `market`: `snapshot`, `series`
- `portfolio`: `create`, `list`, `hold`, `order`, `qorder`
- `quota`: `usage`
- `raw`: `css`, `csd`, `pquery`, `porder`

## Output

Every command uses a unified envelope and supports:

- `--output json` (default)
- `--output table` (ASCII)
- `--output csv`

`--output` can be placed either before the domain command (global) or at the end of leaf commands (override).  
If both are provided, the leaf command `--output` takes precedence.

## Credential Persistence

- `auth login` saves credentials to `~/.emq/state.json` (plain text, initial version).
- Business commands auto-login from saved state or environment variables.
- `auth logout` clears local state and calls SDK logout.

## Development

```bash
uv run ruff check .
uv run mypy src
uv run python scripts/validate_skill_sync.py
uv run pytest
```

## Notes

- The vendored SDK lives in `src/emq/vendor/emquantapi/python3`.
- Root `EMQuantAPI_Python` should not be kept after migration.
- Commit and release governance: `docs/commit-and-release.md`.
