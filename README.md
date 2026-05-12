# Intake Skill

`intake_skill` is a small AI-oriented CLI for turning Apple Voice Memos into dated local intake artifacts. It is intentionally narrow: it only reads Voice Memos files, it does not record microphone audio, and the default engines run offline for install and tests.

## What this gives an AI agent

The package exposes `python -m intake_skill` and the console script `intake-skill`. The stable commands are `doctor`, `sync`, `asr`, `postprocess`, `run-day`, `install-cron`, and `make-sample-audio`. Each command prints a JSON summary so an installer agent can parse status without scraping prose.

The default source is Apple Voice Memos on macOS:

```text
~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/
```

The sync step scans only `.qta` and `.m4a` files and writes normalized copies under `data/YYYYMMDD/YYYYMMDD_HHMM_watch.m4a`. `.m4a` files are copied, and `.qta` files are converted with `ffmpeg` so the destination is a real `.m4a`. It supports `--dry-run`, optional `--date YYYYMMDD` filtering, and treats existing destination files as immutable, so repeated runs are idempotent.

## Install

From the repository root:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e '.[dev]'
python -m pytest -q
```

The test suite is offline. It uses temporary synthetic files and the mock engines only.

## Basic usage

```bash
python -m intake_skill doctor
python -m intake_skill sync --date 20260512 --dry-run
python -m intake_skill sync --date 20260512
python -m intake_skill asr --date 20260512 --engine mock --mock-text "Installer validation transcript."
python -m intake_skill postprocess --date 20260512 --engine mock
python -m intake_skill run-day --date 20260512 --asr-engine mock --postprocess-engine mock
```

Mock ASR writes `transcript_YYYYMMDD.csv` with exactly two columns: `speaker,content`. The default mock content names each audio file. Passing `--mock-text` writes that exact content for each mock transcript row, which lets installer agents validate downstream behavior with known text. The `speaker` values are blank by design; this skill does not perform speaker recognition, diarization, reference voice matching, or meeting participant attribution.

## Optional live engines

`--engine mlx` for ASR requires `mlx-whisper` to be installed by the operator. This package does not depend on it because offline installation and tests should stay lightweight.

`postprocess --engine codex` runs:

```bash
codex exec --full-auto -m gpt-5.2 -c model_reasoning_effort=low
```

Codex mode reads `prompts/codex_postprocess.md`, wraps it in a file-response driver prompt, and sends transcript content to an external service through the Codex CLI. The driver marks transcript text as untrusted data and tells Codex not to infer speaker identity or invent facts. Use mock mode for private offline validation and use Codex mode only when the operator accepts that data boundary.

## Cron

Preview the cron line:

```bash
python -m intake_skill install-cron --dry-run
```

Installing cron backs up the current crontab under `logs/crontab_backup_*.txt` and appends a midnight `run-day` line if the marker is not already present. It never overwrites an existing backup file.

The Mac must be awake at midnight, and Voice Memos must be running or syncing often enough for new recordings to appear in the source directory.

## Sample audio

```bash
python -m intake_skill make-sample-audio --output examples/sample_audio/sample.m4a
```

On macOS with `say` and `ffmpeg`, a requested `.m4a` output uses synthesized speech and writes `examples/sample_audio/sample.m4a`. Otherwise the command falls back to a Python-generated sine wave `.wav`, such as `examples/sample_audio/sample.wav`. The sample contains no private content.

## Agent setup

Copy `skills/skill_intake.md` into the agent's skill directory or point the agent at it from `AGENTS.md`. The skill file documents trigger phrases, command contracts, privacy boundaries, and expected artifacts.
