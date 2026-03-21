from __future__ import annotations

from ctypes import ArgumentError
from pathlib import Path

from typer.testing import CliRunner

from emq.cli import app
from emq.core.errors import EmqCliError

runner = CliRunner()


class FakeEmqData:
    def __init__(
        self,
        *,
        error: int = 0,
        msg: str = "success",
        data=None,
        codes=None,
        indicators=None,
        dates=None,
    ):
        self.ErrorCode = error
        self.ErrorMsg = msg
        self.Data = data if data is not None else {}
        self.Codes = codes if codes is not None else []
        self.Indicators = indicators if indicators is not None else []
        self.Dates = dates if dates is not None else []


class FakeClient:
    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def pcreate(self, code: str, name: str, initial_fund: int, remark: str, options: str):
        self.calls.append(("pcreate", code, name, initial_fund, remark, options))
        return FakeEmqData(data={"result": "ok"}, codes=[code], indicators=["RESULT"], dates=[])

    def css(self, codes: str, indicators: str, options: str):
        self.calls.append(("css", codes, indicators, options))
        return FakeEmqData(
            data={"000001.SZ": [12.3]},
            codes=["000001.SZ"],
            indicators=["CLOSE"],
            dates=[],
        )

    def csd(self, codes: str, indicators: str, start: str, end: str, options: str):
        self.calls.append(("csd", codes, indicators, start, end, options))
        return FakeEmqData(
            data={"000001.SZ": [[1.0, 2.0]]},
            codes=["000001.SZ"],
            indicators=["CLOSE"],
            dates=["2025-01-01", "2025-01-02"],
        )

    def pquery(self, options: str):
        self.calls.append(("pquery", options))
        return FakeEmqData(
            data={"P1": ["Portfolio-1"]},
            codes=["P1"],
            indicators=["NAME"],
            dates=[],
        )

    def preport(self, code: str, indicator: str, options: str):
        self.calls.append(("preport", code, indicator, options))
        return FakeEmqData(
            data={code: ["000001.SZ", 1000.0]},
            codes=[code],
            indicators=["STOCKCODE", "VOLUME"],
            dates=[],
        )

    def porder(self, code: str, orders: dict, remark: str, options: str):
        self.calls.append(("porder", code, orders, remark, options))
        return FakeEmqData(data={"result": "ok"}, codes=[code], indicators=["RESULT"], dates=[])

    def pdelete(self, code: str, options: str):
        self.calls.append(("pdelete", code, options))
        return FakeEmqData(data={"result": "ok"}, codes=[code], indicators=["RESULT"], dates=[])

    def datastatistics(self, func: str, indicators: str, options: str):
        self.calls.append(("datastatistics", func, indicators, options))
        return FakeEmqData(
            data={"0": ["FUNC", "1.0"]},
            codes=["0"],
            indicators=["FUNCNAME", "USEDRATIO"],
            dates=[],
        )



def test_help_shows_domains() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "auth" in result.output
    assert "market" in result.output
    assert "portfolio" in result.output
    assert "quota" in result.output
    assert "raw" in result.output
    assert "skill" in result.output


def test_skill_path_returns_packaged_skill_path() -> None:
    result = runner.invoke(app, ["skill", "path"])
    assert result.exit_code == 0
    assert '"success": true' in result.output
    assert '"skill": "emq-cli"' in result.output
    assert "skills/emq-cli" in result.output
    assert '"skill_file"' in result.output
    assert "skills/emq-cli/SKILL.md" in result.output


