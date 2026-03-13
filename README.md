# choice-cli

A production-ready Python CLI starter built with `uv`, `Typer`, `ruff`, `pytest`, and `mypy`.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## 5-minute quick start

```bash
uv sync --dev
uv run choice --help
uv run choice hello --name Alice
uv run python -m choice_cli hello --name Bob
```

## Development commands

```bash
uv run ruff check .
uv run mypy src
uv run pytest
```

## Project layout

```text
.
├── pyproject.toml
├── src/choice_cli
│   ├── __init__.py
│   ├── __main__.py
│   └── main.py
├── tests/test_cli.py
└── .github/workflows/ci.yml
```

## Common issues

- `uv: command not found`: install `uv` and restart your shell session.
- `choice: command not found`: run via `uv run choice ...` or ensure the virtual environment is active.
- Import errors in editors: configure your IDE to use the `.venv` created by `uv`.

## License

MIT
