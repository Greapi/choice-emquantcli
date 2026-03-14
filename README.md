# emq-cli

`emq` is a domain-oriented command line tool for EmQuantAPI with vendored runtime libraries.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Quick Start

```bash
uv sync --dev
uv run emq --help
```

Login once (credentials from flags or env):

```bash
export EMQ_USER='your_user'
export EMQ_PASS='your_pass'
uv run emq auth login
```

Sample market query:

```bash
uv run emq market series 000001.SZ CLOSE --start 2025-01-01 --end 2025-12-31 --output table
```

## Command Domains

- `auth`: `login`, `logout`, `status`
- `market`: `snapshot`, `series`
- `portfolio`: `create`, `list`, `order`
- `quota`: `usage`
- `raw`: `css`, `csd`, `pquery`, `porder`

## Output

Every command uses a unified envelope and supports:

- `--output json` (default)
- `--output table` (ASCII)
- `--output csv`

## Credential Persistence

- `auth login` saves credentials to `~/.emq/state.json` (plain text, initial version).
- Business commands auto-login from saved state or environment variables.
- `auth logout` clears local state and calls SDK logout.

## Development

```bash
uv run ruff check .
uv run mypy src
uv run pytest
```

## Notes

- The vendored SDK lives in `src/emq/vendor/emquantapi/python3`.
- Root `EMQuantAPI_Python` should not be kept after migration.
