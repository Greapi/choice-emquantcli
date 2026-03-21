from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module():
    root = Path(__file__).resolve().parents[1]
    module_path = root / "scripts" / "validate_commits.py"
    spec = importlib.util.spec_from_file_location("validate_commits", module_path)
    if spec is None or spec.loader is None:
        raise AssertionError("Failed to load validate_commits module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validate_commit_subject_rejects_non_conventional() -> None:
    module = _load_module()

    reason = module.validate_commit_subject("not a conventional message")

    assert reason is not None
    assert "Conventional Commits" in reason


def test_validate_commit_subject_requires_cjk_by_default() -> None:
    module = _load_module()

    reason = module.validate_commit_subject("fix(portfolio): add retry logic")

    assert reason == "描述必须包含中文字符（可混合英文术语和数字，但不能是纯英文）。"


def test_validate_commit_subject_allows_non_cjk_when_disabled() -> None:
    module = _load_module()

    reason = module.validate_commit_subject(
        "fix(portfolio): add retry logic",
        require_cjk=False,
    )

    assert reason is None


def test_validate_commit_subject_still_accepts_cjk_when_disabled() -> None:
    module = _load_module()

    reason = module.validate_commit_subject(
        "fix(portfolio): 修复重试逻辑",
        require_cjk=False,
    )

    assert reason is None
