# Working Log

## Changelog

### 2026-05-12

- Created the public `intake_skill` CLI repo with package code, docs, prompts, skill instructions, scripts, and offline pytest coverage.
- Added deterministic mock ASR and mock postprocessing so installers can verify the workflow without private data or network access.
- Added dry-run sync and dry-run cron paths before any operation touches user-owned audio or crontab state.
- Added sync `--date` filtering, ASR `--mock-text`, external Codex prompt-template loading, and explicit prompt-injection guardrails.
- Validation update: `python -m pytest -q` passed with 14 tests; `doctor` returned status `ok`; sample audio was generated as `examples/sample_audio/sample.wav` and `examples/sample_audio/sample.m4a`; the mock `run-day` flow copied one sample `.m4a` into `tmp/validation_data`, wrote `transcript_YYYYMMDD.csv`, `daily_YYYYMMDD.md`, `daily_YYYYMMDD.html`, and `meetings/meeting_YYYYMMDD.md`; Codex and MLX live integrations were not invoked.

## Lessons Learned

- Keep the sync source restricted to Voice Memos. Expanding to other audio sources changes privacy and consent assumptions.
- The transcript CSV schema is an external contract: exactly `speaker,content`, with blank speaker values unless a future explicit requirement changes that boundary.
- Codex postprocessing must remain opt-in because transcript content crosses a service boundary.
- Treat transcript text as untrusted source data inside any AI postprocessing prompt; spoken words can accidentally contain instruction-like phrases.
