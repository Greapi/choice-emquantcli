from __future__ import annotations

import os
from pathlib import Path

ENV_USER = "EMQ_USER"
ENV_PASS = "EMQ_PASS"

DEFAULT_FORCE_LOGIN = True
DEFAULT_OUTPUT = "json"

STATE_DIR = Path.home() / ".emq"
STATE_FILE = STATE_DIR / "state.json"

VENDOR_ROOT = Path(__file__).resolve().parents[1] / "vendor" / "emquantapi" / "python3"
EMQUANT_PY = VENDOR_ROOT / "EmQuantAPI.py"
LIBS_DIR = VENDOR_ROOT / "libs"


def getenv_user() -> str | None:
    value = os.getenv(ENV_USER)
    return value.strip() if value else None


def getenv_pass() -> str | None:
    value = os.getenv(ENV_PASS)
    return value.strip() if value else None
