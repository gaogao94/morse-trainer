# AGENTS.md

**开始本文件夹的任何工作之前，必须先读 [待办.md](待办.md)**，并主动向用户提醒其中列出的待改问题。那些问题用户说过"先不改"，除非用户明确要求，不要顺手修复。

## 项目概况

- 单文件静态应用 `index.html`（CSS/JS 全内联，无构建步骤）。
- `serve.py`：可选的静态服务 + `POST /api/feedback`（反馈经 hermes 转发到微信）。
- 远程仓库：https://github.com/gaogao94/morse_trainer
- 修改后验证方式：`node --check` 内联 JS；playwright 截图（`node_modules/playwright-core` + `~/.cache/ms-playwright` 可用）；反馈接口用 `FEEDBACK_DRY_RUN=1 python3 serve.py <端口>` 本地测。
