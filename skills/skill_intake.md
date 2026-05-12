---
name: intake-skill
description: >-
  Runs a Voice Memos intake workflow via python -m intake_skill: sync local Voice Memos, create transcript CSVs, and generate daily artifacts.
disable-model-invocation: true
---

# Intake Skill

Use this skill when an agent needs to install, verify, or operate a local Apple Voice Memos intake workflow. The CLI is designed for AI agents: every command prints JSON, mock engines work offline, and privacy boundaries are explicit.

## When to use

Use for these intents:

- Process Apple Voice Memos into daily files.
- Dry-run a Voice Memos sync before touching private audio.
- Generate a mock transcript and mock daily report for installation testing.
- Install a midnight cron job for a Mac that stays awake and keeps Voice Memos syncing.
- Create synthetic sample audio with no private content.

## Prerequisites

Install from the repository root:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e '.[dev]'
python -m pytest -q
```

Default source:

```text
~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/
```

The Mac must be awake when cron runs, and Voice Memos must be running or syncing often enough for new recordings to appear locally.

## Commands

```bash
python -m intake_skill doctor
python -m intake_skill sync --date YYYYMMDD --dry-run
python -m intake_skill sync --date YYYYMMDD
python -m intake_skill asr --date YYYYMMDD --engine mock --mock-text "Installer validation transcript."
python -m intake_skill postprocess --date YYYYMMDD --engine mock
python -m intake_skill run-day --date YYYYMMDD --asr-engine mock --postprocess-engine mock
python -m intake_skill install-cron --dry-run
python -m intake_skill make-sample-audio --output examples/sample.wav
```

Pass `--source`, `--data-dir`, and `--repo-root` to override defaults. Prefer `sync --date YYYYMMDD --dry-run` before a real sync when validating one day.

## Output Contract

Sync reads `.qta` and `.m4a` files only and writes `data/YYYYMMDD/YYYYMMDD_HHMM_watch.m4a`. `--date YYYYMMDD` limits discovery to files whose modification timestamp falls on that day. Existing destination files are skipped, not overwritten.

ASR writes `data/YYYYMMDD/transcript_YYYYMMDD.csv` with exactly these columns:

```csv
speaker,content
```

The `speaker` column is blank in current engines. Mock ASR accepts `--mock-text` for deterministic installer validation. The skill does not perform speaker recognition, diarization, reference voice matching, or microphone recording.

Mock postprocess writes `daily_YYYYMMDD.md`, `daily_YYYYMMDD.html`, and `meetings/*.md`.

## External-Service Warning

`postprocess --engine codex` invokes:

```bash
codex exec --full-auto -m gpt-5.2 -c model_reasoning_effort=low
```

That mode sends transcript content to the Codex service. The CLI builds the Codex request from `prompts/codex_postprocess.md` and adds guardrails that treat transcript content as untrusted data, forbid speaker identity inference, and forbid invented facts. Use Codex only when the operator accepts that boundary. Use `--engine mock` for offline validation.