def test_market_series_table_output(monkeypatch) -> None:
    from emq.commands import market

    client = FakeClient()
    monkeypatch.setattr(market, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(market, "get_emquant_client", lambda: client)

    result = runner.invoke(
        app,
        [
            "--output",
            "table",
            "market",
            "series",
            "000001.SZ",
            "CLOSE",
            "--start",
            "2025-01-01",
            "--end",
            "2025-01-02",
        ],
    )
    assert result.exit_code == 0
    assert "000001.SZ" in result.output
    assert "CLOSE" in result.output


def test_market_series_trailing_output_table(monkeypatch) -> None:
    from emq.commands import market

    client = FakeClient()
    monkeypatch.setattr(market, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(market, "get_emquant_client", lambda: client)

    result = runner.invoke(
        app,
        [
            "market",
            "series",
            "000001.SZ",
            "CLOSE",
            "--start",
            "2025-01-01",
            "--end",
            "2025-01-02",
            "--output",
            "table",
        ],
    )
    assert result.exit_code == 0
    assert "000001.SZ" in result.output
    assert "CLOSE" in result.output


def test_market_series_csv_output(monkeypatch) -> None:
    from emq.commands import market

    client = FakeClient()
    monkeypatch.setattr(market, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(market, "get_emquant_client", lambda: client)

    result = runner.invoke(
        app,
        [
            "--output",
            "csv",
            "market",
            "series",
            "000001.SZ",
            "CLOSE",
            "--start",
            "2025-01-01",
            "--end",
            "2025-01-02",
        ],
    )
    assert result.exit_code == 0
    assert "code,indicator,date,value" in result.output


def test_raw_pquery_trailing_output_csv(monkeypatch) -> None:
    from emq.commands import raw

    client = FakeClient()
    monkeypatch.setattr(raw, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(raw, "get_emquant_client", lambda: client)

    result = runner.invoke(
        app,
        ["raw", "pquery", "--output", "csv"],
    )
    assert result.exit_code == 0
    assert "code,indicator,date,value" in result.output


def test_trailing_output_overrides_global_output(monkeypatch) -> None:
    from emq.commands import market

    client = FakeClient()
    monkeypatch.setattr(market, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(market, "get_emquant_client", lambda: client)

    result = runner.invoke(
        app,
        [
            "--output",
            "json",
            "market",
            "series",
            "000001.SZ",
            "CLOSE",
            "--start",
            "2025-01-01",
            "--end",
            "2025-01-02",
            "--output",
            "table",
        ],
    )
    assert result.exit_code == 0
    assert "|" in result.output
    assert '"success"' not in result.output


def test_trailing_output_invalid_value(monkeypatch) -> None:
    from emq.commands import raw

    monkeypatch.setattr(raw, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(raw, "get_emquant_client", lambda: FakeClient())

    result = runner.invoke(app, ["raw", "pquery", "--output", "invalid"])
    assert result.exit_code == 2


def test_raw_css_options_passthrough(monkeypatch) -> None:
    from emq.commands import raw

    client = FakeClient()
    monkeypatch.setattr(raw, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(raw, "get_emquant_client", lambda: client)

    options = "TradeDate=2025-01-01,Ispandas=0"
    result = runner.invoke(app, ["raw", "css", "000001.SZ", "CLOSE", "--options", options])
    assert result.exit_code == 0
    assert client.calls[-1] == ("css", "000001.SZ", "CLOSE", options)


def test_portfolio_order_uses_json_file(monkeypatch, tmp_path: Path) -> None:
    from emq.commands import portfolio

    client = FakeClient()
    monkeypatch.setattr(portfolio, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(portfolio, "get_emquant_client", lambda: client)

    orders_file = tmp_path / "orders.json"
    orders_file.write_text('{"code": ["000001.SZ"], "volume": [100]}', encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "portfolio",
            "order",
            "--code",
            "P1",
            "--orders-file",
            str(orders_file),
        ],
    )
    assert result.exit_code == 0
    assert client.calls[-1][0] == "porder"
    assert client.calls[-1][1] == "P1"


def test_portfolio_hold_calls_preport_with_hold_indicator(monkeypatch) -> None:
    from emq.commands import portfolio

    client = FakeClient()
    monkeypatch.setattr(portfolio, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(portfolio, "get_emquant_client", lambda: client)

    result = runner.invoke(app, ["portfolio", "hold", "--code", "P1"])
    assert result.exit_code == 0
    assert client.calls[-1] == ("preport", "P1", "hold", "")


def test_portfolio_hold_options_passthrough(monkeypatch) -> None:
    from emq.commands import portfolio

    client = FakeClient()
    monkeypatch.setattr(portfolio, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(portfolio, "get_emquant_client", lambda: client)

    options = "StartDate=20250101,EndDate=20250131"
    result = runner.invoke(
        app,
        ["portfolio", "hold", "--code", "P1", "--options", options],
    )
    assert result.exit_code == 0
    assert client.calls[-1] == ("preport", "P1", "hold", options)


def test_portfolio_hold_trailing_output_csv(monkeypatch) -> None:
    from emq.commands import portfolio

    client = FakeClient()
    monkeypatch.setattr(portfolio, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(portfolio, "get_emquant_client", lambda: client)

    result = runner.invoke(
        app,
        ["portfolio", "hold", "--code", "P1", "--output", "csv"],
    )
    assert result.exit_code == 0
    assert "code,indicator,date,value" in result.output


def test_portfolio_create_accepts_integer_initial_fund(monkeypatch) -> None:
    from emq.commands import portfolio

    client = FakeClient()
    monkeypatch.setattr(portfolio, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(portfolio, "get_emquant_client", lambda: client)

    result = runner.invoke(
        app,
        [
            "portfolio",
            "create",
            "--code",
            "P1",
            "--name",
            "Portfolio-1",
            "--initial-fund",
            "1000000",
        ],
    )
    assert result.exit_code == 0
    assert client.calls[-1][0] == "pcreate"
    assert client.calls[-1][3] == 1000000
    assert isinstance(client.calls[-1][3], int)


def test_portfolio_create_rejects_decimal_initial_fund() -> None:
    result = runner.invoke(
        app,
        [
            "portfolio",
            "create",
            "--code",
            "P1",
            "--name",
            "Portfolio-1",
            "--initial-fund",
            "1000000.5",
        ],
    )
    assert result.exit_code == 2
    assert "not a valid integer" in result.output


def test_portfolio_order_invalid_json(monkeypatch, tmp_path: Path) -> None:
    from emq.commands import portfolio

    monkeypatch.setattr(portfolio, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(portfolio, "get_emquant_client", lambda: FakeClient())

    orders_file = tmp_path / "orders.json"
    orders_file.write_text("{oops", encoding="utf-8")

    result = runner.invoke(
        app,
        ["portfolio", "order", "--code", "P1", "--orders-file", str(orders_file)],
    )
    assert result.exit_code == 2
    assert "invalid JSON" in result.output


def test_portfolio_qorder_builds_order_dict(monkeypatch) -> None:
    from emq.commands import portfolio

    client = FakeClient()
    monkeypatch.setattr(portfolio, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(portfolio, "get_emquant_client", lambda: client)

    result = runner.invoke(
        app,
        [
            "portfolio",
            "qorder",
            "--code",
            "P1",
            "--stock",
            "300059.SZ",
            "--volume",
            "1000",
            "--price",
            "10.5",
            "--date",
            "2025-01-15",
        ],
    )
    assert result.exit_code == 0
    assert client.calls[-1][0] == "porder"
    assert client.calls[-1][1] == "P1"
    # Verify order dict structure (SDK expects lists for batch orders)
    order_dict = client.calls[-1][2]
    assert order_dict["code"] == ["300059.SZ"]
    assert order_dict["volume"] == [1000.0]
    assert order_dict["price"] == [10.5]
    assert order_dict["date"] == ["20250115"]  # Normalized format


def test_auth_status_reports_unsupported_architecture(monkeypatch) -> None:
    from emq.commands import _common

    monkeypatch.setattr(
        _common,
        "ensure_sdk_runtime_supported",
        lambda: (_ for _ in ()).throw(
            EmqCliError("unsupported arch", code="EMQUANT_ARCH_UNSUPPORTED", exit_code=2)
        ),
    )

    result = runner.invoke(app, ["auth", "status"])
    assert result.exit_code == 2
    assert '"code": "EMQUANT_ARCH_UNSUPPORTED"' in result.output
    assert '"source": "cli"' in result.output


def test_auth_status_wraps_oserror_from_sdk_load(monkeypatch) -> None:
    from emq.commands import auth

    monkeypatch.setattr(
        auth,
        "status",
        lambda check=False, no_auto_login=False: (_ for _ in ()).throw(OSError("boom")),
    )
    result = runner.invoke(app, ["auth", "status"])
    assert result.exit_code == 3
    assert '"code": "EMQUANT_NATIVE_LOAD_ERROR"' in result.output
    assert '"source": "emquant"' in result.output


def test_portfolio_qorder_with_optional_params(monkeypatch) -> None:
    from emq.commands import portfolio

    client = FakeClient()
    monkeypatch.setattr(portfolio, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(portfolio, "get_emquant_client", lambda: client)

    result = runner.invoke(
        app,
        [
            "portfolio",
            "qorder",
            "--code",
            "P1",
            "--stock",
            "000001.SZ",
            "--volume",
            "-500",
            "--price",
            "15.0",
            "--date",
            "2025-01-20",
            "--time",
            "14:30:00",
            "--type",
            "2",
            "--remark",
            "Sell order",
        ],
    )
    assert result.exit_code == 0
    order_dict = client.calls[-1][2]
    assert order_dict["code"] == ["000001.SZ"]
    assert order_dict["volume"] == [-500.0]
    assert order_dict["time"] == ["143000"]  # Normalized format
    assert order_dict["optype"] == [2]


def test_portfolio_qorder_missing_required_params() -> None:
    # Test missing required parameters
    result = runner.invoke(app, ["portfolio", "qorder", "--code", "P1"])
    assert result.exit_code != 0
    assert "--stock" in result.output or "Missing option" in result.output


def test_portfolio_delete_success(monkeypatch) -> None:
    from emq.commands import portfolio

    client = FakeClient()
    monkeypatch.setattr(
        portfolio,
        "run_delete_with_network_retry",
        lambda no_auto_login, action: action(client),
    )

    result = runner.invoke(app, ["portfolio", "delete", "--code", "P1", "--yes"])
    assert result.exit_code == 0
    assert client.calls[-1] == ("pdelete", "P1", "")


def test_raw_pdelete_success(monkeypatch) -> None:
    from emq.commands import raw

    client = FakeClient()
    monkeypatch.setattr(
        raw,
        "run_delete_with_network_retry",
        lambda no_auto_login, action: action(client),
    )

    result = runner.invoke(app, ["raw", "pdelete", "--code", "P1", "--yes"])
    assert result.exit_code == 0
    assert client.calls[-1] == ("pdelete", "P1", "")


def test_portfolio_delete_requires_yes(monkeypatch) -> None:
    from emq.commands import portfolio

    monkeypatch.setattr(portfolio, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(portfolio, "get_emquant_client", lambda: FakeClient())

    result = runner.invoke(app, ["portfolio", "delete", "--code", "P1"])
    assert result.exit_code == 2
    assert '"code": "CONFIRMATION_REQUIRED"' in result.output


def test_raw_pdelete_requires_yes(monkeypatch) -> None:
    from emq.commands import raw

    monkeypatch.setattr(raw, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(raw, "get_emquant_client", lambda: FakeClient())

    result = runner.invoke(app, ["raw", "pdelete", "--code", "P1"])
    assert result.exit_code == 2
    assert '"code": "CONFIRMATION_REQUIRED"' in result.output


def test_portfolio_delete_trailing_output_table(monkeypatch) -> None:
    from emq.commands import portfolio

    client = FakeClient()
    monkeypatch.setattr(
        portfolio,
        "run_delete_with_network_retry",
        lambda no_auto_login, action: action(client),
    )

    result = runner.invoke(
        app,
        ["portfolio", "delete", "--code", "P1", "--yes", "--output", "table"],
    )
    assert result.exit_code == 0
    assert "|" in result.output
    assert '"success"' not in result.output


def test_sdk_error_mapped_to_nonzero_exit(monkeypatch) -> None:
    from emq.commands import raw

    class ErrClient(FakeClient):
        def pquery(self, options: str):
            return FakeEmqData(error=1001, msg="bad request")

    monkeypatch.setattr(raw, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(raw, "get_emquant_client", lambda: ErrClient())

    result = runner.invoke(app, ["raw", "pquery"])
    assert result.exit_code == 3
    assert "bad request" in result.output


def test_sdk_argument_error_mapped_to_structured_error(monkeypatch) -> None:
    from emq.commands import portfolio

    class ArgumentErrorClient(FakeClient):
        def pcreate(self, code: str, name: str, initial_fund: int, remark: str, options: str):
            raise ArgumentError("argument 3: TypeError: integer expected")

    monkeypatch.setattr(portfolio, "ensure_login", lambda no_auto_login=False: {"ok": True})
    monkeypatch.setattr(portfolio, "get_emquant_client", lambda: ArgumentErrorClient())

    result = runner.invoke(
        app,
        [
            "portfolio",
            "create",
            "--code",
            "P1",
            "--name",
            "Portfolio-1",
            "--initial-fund",
            "1000000",
        ],
    )
    assert result.exit_code == 2
    assert '"code": "EMQUANT_ARGUMENT_ERROR"' in result.output
    assert "Invalid arguments for EmQuant command" in result.output
    assert "Traceback" not in result.output
