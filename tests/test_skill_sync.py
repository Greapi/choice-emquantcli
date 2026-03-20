from __future__ import annotations

from pathlib import Path

from emq.core.skill_sync import collect_cli_spec, validate_skill_command_references


def test_skill_docs_are_in_sync() -> None:
    root = Path(__file__).resolve().parents[1]
    files = [
        root / "src" / "emq" / "skills" / "emq-cli" / "SKILL.md",
        root / "src" / "emq" / "skills" / "emq-cli" / "references" / "command-recipes.md",
    ]

    spec = collect_cli_spec()
    errors = validate_skill_command_references(files, spec)
    assert errors == []


def test_skill_sync_reports_unknown_option(tmp_path: Path) -> None:
    bad_skill = tmp_path / "bad-skill.md"
    bad_skill.write_text(
        "emq market snapshot 000001.SZ CLOSE --not-real-option 1\n",
        encoding="utf-8",
    )

    spec = collect_cli_spec()
    errors = validate_skill_command_references([bad_skill], spec)

    assert errors
    assert "unknown option '--not-real-option'" in errors[0]


def test_skill_sync_rejects_uv_run_emq(tmp_path: Path) -> None:
    bad_skill = tmp_path / "bad-usage.md"
    bad_skill.write_text(
        "uv run emq market snapshot 000001.SZ CLOSE\n",
        encoding="utf-8",
    )

    spec = collect_cli_spec()
    errors = validate_skill_command_references([bad_skill], spec)

    assert errors
    assert "use direct 'emq ...' command" in errors[0]
