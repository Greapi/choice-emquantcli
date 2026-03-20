from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import typer
from typer.models import OptionInfo

from emq import cli
from emq.commands import auth, market, portfolio, quota, raw, skill


@dataclass(frozen=True)
class CommandSpec:
    options: dict[str, bool]


@dataclass(frozen=True)
class DomainSpec:
    commands: dict[str, CommandSpec]


@dataclass(frozen=True)
class CliSpec:
    global_options: dict[str, bool]
    domains: dict[str, DomainSpec]


def _split_option_declarations(declaration: str) -> list[str]:
    return [part.strip() for part in declaration.split("/") if part.strip().startswith("--")]


def _extract_options_from_callback(callback: Callable[..., Any]) -> dict[str, bool]:
    signature = inspect.signature(callback)
    options: dict[str, bool] = {"--help": False}

    for parameter in signature.parameters.values():
        default = parameter.default
        if not isinstance(default, OptionInfo):
            continue

        declarations = list(default.param_decls) if default.param_decls else []
        if not declarations:
            declarations = [f"--{parameter.name.replace('_', '-')}"]

        is_flag = bool(getattr(default, "is_flag", False))
        takes_value = not is_flag
        for declaration in declarations:
            for option in _split_option_declarations(declaration):
                options[option] = takes_value

    return options


def _collect_domain_spec(app_info: typer.Typer) -> DomainSpec:
    commands: dict[str, CommandSpec] = {}
    registered_commands = getattr(app_info, "registered_commands", [])
    for command in registered_commands:
        callback = command.callback
        if callback is None or not callable(callback):
            continue

        command_name = command.name or callback.__name__.replace("_", "-")
        commands[command_name] = CommandSpec(
            options=_extract_options_from_callback(cast(Callable[..., Any], callback))
        )
    return DomainSpec(commands=commands)


def collect_cli_spec() -> CliSpec:
    global_options = _extract_options_from_callback(cli.callback)

    domains = {
        "auth": _collect_domain_spec(auth.app),
        "market": _collect_domain_spec(market.app),
        "portfolio": _collect_domain_spec(portfolio.app),
        "quota": _collect_domain_spec(quota.app),
        "raw": _collect_domain_spec(raw.app),
        "skill": _collect_domain_spec(skill.app),
    }

    return CliSpec(global_options=global_options, domains=domains)


def _normalize_token(token: str) -> str:
    return token.strip().strip("`\"'.,;()[]{}")


def _find_emq_index(tokens: list[str]) -> int | None:
    for i, token in enumerate(tokens):
        if token != "emq":
            continue
        if i == 0:
            return i
        if i >= 2 and tokens[i - 2] == "uv" and tokens[i - 1] == "run":
            return i
    return None


def _all_known_options(spec: CliSpec) -> dict[str, bool]:
    merged = dict(spec.global_options)
    for domain in spec.domains.values():
        for command in domain.commands.values():
            merged.update(command.options)
    return merged


def _parse_emq_line(line: str, spec: CliSpec) -> tuple[str | None, str | None, set[str]]:
    content = line.split("#", 1)[0].strip()
    if not content:
        return None, None, set()

    raw_tokens = [_normalize_token(t) for t in content.split()]
    tokens = [t for t in raw_tokens if t]
    if not tokens:
        return None, None, set()

    emq_index = _find_emq_index(tokens)
    if emq_index is None or emq_index + 1 >= len(tokens):
        return None, None, set()

    command_tokens = tokens[emq_index + 1 :]
    known_options = _all_known_options(spec)

    plain_tokens: list[str] = []
    options: set[str] = set()

    i = 0
    while i < len(command_tokens):
        token = command_tokens[i]
        if token.startswith("--"):
            option = token.split("=", 1)[0]
            options.add(option)
            takes_value = known_options.get(option, True)

            if "=" in token or not takes_value:
                i += 1
                continue

            if i + 1 < len(command_tokens) and not command_tokens[i + 1].startswith("--"):
                i += 2
                continue

            i += 1
            continue

        plain_tokens.append(token)
        i += 1

    if not plain_tokens:
        return None, None, options

    domain = plain_tokens[0]
    command = plain_tokens[1] if len(plain_tokens) > 1 else None
    return domain, command, options


def validate_skill_command_references(paths: list[Path], spec: CliSpec) -> list[str]:
    errors: list[str] = []

    for path in paths:
        if not path.exists():
            errors.append(f"{path}: missing file")
            continue

        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if "uv run emq" in line.lower():
                errors.append(
                    f"{path}:{lineno}: use direct 'emq ...' command, not 'uv run emq ...'"
                )
                continue

            domain, command, options = _parse_emq_line(line, spec)
            if domain is None:
                continue
            if domain.startswith("<") and domain.endswith(">"):
                continue

            domain_spec = spec.domains.get(domain)
            if domain_spec is None:
                errors.append(f"{path}:{lineno}: unknown domain '{domain}'")
                continue

            command_spec: CommandSpec | None = None
            if command is not None:
                command_spec = domain_spec.commands.get(command)
                if command_spec is None:
                    errors.append(f"{path}:{lineno}: unknown command '{domain} {command}'")
                    continue

            allowed_options = set(spec.global_options)
            if command_spec is not None:
                allowed_options.update(command_spec.options)

            for option in sorted(options):
                if option not in allowed_options:
                    errors.append(
                        f"{path}:{lineno}: unknown option '{option}' for '{domain}'"
                        + (f" '{command}'" if command is not None else "")
                    )

    return errors


def default_skill_docs() -> list[Path]:
    root = Path(__file__).resolve().parents[3]
    return [
        root / "src" / "emq" / "skills" / "emq-cli" / "SKILL.md",
        root / "src" / "emq" / "skills" / "emq-cli" / "references" / "command-recipes.md",
    ]
