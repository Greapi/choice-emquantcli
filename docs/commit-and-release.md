# Commit 与发布标签规范

本文档定义本项目的提交与发布规则。CI 会阻断不符合强制校验项的变更与发布。

## 1. Commit 规范（强制）

Commit Message 必须使用 Conventional Commits 前缀。描述推荐使用中文，但 CI 不强制。

格式：

```text
type(scope)?: 描述
type!: 描述
```

允许的 `type`：

- `feat`
- `fix`
- `docs`
- `style`
- `refactor`
- `perf`
- `test`
- `build`
- `ci`
- `chore`
- `revert`

约束说明：

- `type` 必须为小写英文。
- `scope` 可选，若存在仅允许英文小写、数字和 `._/-`。
- 冒号后描述推荐包含中文字符，可混合英文术语与数字。
- CI 当前只强制校验 Conventional Commits 结构（`type(scope)?: subject` / `type!: subject`）。

示例（合规）：

- `fix(portfolio): 修复初始资金必须为整数的问题`
- `feat: 新增 Python 3.10 兼容性校验`
- `ci: 调整发布流程触发条件`

示例（不推荐，但 CI 可通过）：

- `fix: Fix portfolio bug`（仅英文描述，不推荐）

示例（不合规）：
- `修复: 处理参数问题`（type 非约定英文类型）
- `fix(portfolio)`（缺少描述）

## 2. 标签与版本规范（强制）

发布标签语义：**创建发布标签即触发正式版本发布**。

标签规则：

- 标签必须为 `vX.Y.Z`（例如 `v0.2.4`）。
- `pyproject.toml` 中 `[project].version` 必须与标签一致（去掉 `v` 前缀后相同）。
- 新标签版本必须严格大于历史最大发布标签版本（只增不减，不可复用）。

## 3. 发布流程

1. 修改 `pyproject.toml` 的 `[project].version` 为目标版本（如 `0.2.4`）。
2. 提交代码（Commit Message 需符合 Conventional Commits 规范，推荐中文描述）。
3. 创建标签：`git tag v0.2.4`。
4. 推送分支与标签：`git push && git push --tags`。
5. GitHub Actions 自动执行校验并发布到 PyPI。

## 4. CI 失败排查

提交校验失败：

- 检查是否使用了允许的 `type`。
- 若你期望中文规范，检查是否包含冒号后的中文描述（CI 不强制）。
- 检查 `scope` 是否为英文小写格式。

发布标签校验失败：

- 检查标签是否为 `vX.Y.Z`。
- 检查 `pyproject.toml` 版本是否与标签一致。
- 检查当前标签是否大于历史最大发布标签。
