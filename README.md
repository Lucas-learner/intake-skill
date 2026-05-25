# Intake Skill - 语音备忘录日报工具

Intake Skill 将已同步到 Mac 的 Apple 语音备忘录，自动整理成按日期归档的本地文件：标准化音频、转录文本 CSV、每日 Markdown/HTML 报告、以及会议记录。

本工具由 AI 代理安装为项目级技能，而非全局 Codex 技能。在你的工作目录中向代理提供以下 URL：

```text
https://github.com/Lucas-learner/intake-skill
```

然后告诉代理："帮我安装这个仓库"。代理会克隆仓库、安装 Python 依赖、安装 `mlx-qwen3-asr`，并验证端到端流程。

详细的安装和操作指南见 [`skills/skill_intake.md`](skills/skill_intake.md)。普通用户通常不需要直接运行 README 中的命令；skill 文件包含了 AI 代理应遵循的完整操作手册。

## 功能说明

Intake Skill  intentionally 功能单一。它只读取 macOS 语音备忘录标准目录中的文件，复制或转换到 `data/YYYYMMDD/`，转录为 `transcript_YYYYMMDD.csv`，并基于转录生成日报。

它**不**录制麦克风音频，**不**处理非语音备忘录来源，**不**进行说话人识别、声纹匹配或参与者归属。

运行流程：

```text
Apple 语音备忘录同步到 Mac
  -> 同步本地音频到 data/YYYYMMDD/
  -> MLX Qwen3 ASR 语音转文字
  -> Codex/Kimi AI 生成日报
```

## 主要命令

```bash
# 检查环境
python -m intake_skill doctor

# 预览今天会同步哪些文件
python -m intake_skill sync --date $(date +%Y%m%d) --dry-run

# 处理今天（同步 + 转录 + 生成日报）
python -m intake_skill today

# 或手动跑完整流程
python -m intake_skill run-day --date $(date +%Y%m%d) --asr-engine mlx --postprocess-engine kimi

# 启动本地仪表盘
python -m intake_skill dash
```

## 使用模式

- **手动模式**：需要时运行 `today` 或 `run-day` 处理最新录音
- **定时模式**：安装 cron 后，每晚自动处理当天的录音（见下方 cron 配置）

## 定时自动处理（cron）

安装 cron 定时任务，每天午夜自动处理：

```bash
# 预览将要安装的内容
python -m intake_skill install-cron --dry-run

# 安装（备份现有 crontab，追加 intake 任务）
python -m intake_skill install-cron
```

默认每天 **0:00** 执行，日志保存在 `logs/intake_cron.log`。

### 前提条件

- Mac 需保持开机（睡眠/休眠时不会执行）
- 语音备忘录需完成 iCloud 同步

### 查看日志

```bash
# 最近几次定时运行结果
tail -50 logs/intake_cron.log

# 实时跟踪
tail -f logs/intake_cron.log
```

### 取消定时任务

```bash
# 查看当前有哪些定时任务
crontab -l

# 取消所有任务（会清空，谨慎使用）
crontab -r

# 或者手动编辑，只删除 intake_skill 那一行
crontab -e
# 在编辑器里找到带 # intake_skill nightly run 的那行，删除后保存
```

### 多设备方案

如果 MacBook 晚上会睡眠，建议把定时任务装在常驻的 **Mac mini** 上，MacBook 通过 iCloud 或 Tailscale 查看报告。

## 生成的文件

```text
data/YYYYMMDD/
  YYYYMMDD_HHMM_watch.m4a    # 同步的标准化音频
  transcript_YYYYMMDD.csv     # 转录文本
  daily_YYYYMMDD.md           # Markdown 日报
  daily_YYYYMMDD.html         # HTML 日报
  meetings/*.md               # 会议记录
```

## 运行边界

- **MLX Qwen3 ASR**：本地运行，首次需要下载 `Qwen/Qwen3-ASR-1.7B` 模型
- **Kimi 后处理**：调用 Kimi Code API（通过 `~/.kimi/credentials/kimi-code.json` 自动认证），无需 Codex CLI
- **定时运行**：可选，Mac 需保持开机，语音备忘录需保持同步
- **增量处理**：已转录的音频不会重复处理
- **中文输出**：后处理默认生成中文报告

## 本地仪表盘

```bash
cd /Users/apple/projects/tools/intake-skill
source .venv/bin/activate
python -m intake_skill dash
```

默认绑定 `127.0.0.1:8765`，功能包括：

- cron 安装状态、下次运行时间
- 当前处理进度（sync/ASR/后处理）
- 今日同步队列
- 近期处理天数统计
- 手动触发 `Generate now`
- 修改/禁用定时任务

**安全提示**：不要将此仪表盘暴露到公网。

## 快捷配置（推荐）

在 `~/.zshrc` 中添加以下内容，之后无需手动 `cd` 和 `source .venv/bin/activate`：

```bash
# Intake Skill - 语音备忘录日报工具
export INTAKE_ROOT="/Users/apple/projects/tools/intake-skill"

alias intake='cd "$INTAKE_ROOT" && source .venv/bin/activate && python -m intake_skill'
alias intoday='cd "$INTAKE_ROOT" && source .venv/bin/activate && python -m intake_skill today'
alias indash='cd "$INTAKE_ROOT" && source .venv/bin/activate && python -m intake_skill dash'
alias indoctor='cd "$INTAKE_ROOT" && source .venv/bin/activate && python -m intake_skill doctor'

# 处理指定日期（用法: indate 20260522）
indate() {
    cd "$INTAKE_ROOT" && source .venv/bin/activate && python -m intake_skill run-day --date "$1" --asr-engine mlx --postprocess-engine kimi
}

# 预览指定日期同步（用法: indry 20260522）
indry() {
    cd "$INTAKE_ROOT" && source .venv/bin/activate && python -m intake_skill sync --date "$1" --dry-run
}
```

添加后运行 `source ~/.zshrc` 即可使用：

```bash
intoday        # 处理今天
indate 20260522  # 处理指定日期
indash         # 打开仪表盘
indry 20260522   # 预览同步
```

## 环境要求

- macOS（语音备忘录同步依赖）
- Python 3.10+
- `uv` 包管理器
- `ffmpeg`（用于 .qta 转换）

## 多设备方案（Mac mini + MacBook）

如果你有常驻的 Mac mini 和日常使用的 MacBook：

### iCloud Drive 同步（推荐）

Mac mini 处理录音，报告通过 iCloud Drive 自动同步到 MacBook：

```bash
# Mac mini
mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/intake-skill/data
cd ~/projects/tools/intake-skill
rm -rf data
ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/intake-skill/data data
```

MacBook 直接在 Finder → iCloud Drive → intake-skill → data 中查看报告。

### Tailscale 远程仪表盘

如果两台设备都安装了 Tailscale：

```bash
# Mac mini 查看 Tailscale IP
tailscale ip -4

# 启动仪表盘绑定 Tailscale IP
cd ~/projects/tools/intake-skill
source .venv/bin/activate
python -m intake_skill dashboard --host $(tailscale ip -4) --port 8765
```

MacBook 浏览器访问 `http://100.x.x.x:8765`。

## 给 AI 代理的说明

安装、验证、操作、调试的完整指南见 [`skills/skill_intake.md`](skills/skill_intake.md)。
