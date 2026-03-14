import typer

app = typer.Typer(
    name="emq",
    help="A sample production-ready CLI built with Typer.",
    add_completion=False,
)


@app.callback()
def callback() -> None:
    """EMQ CLI root command group."""


@app.command()
def hello(
    name: str = typer.Option(..., "--name", help="Name to greet."),
    times: int = typer.Option(1, "--times", help="Number of greetings.", min=1),
) -> None:
    for _ in range(times):
        typer.echo(f"Hello, {name}")


def main() -> None:
    app()
