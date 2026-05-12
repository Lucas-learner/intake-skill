# Installer Checklist Prompt

You are installing `intake_skill` for a Mac user.

Install it as a project-local skill. Clone the repo into the user's current workspace, normally as `skills/intake-skill`; do not install it as a global Codex skill.

First create a venv and verify the package:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e '.[dev]'
python -m pytest -q
python -m intake_skill doctor
```

Then install and verify real local ASR before declaring setup complete. This must force the default MLX Whisper model download and execution path:

```bash
uv pip install mlx-whisper
python -c "import mlx_whisper; print('mlx-whisper import ok')"
VALIDATION_DAY=$(date +%Y%m%d)
VALIDATION_ROOT="tmp/intake_validation_$(date +%Y%m%d_%H%M%S)"
VALIDATION_SOURCE="$VALIDATION_ROOT/source"
VALIDATION_DATA="$VALIDATION_ROOT/data"
mkdir -p "$VALIDATION_SOURCE" "$VALIDATION_DATA"
python -m intake_skill make-sample-audio --output "$VALIDATION_SOURCE/sample.m4a" --seconds 3
python -m intake_skill sync --source "$VALIDATION_SOURCE" --data-dir "$VALIDATION_DATA" --date "$VALIDATION_DAY" --dry-run
python -m intake_skill sync --source "$VALIDATION_SOURCE" --data-dir "$VALIDATION_DATA" --date "$VALIDATION_DAY"
python -m intake_skill asr --data-dir "$VALIDATION_DATA" --date "$VALIDATION_DAY" --engine mlx
codex exec --full-auto -c model_reasoning_effort=low "Reply with exactly: intake codex ok"
python -m intake_skill postprocess --data-dir "$VALIDATION_DATA" --date "$VALIDATION_DAY" --engine codex
```

Then explain the real Voice Memos requirements to the operator: iCloud sync for Voice Memos must be enabled if they rely on it, the Mac should be plugged in, and the Mac must be awake rather than shut down when the nightly job is expected to run.

Preview real Voice Memos sync before running it:

```bash
python -m intake_skill sync --dry-run
```

If the operator wants daily automatic processing, explain that installing cron may trigger a macOS permission prompt and they should allow it. Then preview, back up, and install cron:

```bash
python -m intake_skill install-cron --dry-run
mkdir -p logs
crontab -l > logs/crontab_manual_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null || true
python -m intake_skill install-cron
```
