from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from emq.cli import app

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

    def porder(self, code: str, orders: dict, remark: str, options: str):
        self.calls.append(("porder", code, orders, remark, options))
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
