from __future__ import annotations

import typer

from emq.commands._common import normalize_output
from emq.commands.auth import app as auth_app
from emq.commands.market import app as market_app
from emq.commands.portfolio import app as portfolio_app
from emq.commands.quota import app as quota_app
from emq.commands.raw import app as raw_app
from emq.commands.skill import app as skill_app
from emq.core.logging import setup_logging

app = typer.Typer(
    name="emq",
    help="EMQ command line interface.",
    add_completion=False,
)

app.add_typer(auth_app, name="auth")
app.add_typer(market_app, name="market")
app.add_typer(portfolio_app, name="portfolio")
app.add_typer(quota_app, name="quota")
app.add_typer(raw_app, name="raw")
app.add_typer(skill_app, name="skill")


@app.callback()
def callback(
    ctx: typer.Context,
    output: str = typer.Option("json", "--output", help="Output format: json|table|csv."),
    log_level: str = typer.Option("INFO", "--log-level", help="Log level."),
    log_file: str | None = typer.Option(None, "--log-file", help="Optional log file path."),
    no_auto_login: bool = typer.Option(False, "--no-auto-login", help="Disable automatic login."),
) -> None:
    setup_logging(log_level, log_file)
    fmt = normalize_output(output)

    ctx.ensure_object(dict)
    ctx.obj["output"] = fmt
    ctx.obj["no_auto_login"] = no_auto_login


def main() -> None:
    app()
