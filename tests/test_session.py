from __future__ import annotations

from emq.core import session


class FakeEmqData:
    def __init__(self, error: int = 0, msg: str = "success") -> None:
        self.ErrorCode = error
        self.ErrorMsg = msg


class FakeClient:
    def __init__(self) -> None:
        self.start_calls: list[str] = []

    def start(self, options: str):
        self.start_calls.append(options)
        return FakeEmqData()

    def stop(self):
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
