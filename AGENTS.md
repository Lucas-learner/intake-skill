# AGENTS.md - Intake Skill

## 项目结构

- `src/intake_skill/` - Python 包和 CLI 实现
- `tests/` - 离线 pytest 测试。测试不会读取真实语音备忘录数据
- `docs/` - PRD、RFC、测试记录和工作日志
- `skills/skill_intake.md` - 面向 AI 代理的公开 skill 入口
- `prompts/` - 安装代理和后处理使用的 prompt 模板

## 操作规则

1. 本项目**仅限语音备忘录**。不要添加麦克风录音、说话人识别、声纹匹配或私人生活记录导入
2. 仓库文档保持中文，面向中文用户
3. mock 引擎保持离线且确定性，确保 `uv pip install -e '.[dev]'` 和 `python -m pytest -q` 无需网络或私有数据即可运行
4. 实质性修改后，更新 `docs/working.md` 的 Changelog，并添加具体的 Lessons Learned
5. `data/`、`logs/`、`.env` 和生成的音频/报告视为本地用户状态，而非源代码

## 环境

Python 3.10+。在仓库根目录使用 `.venv` 和 `uv pip install -e '.[dev]'`。
