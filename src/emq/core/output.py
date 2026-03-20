from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from io import StringIO
from typing import Any

from emq.types import ErrorInfo, ResultEnvelope

DEFAULT_COLUMNS = ["code", "indicator", "date", "value"]


def build_envelope(
    *,
    command: str,
    data: list[dict[str, Any]],
    output: str,
    error: ErrorInfo | None = None,
    meta: dict[str, Any] | None = None,
) -> ResultEnvelope:
    merged_meta = {
        "command": command,
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "output": output,
        "row_count": len(data),
    }
    if meta:
        merged_meta.update(meta)
    return ResultEnvelope(success=error is None, error=error, meta=merged_meta, data=data)


def _as_plain_dict(envelope: ResultEnvelope) -> dict[str, Any]:
    return {
        "success": envelope.success,
        "error": None
        if envelope.error is None
        else {
            "code": envelope.error.code,
            "message": envelope.error.message,
            "source": envelope.error.source,
        },
        "meta": envelope.meta,
        "data": envelope.data,
    }


def _to_ascii_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "(no data)"

    columns = list(DEFAULT_COLUMNS)
    for row in rows:
        for key in row.keys():
            if key not in columns:
                columns.append(key)

    data_rows = [
        ["" if row.get(col) is None else str(row.get(col)) for col in columns]
        for row in rows
    ]
    widths = [len(col) for col in columns]
    for values in data_rows:
        for i, value in enumerate(values):
            widths[i] = max(widths[i], len(value))

    def fmt_line(values: list[str]) -> str:
        return " | ".join(v.ljust(widths[i]) for i, v in enumerate(values))

    sep = "-+-".join("-" * w for w in widths)
    header = fmt_line(columns)
    body = [fmt_line(values) for values in data_rows]
    return "\n".join([header, sep, *body])


def _to_csv(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    columns = list(DEFAULT_COLUMNS)
    for row in rows:
        for key in row.keys():
            if key not in columns:
                columns.append(key)

    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue().rstrip("\n")


def render_output(envelope: ResultEnvelope, output: str) -> str:
    output = output.lower()
    if output == "json":
        return json.dumps(_as_plain_dict(envelope), ensure_ascii=False, indent=2)

    if not envelope.success and envelope.error is not None:
        error_rows = [
            {
                "code": envelope.error.code,
                "indicator": "error",
                "date": None,
                "value": envelope.error.message,
                "source": envelope.error.source,
            }
        ]
        if output == "table":
            return _to_ascii_table(error_rows)
        if output == "csv":
            return _to_csv(error_rows)

    if output == "table":
        return _to_ascii_table(envelope.data)
    if output == "csv":
        return _to_csv(envelope.data)

    raise ValueError(f"Unsupported output format: {output}")


def emit(envelope: ResultEnvelope, output: str) -> None:
    text = render_output(envelope, output)
    sys.stdout.write(text)
    sys.stdout.write("\n")
