from __future__ import annotations

from collections.abc import Callable
from typing import Any

import typer

from emq.core.errors import EmqCliError
from emq.core.normalize import normalize_emquant_data
from emq.core.output import build_envelope, emit
from emq.types import ErrorInfo


def get_global_output(ctx: typer.Context) -> str:
    obj = ctx.obj or {}
    return str(obj.get("output", "json"))


def get_no_auto_login(ctx: typer.Context) -> bool:
    obj = ctx.obj or {}
    return bool(obj.get("no_auto_login", False))


def emit_success(
    ctx: typer.Context,
    *,
    command: str,
    rows: list[dict[str, Any]],
    meta: dict[str, Any] | None = None,
) -> None:
    output = get_global_output(ctx)
    envelope = build_envelope(command=command, data=rows, output=output, meta=meta)
    emit(envelope, output)


def emit_error(ctx: typer.Context, *, command: str, error: EmqCliError) -> None:
    output = get_global_output(ctx)
    envelope = build_envelope(
        command=command,
        data=[],
        output=output,
        error=ErrorInfo(code=error.code, message=error.message, source=error.source),
    )
    emit(envelope, output)
    raise typer.Exit(code=error.exit_code)


def execute_sdk_command(
    ctx: typer.Context,
    *,
    command: str,
    fn: Callable[[], Any],
) -> None:
    try:
        result = fn()
        if hasattr(result, "ErrorCode") and int(result.ErrorCode) != 0:
            raise EmqCliError(
                str(getattr(result, "ErrorMsg", "EmQuant API error")),
                code=int(result.ErrorCode),
                source="emquant",
                exit_code=3,
            )

        if hasattr(result, "Data"):
            rows, meta = normalize_emquant_data(result)
            emit_success(ctx, command=command, rows=rows, meta=meta)
        elif isinstance(result, dict):
            emit_success(ctx, command=command, rows=[result], meta={"row_count": 1})
        elif isinstance(result, list):
            normalized_rows = [{"value": item} for item in result]
            emit_success(
                ctx,
                command=command,
                rows=normalized_rows,
                meta={"row_count": len(result)},
            )
        else:
            emit_success(ctx, command=command, rows=[{"value": result}], meta={"row_count": 1})
    except EmqCliError as exc:
        emit_error(ctx, command=command, error=exc)
