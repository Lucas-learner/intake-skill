# Installer Checklist Prompt

You are installing `intake_skill` for a Mac user.

First verify the package:

```bash
uv pip install -e '.[dev]'
python -m pytest -q
python -m intake_skill doctor
```

Then install and verify real local ASR before declaring setup complete:

```bash
uv pip install mlx-whisper
python -c "import mlx_whisper; print('mlx-whisper import ok')"
python -m intake_skill make-sample-audio --output tmp/intake_validation_source/sample.m4a --seconds 3
python -m intake_skill sync --source tmp/intake_validation_source --data-dir tmp/intake_validation_data --date YYYYMMDD
python -m intake_skill asr --data-dir tmp/intake_validation_data --date YYYYMMDD --engine mlx
python -m intake_skill postprocess --data-dir tmp/intake_validation_data --date YYYYMMDD --engine mock
```

Then preview private-data operations before running them:

```bash
python -m intake_skill sync --dry-run
python -m intake_skill install-cron --dry-run
```

Warn the operator that Codex postprocessing sends transcript content to an external service, and that cron only works when the Mac is awake and Voice Memos is syncing locally.

Before enabling Codex, verify the configured default Codex model with a non-private prompt:

```bash
codex exec --full-auto -c model_reasoning_effort=low "Reply with exactly: intake codex ok"
```
