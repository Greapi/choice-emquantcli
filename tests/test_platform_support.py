from __future__ import annotations

from emq.core.errors import EmqCliError
from emq.core.platform_support import ensure_sdk_runtime_supported


def test_linux_aarch64_is_rejected(monkeypatch) -> None:
    monkeypatch.setattr("emq.core.platform_support.platform.system", lambda: "Linux")
    monkeypatch.setattr("emq.core.platform_support.platform.machine", lambda: "aarch64")

    try:
        ensure_sdk_runtime_supported()
    except EmqCliError as exc:
        assert exc.code == "EMQUANT_ARCH_UNSUPPORTED"
    else:
        raise AssertionError("Expected EmqCliError for Linux aarch64")


def test_linux_x86_64_is_supported(monkeypatch) -> None:
    monkeypatch.setattr("emq.core.platform_support.platform.system", lambda: "Linux")
    monkeypatch.setattr("emq.core.platform_support.platform.machine", lambda: "x86_64")
    ensure_sdk_runtime_supported()


def test_windows_x86_64_is_supported(monkeypatch) -> None:
    monkeypatch.setattr("emq.core.platform_support.platform.system", lambda: "Windows")
    monkeypatch.setattr("emq.core.platform_support.platform.machine", lambda: "AMD64")
    ensure_sdk_runtime_supported()
