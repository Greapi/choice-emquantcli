from __future__ import annotations

import typer

from emq.commands._common import apply_output_override, execute_sdk_command
from emq.core.session import login, logout, status

app = typer.Typer(help="Authentication commands.")


@app.command("login")
def login_cmd(
    ctx: typer.Context,
    user: str | None = typer.Option(None, "--user", help="EMQ username."),
    password: str | None = typer.Option(None, "--password", help="EMQ password."),
    force_login: bool = typer.Option(
        True, "--force-login/--no-force-login", help="Set ForceLogin."
    ),
    save: bool = typer.Option(True, "--save/--no-save", help="Save credentials to local state."),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(
        ctx,
        command="auth.login",
        fn=lambda: login(user=user, password=password, force_login=force_login, save=save),
    )


@app.command("logout")
def logout_cmd(
    ctx: typer.Context,
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(ctx, command="auth.logout", fn=logout)


@app.command("status")
def status_cmd(
    ctx: typer.Context,
    check: bool = typer.Option(False, "--check", help="Probe remote API status."),
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    no_auto_login = bool((ctx.obj or {}).get("no_auto_login", False))
    execute_sdk_command(
        ctx,
        command="auth.status",
        fn=lambda: status(check=check, no_auto_login=no_auto_login),
    )
