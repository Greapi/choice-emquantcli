from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from emq.commands._common import apply_output_override, execute_sdk_command, get_no_auto_login
from emq.core.emquant_loader import get_emquant_client
from emq.core.errors import EmqCliError
from emq.core.session import ensure_login, run_delete_with_network_retry

app = typer.Typer(help="Portfolio commands.")


@app.command("create")
def create(
    ctx: typer.Context,
    code: str = typer.Option(..., "--code", help="Portfolio code."),
    name: str = typer.Option(..., "--name", help="Portfolio name."),
    initial_fund: int = typer.Option(..., "--initial-fund", help="Initial fund (integer only)."),
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
    code: str, name: str, initial_fund: int, remark: str, options: str, no_auto_login: bool
) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    return c.pcreate(code, name, initial_fund, remark, options)


def _list(options: str, no_auto_login: bool) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    return c.pquery(options)


@app.command("delete")
def delete(
    ctx: typer.Context,
    code: str = typer.Option(..., "--code", help="Portfolio code."),
    yes: bool = typer.Option(False, "--yes", help="Confirm deletion."),
    options: str = typer.Option("", "--options", help="Raw EmQuant options string."),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(
        ctx,
        command="portfolio.delete",
        fn=lambda: _delete(code, yes, options, get_no_auto_login(ctx)),
    )


def _delete(code: str, yes: bool, options: str, no_auto_login: bool) -> Any:
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


@app.command("qorder")
def qorder(
    ctx: typer.Context,
    code: str = typer.Option(..., "--code", help="Portfolio code."),
    stock: str = typer.Option(..., "--stock", help="Stock code, e.g., 300059.SZ"),
    volume: float = typer.Option(
        ..., "--volume", help="Trading volume (positive=buy, negative=sell)."
    ),
    price: float = typer.Option(..., "--price", help="Trading price."),
    date: str = typer.Option(..., "--date", help="Trading date (YYYY-MM-DD)."),
    time: str | None = typer.Option(None, "--time", help="Trading time (HHMMSS or HH:MM:SS)."),
    type: int = typer.Option(
        0, "--type", help="Operation type: 1=buy, 2=sell, 3=subscribe, 4=redeem."
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
        command="portfolio.qorder",
        fn=lambda: _qorder(
            code, stock, volume, price, date, time, type, remark, options, get_no_auto_login(ctx)
        ),
    )


def _qorder(
    code: str,
    stock: str,
    volume: float,
    price: float,
    date: str,
    time: str | None,
    type: int,
    remark: str,
    options: str,
    no_auto_login: bool,
) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()

    # Build order dict for SDK porder function
    # Ref: https://quantapi.eastmoney.com/Upload/EMQuantAPI_Python.html
    # SDK expects lists for batch orders, even for single order
    order_dict: dict[str, Any] = {
        "code": [stock],
        "volume": [volume],
        "price": [price],
        "date": [date.replace("-", "").replace("/", "")],  # Normalize to YYYYMMDD
    }

    if time is not None:
        # Normalize time format (HH:MM:SS -> HHMMSS)
        order_dict["time"] = [time.replace(":", "")]

    if type > 0:
        order_dict["optype"] = [type]

    return c.porder(code, order_dict, remark, options)


def _order(code: str, orders_file: Path, remark: str, options: str, no_auto_login: bool) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    orders = _load_orders(orders_file)
    return c.porder(code, orders, remark, options)
