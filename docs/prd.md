# Product Requirements Document

## Purpose

`intake_skill` gives AI agents a predictable local interface for processing Apple Voice Memos into daily artifacts. The primary user is an installer or maintenance agent, not a human clicking through a desktop app.

The project deliberately starts with a narrow scope. It reads files that Voice Memos has already synced to the Mac, normalizes them into dated folders, creates a transcript CSV through a selected ASR engine, and turns that transcript into daily markdown, HTML, and meeting-note files.

## Users

The direct user is an AI coding or operations agent that needs a stable terminal contract. The human operator benefits from predictable local files, dry-run sync, offline tests, and clear privacy boundaries.

## Requirements

The CLI must expose `doctor`, `sync`, `asr`, `postprocess`, `run-day`, `install-cron`, and `make-sample-audio`. Commands should print JSON summaries and avoid reading private data during tests.

Sync is Voice Memos only. The default source is `~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/`. It discovers `.qta` and `.m4a` files and writes them to `data/YYYYMMDD/YYYYMMDD_HHMM_watch.m4a`. Repeated runs must skip existing outputs rather than overwrite them.

ASR writes `transcript_YYYYMMDD.csv` with exactly `speaker,content` columns. There is no speaker recognition. Mock ASR must work offline. First-run setup must also verify the real MLX ASR path by installing `mlx-whisper`, downloading or initializing the local model through a synthetic sample transcription, and confirming the transcript CSV contract. If the target Mac cannot complete that path, setup should be marked blocked with the exact reason.

Postprocessing supports `mock` and `codex`. Mock mode writes deterministic markdown, HTML, and `meetings/*.md` files. Codex mode may call an external service through `codex exec --full-auto -c model_reasoning_effort=low`; documentation must warn about transcript content leaving the local machine. The CLI must not pass a hardcoded Codex model flag, so Codex uses the user's configured default model.

Cron installation must back up the current crontab and append one midnight line. It must support `--dry-run` and never overwrite backup files.

## Success Criteria

`uv pip install -e '.[dev]'` and `python -m pytest -q` run offline from a clean checkout with cached packaging tools. `doctor`, `sync --dry-run`, mock ASR, mock postprocess, and mock `run-day` can be exercised without private Voice Memos data. Installer agents additionally validate real MLX ASR on synthetic sample audio before declaring setup complete.

## Non-Goals

This project does not record microphone audio. It does not import private life-record code or copy private examples into the repo. It does not add diarization, speaker recognition, reference voices, or any feature that makes identity claims about voices.
