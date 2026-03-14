from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import typer

from emq.commands._common import execute_sdk_command, get_no_auto_login
from emq.core.emquant_loader import get_emquant_client
from emq.core.session import ensure_login

app = typer.Typer(help="Quota and usage commands.")


@app.command("usage")
def usage(
    ctx: typer.Context,
    start: str | None = typer.Option(None, "--start", help="Start date YYYY-MM-DD."),
    end: str | None = typer.Option(None, "--end", help="End date YYYY-MM-DD."),
    func: str = typer.Option("", "--func", help="Function name filter."),
    indicators: str = typer.Option(
        "FUNCENAME,FUNCNAME,SECUTYPE,PERIOD,STARTDATE,ENDDATE,THRESHOLD,USEDDATA,USEDRATIO,AVAILABEDATA",
        "--indicators",
        help="Indicators to query.",
    ),
    options: str = typer.Option("", "--options", help="Raw EmQuant options string."),
) -> None:
    execute_sdk_command(
        ctx,
        command="quota.usage",
        fn=lambda: _usage(start, end, func, indicators, options, get_no_auto_login(ctx)),
    )


def _usage(
    start: str | None,
    end: str | None,
    func: str,
    indicators: str,
    options: str,
    no_auto_login: bool,
) -> Any:
    ensure_login(no_auto_login=no_auto_login)
    c = get_emquant_client()
    today = date.today()
    start_value = start or (today - timedelta(days=29)).isoformat()
    end_value = end or today.isoformat()

    merged_options = [f"StartDate={start_value}", f"EndDate={end_value}"]
    if options.strip():
        merged_options.append(options.strip())

    return c.datastatistics(func, indicators, ",".join(merged_options))
