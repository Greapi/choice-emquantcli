from __future__ import annotations

from importlib.resources import files

import typer

from emq.commands._common import apply_output_override, execute_sdk_command
from emq.core.errors import EmqCliError

app = typer.Typer(help="Skill discovery commands.")


@app.command("path")
def path_cmd(
    ctx: typer.Context,
    output: str | None = typer.Option(
        None, "--output", help="Output format override: json|table|csv."
    ),
) -> None:
    apply_output_override(ctx, output)
    execute_sdk_command(ctx, command="skill.path", fn=get_skill_path_info)


def get_skill_path_info() -> dict[str, str]:
    root = files("emq.skills")
    skill_dir = root.joinpath("emq-cli")
    skill_file = skill_dir.joinpath("SKILL.md")

    if not skill_dir.is_dir():
        raise EmqCliError(
            "packaged skill directory 'emq-cli' not found",
            code="SKILL_NOT_FOUND",
            exit_code=2,
        )

    if not skill_file.is_file():
        raise EmqCliError(
            "packaged skill file 'emq-cli/SKILL.md' not found",
            code="SKILL_NOT_FOUND",
            exit_code=2,
        )

    return {"skill": "emq-cli", "path": str(skill_dir), "skill_file": str(skill_file)}
