from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from emq.commands._common import apply_output_override, execute_sdk_command, get_no_auto_login
from emq.core.emquant_loader import get_emquant_client
from emq.core.errors import EmqCliError
from emq.core.session import ensure_login

app = typer.Typer(help="Portfolio commands.")


@app.command("create")
def create(
    ctx: typer.Context,
    code: str = typer.Option(..., "--code", help="Portfolio code."),
    name: str = typer.Option(..., "--name", help="Portfolio name."),
    initial_fund: float = typer.Option(..., "--initial-fund", help="Initial fund."),
    remark: str = typer.Option("", "--remark", help="Remark."),
    options: str = typer.Option("", "--options", help="Raw EmQuant options string."),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(
        ctx,
        command="portfolio.create",
        fn=lambda: _create(code, name, initial_fund, remark, options, get_no_auto_login(ctx)),
    )


@app.command("list")
def list_portfolio(
    ctx: typer.Context,
    options: str = typer.Option("", "--options", help="Raw EmQuant options string."),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(
        ctx,
        command="portfolio.list",
        fn=lambda: _list(options, get_no_auto_login(ctx)),
    )


@app.command("order")
def order(
    ctx: typer.Context,
    code: str = typer.Option(..., "--code", help="Portfolio code."),
    orders_file: Path = typer.Option(  # noqa: B008
        ...,
        "--orders-file",
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
    remark: str = typer.Option("", "--remark", help="Remark."),
    options: str = typer.Option("", "--options", help="Raw EmQuant options string."),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(
        ctx,
        command="portfolio.order",
        fn=lambda: _order(code, orders_file, remark, options, get_no_auto_login(ctx)),
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


def _create(
    code: str, name: str, initial_fund: float, remark: str, options: str, no_auto_login: bool
) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    return c.pcreate(code, name, initial_fund, remark, options)


def _list(options: str, no_auto_login: bool) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    return c.pquery(options)


def _order(code: str, orders_file: Path, remark: str, options: str, no_auto_login: bool) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    orders = _load_orders(orders_file)
    return c.porder(code, orders, remark, options)
