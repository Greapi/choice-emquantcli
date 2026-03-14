from __future__ import annotations

from typing import Any

from .config import DEFAULT_FORCE_LOGIN, getenv_pass, getenv_user
from .emquant_loader import get_emquant_client
from .errors import EmqCliError
from .state import AuthState, clear_auth_state, load_auth_state, save_auth_state

_STARTED = False


def _resolve_credentials(
    user: str | None = None,
    password: str | None = None,
    *,
    allow_saved: bool = True,
) -> AuthState | None:
    user = user or getenv_user()
    password = password or getenv_pass()
    if user and password:
        return AuthState(user=user, password=password, force_login=DEFAULT_FORCE_LOGIN)

    if allow_saved:
        return load_auth_state()
    return None


def login(
    user: str | None,
    password: str | None,
    *,
    force_login: bool = DEFAULT_FORCE_LOGIN,
    save: bool = True,
) -> dict[str, Any]:
    state = _resolve_credentials(user=user, password=password, allow_saved=False)
    if state is None:
        raise EmqCliError(
            "Missing credentials. Provide --user/--password or set EMQ_USER/EMQ_PASS.",
            code="AUTH_CREDENTIAL_MISSING",
            exit_code=2,
        )

    client = get_emquant_client()
    options = (
        f"ForceLogin={1 if force_login else 0},"
        f"UserName={state.user},Password={state.password}"
    )
    result = client.start(options)
    if result.ErrorCode != 0:
        raise EmqCliError(
            result.ErrorMsg,
            code=result.ErrorCode,
            source="emquant",
            exit_code=3,
        )

    if save:
        save_auth_state(AuthState(state.user, state.password, force_login=force_login))

    global _STARTED
    _STARTED = True
    return {
        "user": state.user,
        "saved": save,
        "force_login": force_login,
    }


def ensure_login(*, no_auto_login: bool = False) -> dict[str, Any]:
    global _STARTED
    if _STARTED:
        return {"already_started": True}

    if no_auto_login:
        raise EmqCliError(
            "Auto login disabled. Please run `emq auth login` first.",
            code="AUTH_AUTO_LOGIN_DISABLED",
            exit_code=2,
        )

    state = _resolve_credentials(allow_saved=True)
    if state is None:
        raise EmqCliError(
            "Not logged in. Run `emq auth login` or set EMQ_USER/EMQ_PASS.",
            code="AUTH_NOT_LOGGED_IN",
            exit_code=2,
        )

    return login(
        state.user,
        state.password,
        force_login=state.force_login,
        save=True,
    )


def logout() -> dict[str, Any]:
    client = get_emquant_client()
    result = client.stop()
    clear_auth_state()

    global _STARTED
    _STARTED = False

    if result.ErrorCode != 0:
        raise EmqCliError(result.ErrorMsg, code=result.ErrorCode, source="emquant", exit_code=3)

    return {"logged_out": True}


def status(check: bool = False, *, no_auto_login: bool = False) -> dict[str, Any]:
    current = load_auth_state()
    payload: dict[str, Any] = {
        "local_logged_in": current is not None,
        "user": None if current is None else current.user,
        "remote_ok": None,
    }

    if not check:
        return payload

    try:
        ensure_login(no_auto_login=no_auto_login)
        client = get_emquant_client()
        probe = client.pquery("")
        payload["remote_ok"] = probe.ErrorCode == 0
        payload["remote_error"] = None if probe.ErrorCode == 0 else probe.ErrorMsg
    except EmqCliError as exc:
        payload["remote_ok"] = False
        payload["remote_error"] = exc.message

    return payload
