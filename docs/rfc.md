# RFC: Minimal Voice Memos Intake CLI

## Decision 1: Voice Memos as the Only Source

The first version supports only Apple Voice Memos files from the standard macOS group container. This keeps permission and privacy behavior understandable. Other recording sources can have different consent, filename, and metadata semantics, so they are outside the current public skill.

## Decision 2: File-Based Contracts

Every stage writes plain files under `data/YYYYMMDD/`. Sync produces normalized audio names, ASR produces one CSV, and postprocessing produces markdown, HTML, and meeting-note markdown. This file contract is easier for agents to inspect than hidden state in a database. Sync can now filter by one `YYYYMMDD` day before planning or copying, which lets agents validate a single day without scanning every synced Voice Memo into the plan.

## Decision 3: Mock Engines Are Wiring Checks, Not Setup Completion

Mock ASR and mock postprocessing are first-class engines. They are not placeholders for tests only; they let an installer verify wiring, cron paths, and artifact locations without sending private content anywhere. `--mock-text` gives installer agents deterministic transcript content for postprocess validation while preserving the exact `speaker,content` CSV contract.

Initial setup still requires real ASR validation. The AI-facing install playbook instructs the installer to install `mlx-whisper`, force the local model download by transcribing synthetic sample audio, and block setup with an exact reason if the target Mac cannot complete that path.

## Decision 4: Optional Live Engines

MLX ASR and Codex postprocessing are runtime integrations. They are loaded dynamically or invoked through subprocesses, which keeps package installation lightweight and offline. Codex mode uses file-response prompting: the CLI reads `prompts/codex_postprocess.md`, combines it with concrete input and output paths, and adds prompt-injection guardrails that treat transcript content as untrusted source data. The Codex subprocess does not pass a model flag, so the local Codex CLI uses the user's configured default model.

## Decision 5: Cron Appends, Never Replaces

`install-cron` reads the current crontab, writes a timestamped backup under `logs/`, and appends one marked midnight line if absent. It does not rewrite unrelated user cron entries except through the normal append operation.

## Privacy Boundary

Mock mode stays local. MLX mode stays local if the installed ASR library does. Codex mode sends transcript content to the Codex service through the local Codex CLI. Operators must choose Codex mode only when that data boundary is acceptable.
