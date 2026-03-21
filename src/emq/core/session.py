from __future__ import annotations

import re
import time
from collections.abc import Callable
from typing import Any

from .config import DEFAULT_FORCE_LOGIN, getenv_pass, getenv_user
from .emquant_loader import get_emquant_client
from .errors import EmqCliError
from .state import AuthState, clear_auth_state, load_auth_state, save_auth_state

_STARTED = False
_DELETE_RETRY_ROUTE_OPTIONS = ("", "TestLatency=1", "UseInnerNet=1", "UseProxy=1")
_DELETE_RETRY_BACKOFF_SECONDS = (0.5, 1.0, 2.0)
_NETWORK_CONNECT_FAIL_CODE = 10002002
_NETWORK_CONNECT_FAIL_TEXT = "network connect failure"
_GATEWAY_PATTERN = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}:\d+")


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
    extra_options: str = "",
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
    if extra_options:
        options = f"{options},{extra_options}"
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
        "extra_options": extra_options,
    }


def _is_retryable_network_error(exc: EmqCliError) -> bool:
    message = str(exc.message).lower()
    code_raw = exc.code
    code_num: int | None
    if isinstance(code_raw, int):
        code_num = code_raw
    elif isinstance(code_raw, str) and code_raw.isdigit():
        code_num = int(code_raw)
    else:
        code_num = None
    return code_num == _NETWORK_CONNECT_FAIL_CODE or _NETWORK_CONNECT_FAIL_TEXT in message


def _route_label(route_option: str) -> str:
    return "default" if route_option == "" else route_option


def _extract_gateways(message: str) -> list[str]:
    seen: dict[str, None] = {}
    for gateway in _GATEWAY_PATTERN.findall(message):
        seen.setdefault(gateway, None)
    return list(seen.keys())


def _reset_session_soft() -> None:
    global _STARTED
    try:
        client = get_emquant_client()
        client.stop()
    except Exception:
        # Reconnect logic should proceed even when stop() fails.
        pass
    _STARTED = False


def _relogin_with_route(*, no_auto_login: bool, route_option: str) -> None:
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

    login(
        state.user,
        state.password,
        force_login=state.force_login,
        save=True,
        extra_options=route_option,
    )


def _to_emquant_error(result: Any) -> EmqCliError | None:
    if hasattr(result, "ErrorCode") and int(result.ErrorCode) != 0:
        return EmqCliError(
            str(getattr(result, "ErrorMsg", "EmQuant API error")),
            code=int(result.ErrorCode),
            source="emquant",
            exit_code=3,
        )
    return None


def run_delete_with_network_retry(
    *,
    no_auto_login: bool,
    action: Callable[[Any], Any],
) -> Any:
    attempts = len(_DELETE_RETRY_ROUTE_OPTIONS)
    tried_routes: list[str] = []
    seen_gateways: list[str] = []
    last_error: EmqCliError | None = None

    for idx, route_option in enumerate(_DELETE_RETRY_ROUTE_OPTIONS):
        tried_routes.append(_route_label(route_option))
        try:
            if idx == 0:
                ensure_login(no_auto_login=no_auto_login)
            else:
                _reset_session_soft()
                _relogin_with_route(no_auto_login=no_auto_login, route_option=route_option)

            result = action(get_emquant_client())
            result_error = _to_emquant_error(result)
            if result_error is not None:
                raise result_error
            return result
        except EmqCliError as exc:
            if not _is_retryable_network_error(exc):
                raise
            gateways = _extract_gateways(exc.message)
            for gateway in gateways:
                if gateway not in seen_gateways:
                    seen_gateways.append(gateway)
            last_error = exc

            is_last_attempt = idx >= attempts - 1
            if is_last_attempt:
                routes = ", ".join(tried_routes)
                gateway_text = ", ".join(seen_gateways) if seen_gateways else "(none)"
                message = (
                    f"{exc.message}\n"
                    f"delete retry exhausted after {attempts} attempts; "
                    f"routes tried: {routes}; gateways: {gateway_text}; "
                    f"last_error: code={exc.code}, message={exc.message}"
                )
                raise EmqCliError(
                    message,
                    code=exc.code,
                    source=exc.source,
                    exit_code=exc.exit_code,
                ) from exc

            time.sleep(_DELETE_RETRY_BACKOFF_SECONDS[idx])

    if last_error is not None:
        raise last_error
    raise EmqCliError(
        "delete retry failed without a concrete error",
        code="DELETE_RETRY_UNKNOWN",
        source="cli",
        exit_code=1,
    )


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
