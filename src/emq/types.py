from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ErrorInfo:
    code: int | str
    message: str
    source: str = "cli"


@dataclass
class ResultEnvelope:
    success: bool
    error: ErrorInfo | None
    meta: dict[str, Any] = field(default_factory=dict)
    data: list[dict[str, Any]] = field(default_factory=list)
