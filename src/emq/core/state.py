from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .config import STATE_DIR, STATE_FILE


class AuthState:
    def __init__(self, user: str, password: str, force_login: bool = True) -> None:
        self.user = user
        self.password = password
        self.force_login = force_login

    def to_dict(self) -> dict[str, Any]:
        return {
            "user": self.user,
            "password": self.password,
            "force_login": self.force_login,
            "updated_at": datetime.now(tz=UTC).isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AuthState | None:
        user = data.get("user")
        password = data.get("password")
        if not user or not password:
            return None
        return cls(str(user), str(password), bool(data.get("force_login", True)))


def _ensure_state_dir() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(STATE_DIR, 0o700)


def save_auth_state(state: AuthState, path: Path = STATE_FILE) -> None:
    _ensure_state_dir()
    with path.open("w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, ensure_ascii=False, indent=2)
    os.chmod(path, 0o600)


def load_auth_state(path: Path = STATE_FILE) -> AuthState | None:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        if not isinstance(raw, dict):
            return None
        return AuthState.from_dict(raw)
    except (OSError, json.JSONDecodeError):
        return None


def clear_auth_state(path: Path = STATE_FILE) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass
