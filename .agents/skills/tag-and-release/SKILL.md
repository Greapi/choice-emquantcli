---
name: tag-and-release
description: 指导在 emq-cli 仓库中执行版本发布：更新 pyproject.toml 版本、按 Conventional Commits 提交、创建并推送 vX.Y.Z 标签、触发 GitHub Actions 发布，并总结上一个 tag 到当前 tag 的主要 commit 变更。遇到“如何打 tag”“如何发布 PyPI”“如何写发布说明”“标签与版本不一致”“发布校验失败排查”等场景时使用本技能。
---

# Tag And Release

## 目标

按仓库规范完成一次可追踪的正式发布，确保版本号、Git 标签和 CI 发布流程一致。

## 发布前检查

1. 确认工作区干净，避免将无关改动带入发布。
2. 确认目标版本号为 `X.Y.Z`，且严格大于历史最大发布版本。
3. 确认 `pyproject.toml` 中 `[project].version` 将被更新为目标版本。

## 标准发布流程

0. 确认工作区为空：发布前必须没有待提交改动。

```bash
git status --porcelain
```

1. 更新版本号：修改 `pyproject.toml` 的 `[project].version` 为目标版本（例如 `0.2.8`），并同步更新所有与版本相关的文件。
2. 运行发布前校验：

```bash
uv run ruff check .
uv run mypy src
uv run python scripts/validate_skill_sync.py
uv run pytest
```

3. 提交变更：使用 Conventional Commits，描述优先中文。

```bash
git add pyproject.toml [其他发布相关文件]
git commit -m "chore(release): 发布 v0.2.8"
```

4. 创建发布标签：

```bash
git tag v0.2.8
```

5. 推送分支和标签：

```bash
git push
git push --tags
```

6. 在 GitHub Actions 确认发布流水线通过，并检查包发布结果。

## 发布内容整理（必须执行，且发生在打新 tag 之前）

1. 找到最近一个发布标签（例如 `v0.2.7`）：

```bash
git describe --tags --abbrev=0
```

2. 在未打新 tag 前，查看“最近 tag 到当前 HEAD”的 commit 区间（例如 `v0.2.7..HEAD`）：

```bash
git log --oneline v0.2.7..HEAD
```

3. 按主题总结主要变更，不逐条机械罗列；优先归纳为“功能新增 / 缺陷修复 / 工程与CI调整 / 文档变更”。
4. 新增发布 commit，内容必须包含：
   - 发布目标版本号（例如 `v0.2.8`）
   - 上述区间的主要变更摘要（作为本版本发布内容）
5. 打上新 tag 后，发布说明中可将统计区间写为 `v0.2.7..v0.2.8`（与 `v0.2.7..HEAD` 在打标当下等价）。

可选辅助命令：

```bash
git log --pretty=format:'%h %s (%an)' v0.2.7..HEAD
git diff --name-only v0.2.7..HEAD
```

## 规则约束

1. 标签必须使用 `vX.Y.Z` 格式。
2. 标签版本去掉 `v` 前缀后，必须与 `[project].version` 完全一致。
3. 版本号必须递增，禁止复用历史标签版本。
4. 提交信息必须符合 Conventional Commits。

## 失败排查

1. 标签格式错误：检查是否为 `vX.Y.Z`。
2. 版本不一致：检查 `pyproject.toml` 的 `[project].version` 与标签是否一致。
3. 版本未递增：检查远端历史标签，确认新版本更大。
4. 提交校验失败：检查 commit `type(scope): 描述` 结构是否正确。

## 输出要求

执行本技能时，优先给出：

1. 当前版本与目标版本。
2. 将执行的命令清单。
3. 每一步执行结果与是否通过。
4. 若失败，给出最小修复步骤与重试命令。
5. 输出发布说明时包含“上一个 tag 到当前 tag 的 commit 汇总”和“主要变更摘要”。
