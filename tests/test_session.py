from __future__ import annotations

import pytest

from emq.core import session


class FakeEmqData:
    def __init__(self, error: int = 0, msg: str = "success") -> None:
        self.ErrorCode = error
        self.ErrorMsg = msg


class FakeClient:
    def __init__(self) -> None:
        self.start_calls: list[str] = []
        self.stop_calls = 0

    def start(self, options: str):
        self.start_calls.append(options)
        return FakeEmqData()

    def stop(self):
        self.stop_calls += 1
        return FakeEmqData()

    def pquery(self, options: str):
        return FakeEmqData()



def test_login_prefers_args_over_env(monkeypatch) -> None:
    client = FakeClient()
    monkeypatch.setattr(session, "get_emquant_client", lambda: client)
    monkeypatch.setattr(session, "getenv_user", lambda: "env_user")
    monkeypatch.setattr(session, "getenv_pass", lambda: "env_pass")

    saved: dict = {}
    monkeypatch.setattr(session, "save_auth_state", lambda state: saved.update(state.to_dict()))

    result = session.login("arg_user", "arg_pass", force_login=True, save=True)
    assert result["user"] == "arg_user"
    assert "UserName=arg_user" in client.start_calls[-1]
    assert saved["user"] == "arg_user"


def test_ensure_login_uses_saved_state(monkeypatch) -> None:
    client = FakeClient()
    monkeypatch.setattr(session, "get_emquant_client", lambda: client)
    monkeypatch.setattr(session, "getenv_user", lambda: None)
    monkeypatch.setattr(session, "getenv_pass", lambda: None)
    monkeypatch.setattr(
        session,
        "load_auth_state",
        lambda: session.AuthState(user="saved_user", password="saved_pass", force_login=True),
    )
    monkeypatch.setattr(session, "save_auth_state", lambda state: None)

    session._STARTED = False
    session.ensure_login(no_auto_login=False)
    assert client.start_calls
    assert "UserName=saved_user" in client.start_calls[-1]


def test_status_check_returns_remote_ok(monkeypatch) -> None:
    client = FakeClient()
    monkeypatch.setattr(session, "get_emquant_client", lambda: client)
    monkeypatch.setattr(
        session,
        "load_auth_state",
        lambda: session.AuthState(user="saved_user", password="saved_pass", force_login=True),
    )
    monkeypatch.setattr(session, "save_auth_state", lambda state: None)
    session._STARTED = False

    payload = session.status(check=True)
    assert payload["local_logged_in"] is True
    assert payload["remote_ok"] is True


def test_run_delete_with_network_retry_succeeds_after_retry(monkeypatch) -> None:
    client = FakeClient()
    monkeypatch.setattr(session, "get_emquant_client", lambda: client)
    monkeypatch.setattr(session, "getenv_user", lambda: None)
    monkeypatch.setattr(session, "getenv_pass", lambda: None)
    monkeypatch.setattr(
        session,
        "load_auth_state",
        lambda: session.AuthState(user="saved_user", password="saved_pass", force_login=True),
    )
    monkeypatch.setattr(session, "save_auth_state", lambda state: None)
    monkeypatch.setattr(session.time, "sleep", lambda _: None)
    session._STARTED = False

    attempts = {"count": 0}

    def delete_action(_client):
        attempts["count"] += 1
        if attempts["count"] == 1:
            return FakeEmqData(error=10002002, msg="network connect failure 61.1.1.1:1818")
        return FakeEmqData()

    result = session.run_delete_with_network_retry(no_auto_login=False, action=delete_action)
    assert result.ErrorCode == 0
    assert attempts["count"] == 2
    assert any("TestLatency=1" in opt for opt in client.start_calls)
    assert client.stop_calls >= 1


def test_run_delete_with_network_retry_exhausted_has_diagnostics(monkeypatch) -> None:
    client = FakeClient()
    monkeypatch.setattr(session, "get_emquant_client", lambda: client)
    monkeypatch.setattr(session, "getenv_user", lambda: None)
    monkeypatch.setattr(session, "getenv_pass", lambda: None)
    monkeypatch.setattr(
        session,
        "load_auth_state",
        lambda: session.AuthState(user="saved_user", password="saved_pass", force_login=True),
    )
    monkeypatch.setattr(session, "save_auth_state", lambda state: None)
    monkeypatch.setattr(session.time, "sleep", lambda _: None)
    session._STARTED = False

    def delete_action(_client):
        return FakeEmqData(
            error=10002002,
            msg="network connect failure can't connect to 114.80.72.132:1818",
        )

    with pytest.raises(session.EmqCliError) as exc_info:
        session.run_delete_with_network_retry(no_auto_login=False, action=delete_action)

    assert "delete retry exhausted after 4 attempts" in exc_info.value.message
    assert (
        "routes tried: default, TestLatency=1, UseInnerNet=1, UseProxy=1"
        in exc_info.value.message
    )
    assert "114.80.72.132:1818" in exc_info.value.message


def test_run_delete_with_network_retry_non_retryable_error(monkeypatch) -> None:
    client = FakeClient()
    monkeypatch.setattr(session, "get_emquant_client", lambda: client)
    monkeypatch.setattr(session, "getenv_user", lambda: None)
    monkeypatch.setattr(session, "getenv_pass", lambda: None)
    monkeypatch.setattr(
        session,
        "load_auth_state",
        lambda: session.AuthState(user="saved_user", password="saved_pass", force_login=True),
    )
    monkeypatch.setattr(session, "save_auth_state", lambda state: None)
    monkeypatch.setattr(session.time, "sleep", lambda _: None)
    session._STARTED = False

    call_count = {"count": 0}

    def delete_action(_client):
        call_count["count"] += 1
        return FakeEmqData(error=1001, msg="bad request")

    with pytest.raises(session.EmqCliError) as exc_info:
        session.run_delete_with_network_retry(no_auto_login=False, action=delete_action)

    assert exc_info.value.code == 1001
    assert call_count["count"] == 1
