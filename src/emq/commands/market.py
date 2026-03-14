from __future__ import annotations

from typing import Any

import typer

from emq.commands._common import execute_sdk_command, get_no_auto_login
from emq.core.emquant_loader import get_emquant_client
from emq.core.session import ensure_login

app = typer.Typer(help="Market data commands.")


@app.command("snapshot")
def snapshot(
    ctx: typer.Context,
    codes: str = typer.Argument(..., help="Codes, comma-separated."),
    indicators: str = typer.Argument(..., help="Indicators, comma-separated."),
    options: str = typer.Option("", "--options", help="Raw EmQuant options string."),
) -> None:
    execute_sdk_command(
        ctx,
        command="market.snapshot",
        fn=lambda: _snapshot(codes, indicators, options, get_no_auto_login(ctx)),
    )


@app.command("series")
def series(
    ctx: typer.Context,
    codes: str = typer.Argument(..., help="Codes, comma-separated."),
    indicators: str = typer.Argument(..., help="Indicators, comma-separated."),
    start: str = typer.Option(..., "--start", help="Start date YYYY-MM-DD."),
    end: str = typer.Option(..., "--end", help="End date YYYY-MM-DD."),
    options: str = typer.Option("", "--options", help="Raw EmQuant options string."),
) -> None:
    execute_sdk_command(
        ctx,
        command="market.series",
        fn=lambda: _series(codes, indicators, start, end, options, get_no_auto_login(ctx)),
    )


def _snapshot(codes: str, indicators: str, options: str, no_auto_login: bool) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    return c.css(codes, indicators, options)


def _series(
    codes: str, indicators: str, start: str, end: str, options: str, no_auto_login: bool
) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    return c.csd(codes, indicators, start, end, options)
