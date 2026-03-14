# EMQ CLI Architecture Map

## Overview

The CLI is structured by business domains and a shared core layer:

- `src/emq/cli.py`: root command and global options.
- `src/emq/commands/*`: domain command handlers (`auth`, `market`, `portfolio`, `quota`, `raw`).
- `src/emq/core/*`: common runtime services.
- `src/emq/vendor/emquantapi/python3`: vendored EmQuant SDK and native libraries.

## Core Modules

- `config.py`: constants, env names, vendor paths.
- `emquant_loader.py`: dynamic import + native library path patching.
- `session.py`: login lifecycle and auto-login.
- `state.py`: local credential state persistence.
- `normalize.py`: convert `EmQuantData` into row-based data.
- `output.py`: envelope creation + `json/table/csv` rendering.
- `errors.py`: domain exceptions and exit codes.
- `logging.py`: CLI logging initialization.

## Command Flow

1. Root callback parses global options (`--output`, logging, auto-login).
2. Domain command validates inputs and invokes core session.
3. Loader returns EmQuant client from vendored SDK.
4. SDK result is normalized into row records.
5. Output layer renders the unified envelope in selected format.

## Session Model

1. `auth login` logs in and stores credentials in `~/.emq/state.json`.
2. Business commands call `ensure_login()` to auto-login if needed.
3. `auth logout` calls `stop()` and clears local state.
4. `auth status` supports local-only and remote probe modes.

## Data and Error Model

All commands emit:

- `success`: boolean
- `error`: `{code,message,source}` or `null`
- `meta`: command metadata + row count
- `data`: row records

Errors from SDK (`ErrorCode != 0`) are mapped to `source=emquant`.
