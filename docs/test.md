# Test Plan

## Unit and CLI Tests

The pytest suite runs offline. It creates temporary `.m4a` files, temporary data directories, and fake transcript CSVs. It does not inspect the real Voice Memos folder.

Covered areas:

- Argument parsing and subcommand availability.
- Sync dry-run planning, date filtering, and idempotent skip behavior.
- Cron line generation, dry-run output, and non-overwriting backup paths.
- Mock ASR transcript CSV shape with exactly `speaker,content` columns and controlled `--mock-text` content.
- Codex driver prompt construction from the external prompt template with prompt-injection guardrails.
- Mock postprocess markdown, HTML, and meeting-note artifacts.
- `run-day` across sync, mock ASR, and mock postprocess.
- `doctor` JSON status with explicit path checks.

## Manual Validation

Run these commands from the repo root after installation:

```bash
python -m intake_skill --help
python -m intake_skill doctor --source examples/sample_audio --data-dir tmp/validation_data --repo-root .
python -m intake_skill make-sample-audio --output examples/sample_audio/sample.m4a --seconds 1
python -m intake_skill make-sample-audio --output examples/sample_audio/sample.wav --seconds 1
python -m intake_skill sync --source examples/sample_audio --data-dir tmp/validation_data --date 20260512 --dry-run
python -m intake_skill run-day --source examples/sample_audio --data-dir tmp/validation_data --date 20260512 --asr-engine mock --postprocess-engine mock --mock-text "Installer validation transcript."
```

The end-to-end mock validation should copy one sample `.m4a` into `tmp/validation_data/20260512/`, write `transcript_20260512.csv`, then write `daily_20260512.md`, `daily_20260512.html`, and `meetings/meeting_20260512.md`. If the sample file timestamp is different from `20260512`, update the command date to the sample file's modification day before running the validation.

For live Voice Memos use, run `sync --dry-run` first and inspect the planned destination paths before copying private audio.

## Integration Notes

No live integration tests are enabled by default. MLX ASR depends on operator-installed `mlx-whisper`. Codex postprocessing depends on a configured `codex` CLI and sends transcript content to an external service. Offline tests validate the Codex prompt text and driver prompt without invoking Codex.
