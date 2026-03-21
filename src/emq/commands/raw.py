from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from emq.commands._common import apply_output_override, execute_sdk_command, get_no_auto_login
from emq.core.emquant_loader import get_emquant_client
from emq.core.errors import EmqCliError
from emq.core.session import ensure_login, run_delete_with_network_retry

app = typer.Typer(help="Raw EmQuant command passthrough.")


@app.command("css")
def css(
    ctx: typer.Context,
    codes: str = typer.Argument(...),
    indicators: str = typer.Argument(...),
    options: str = typer.Option("", "--options"),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(
        ctx,
        command="raw.css",
        fn=lambda: _css(codes, indicators, options, get_no_auto_login(ctx)),
    )


@app.command("csd")
def csd(
    ctx: typer.Context,
    codes: str = typer.Argument(...),
    indicators: str = typer.Argument(...),
    start: str = typer.Option(..., "--start"),
    end: str = typer.Option(..., "--end"),
    options: str = typer.Option("", "--options"),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(
        ctx,
        command="raw.csd",
        fn=lambda: _csd(codes, indicators, start, end, options, get_no_auto_login(ctx)),
    )


@app.command("pquery")
def pquery(
    ctx: typer.Context,
    options: str = typer.Option("", "--options"),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(
        ctx,
        command="raw.pquery",
        fn=lambda: _pquery(options, get_no_auto_login(ctx)),
    )


@app.command("porder")
def porder(
    ctx: typer.Context,
    code: str = typer.Option(..., "--code"),
    orders_file: Path = typer.Option(  # noqa: B008
        ...,
        "--orders-file",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    remark: str = typer.Option("", "--remark"),
    options: str = typer.Option("", "--options"),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(
        ctx,
        command="raw.porder",
        fn=lambda: _porder(code, orders_file, remark, options, get_no_auto_login(ctx)),
    )


@app.command("pdelete")
def pdelete(
    ctx: typer.Context,
    code: str = typer.Option(..., "--code"),
    yes: bool = typer.Option(False, "--yes", help="Confirm deletion."),
    options: str = typer.Option("", "--options"),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(
        ctx,
        command="raw.pdelete",
        fn=lambda: _pdelete(code, yes, options, get_no_auto_login(ctx)),
    )


def _load_orders(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            payload = json.load(f)
        if not isinstance(payload, dict):
            raise EmqCliError(
                "orders file must contain a JSON object",
                code="ORDER_FILE_INVALID",
                exit_code=2,
            )
        return payload
    except json.JSONDecodeError as exc:
        raise EmqCliError(
            f"invalid JSON in orders file: {exc}",
            code="ORDER_FILE_INVALID",
            exit_code=2,
        ) from exc


def _css(codes: str, indicators: str, options: str, no_auto_login: bool) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    return c.css(codes, indicators, options)


def _csd(
    codes: str, indicators: str, start: str, end: str, options: str, no_auto_login: bool
) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    return c.csd(codes, indicators, start, end, options)


def _pquery(options: str, no_auto_login: bool) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    return c.pquery(options)


def _porder(code: str, orders_file: Path, remark: str, options: str, no_auto_login: bool) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    orders = _load_orders(orders_file)
    return c.porder(code, orders, remark, options)


def _pdelete(code: str, yes: bool, options: str, no_auto_login: bool) -> Any:
    if not yes:
        raise EmqCliError(
            "Deletion requires explicit confirmation. Pass --yes to continue.",
            code="CONFIRMATION_REQUIRED",
            exit_code=2,
        )
    return run_delete_with_network_retry(
        no_auto_login=no_auto_login,
        action=lambda c: c.pdelete(code, options),
    )
