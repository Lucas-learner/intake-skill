# Installer Checklist Prompt

You are installing `intake_skill` for a Mac user.

Install it as a project-local skill. Clone the repo into the user's current workspace, normally as `skills/intake-skill`; do not install it as a global Codex skill.

First create a venv and verify the package:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e '.[dev,qwen-asr]'
python -m pytest -q
python -m intake_skill doctor
```

Then install and verify real local ASR before declaring setup complete. This must force the `Qwen/Qwen3-ASR-1.7B` model download and execution path:

Before running the ASR command, tell the user: "This first transcription may take a little while because it may need to download or warm up the local speech model."

```bash
python -c "import mlx_qwen3_asr; print('mlx-qwen3-asr import ok')"
export VALIDATION_DAY=$(date +%Y%m%d)
export VALIDATION_ROOT="tmp/intake_validation_$(date +%Y%m%d_%H%M%S)"
export VALIDATION_SOURCE="$VALIDATION_ROOT/source"
export VALIDATION_DATA="$VALIDATION_ROOT/data"
mkdir -p "$VALIDATION_SOURCE" "$VALIDATION_DATA"
python -m intake_skill make-sample-audio --output "$VALIDATION_SOURCE/sample.m4a" --seconds 3
python -m intake_skill sync --source "$VALIDATION_SOURCE" --data-dir "$VALIDATION_DATA" --date "$VALIDATION_DAY" --dry-run
python -m intake_skill sync --source "$VALIDATION_SOURCE" --data-dir "$VALIDATION_DATA" --date "$VALIDATION_DAY"
python -m intake_skill asr --data-dir "$VALIDATION_DATA" --date "$VALIDATION_DAY" --engine mlx
python - <<'PY'
import csv
import os
from pathlib import Path

data_dir = Path(os.environ["VALIDATION_DATA"])
day = os.environ["VALIDATION_DAY"]
transcript = data_dir / day / f"transcript_{day}.csv"
with transcript.open(newline="", encoding="utf-8") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
assert reader.fieldnames == ["speaker", "content"]
assert rows and any((row.get("content") or "").strip() for row in rows)
print(f"ASR transcript ok: {transcript}")
PY
codex exec --full-auto -c model_reasoning_effort=low "Reply with exactly: intake codex ok"
python -m intake_skill postprocess --data-dir "$VALIDATION_DATA" --date "$VALIDATION_DAY" --engine codex
open "$VALIDATION_DATA/$VALIDATION_DAY"
```

Then tell the operator where the sample output files were written. Do not treat ASR as verified until the CSV check has passed; if you inspect the transcript in a separate shell, use the exact `output_path` from the ASR JSON or re-export `VALIDATION_DATA` and `VALIDATION_DAY`. If Finder opened successfully, mention that the folder is open; otherwise give the exact path. Explain the real Voice Memos requirements in plain language: iCloud sync for Voice Memos must be enabled if they rely on it, the Mac should be plugged in, and the Mac must be awake rather than shut down when the nightly automatic run is expected to happen.

Preview real Voice Memos sync before running it:

```bash
python -m intake_skill sync --dry-run
```

If the operator wants daily automatic processing, describe it as "a small job that runs every night while your Mac is awake." Mention that macOS may show a permission prompt and they should allow it. Then preview, back up, and install the schedule:

```bash
python -m intake_skill install-cron --dry-run
mkdir -p logs
crontab -l > logs/crontab_manual_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null || true
python -m intake_skill install-cron
```
