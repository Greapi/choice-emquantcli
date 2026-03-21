# EMQ CLI Detailed Design

## 1. Goals

- Provide domain-driven EMQ CLI commands.
- Vendor EmQuant Python runtime in package without external install step.
- Persist login until explicit logout.
- Standardize output across commands.

## 2. Command Contracts

### auth

- `auth login [--user] [--password] [--force-login/--no-force-login]`
- `auth logout`
- `auth status [--check]`

### market

- `market snapshot <codes> <indicators> [--options]`
- `market series <codes> <indicators> --start <date> --end <date> [--options]`

### portfolio

- `portfolio create --code --name --initial-fund [--remark] [--options]`
- `portfolio list [--options]`
- `portfolio delete --code <combinCode> --yes [--options]`
- `portfolio order --code <combinCode> --orders-file <json> [--remark] [--options]`
- `portfolio qorder --code <combinCode> --stock <code> --volume <n> --price <p> --date <date> [--time <time>] [--type <type>] [--remark] [--options]`

### quota

- `quota usage [--start] [--end] [--func] [--indicators] [--options]`

### raw

- `raw css <codes> <indicators> [--options]`
- `raw csd <codes> <indicators> --start --end [--options]`
- `raw pquery [--options]`
- `raw porder --code <combinCode> --orders-file <json> [--remark] [--options]`
- `raw pdelete --code <combinCode> --yes [--options]`

## 3. SDK Loading

- Use `importlib` to load `EmQuantAPI.py` from vendored path.
- Patch `UtilAccess.GetLibraryPath()` to return platform-specific native library path.
- Native library location is selected by OS and architecture.

## 4. Authentication State

- State file: `~/.emq/state.json`.
- File permission target: `0600`.
- Credential resolution priority:
  1. CLI options
  2. env `EMQ_USER` / `EMQ_PASS`
  3. saved local state

## 5. Unified Output

Envelope schema:

```json
{
  "success": true,
  "error": null,
  "meta": {},
  "data": []
}
```

`table` and `csv` are rendered from normalized row records.

## 6. Error Strategy

- User/config validation errors: `source=cli`, exit code `2`.
- SDK errors: `source=emquant`, exit code `3`.
- Unexpected command failures are wrapped into envelope errors.

## 7. Logging

- Configured in root callback.
- Supports `--log-level` and optional `--log-file`.

## 8. Testing Scope

- Command tree availability.
- Output format behavior.
- Login precedence and auto-login semantics.
- Raw option passthrough and order file validation.
- SDK error mapping.
- SDK mocking via `FakeClient`/`FakeEmqData` with call recording for verification.
