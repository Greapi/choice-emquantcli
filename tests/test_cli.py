from typer.testing import CliRunner

from choice_cli.main import app

runner = CliRunner()


def test_help_shows_usage() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "hello" in result.output


def test_hello_success() -> None:
    result = runner.invoke(app, ["hello", "--name", "Alice"])
    assert result.exit_code == 0
    assert "Hello, Alice" in result.output


def test_hello_missing_required_name() -> None:
    result = runner.invoke(app, ["hello"])
    assert result.exit_code != 0
    assert "Missing option '--name'" in result.output


def test_hello_invalid_times_type() -> None:
    result = runner.invoke(app, ["hello", "--name", "Alice", "--times", "abc"])
    assert result.exit_code != 0
    assert "Invalid value for '--times'" in result.output
