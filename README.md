# Intake Skill

Intake Skill turns Apple Voice Memos that have already synced to a Mac into dated local intake artifacts: normalized audio files, transcript CSVs, daily Markdown and HTML reports, and meeting-note Markdown files.

This repo is meant to be installed by an AI agent as a project-local skill, not as a standard global Codex skill. Give the agent this URL from the workspace where you want the skill to live:

```text
https://github.com/grapeot/intake-skill
```

Ask it: "Install this repo for me: https://github.com/grapeot/intake-skill". The agent should clone the repo under the current folder, normally at `skills/intake-skill`, install Python dependencies, install `mlx-whisper`, tell the user that the first speech-model download may take a little while, transcribe synthetic sample audio, run sync, ASR, and Codex postprocessing end to end, show where the sample outputs were written, and then explain the optional nightly automatic run in plain language.

The detailed installer and operating guide lives in [`skills/skill_intake.md`](skills/skill_intake.md). Human readers normally do not need to run commands from this README; the skill file contains the exact playbook an AI agent should follow.

## What It Does

Intake Skill is intentionally narrow. It reads Apple Voice Memos files from the standard macOS Voice Memos container, copies or converts them into `data/YYYYMMDD/`, transcribes them into `transcript_YYYYMMDD.csv`, and generates daily artifacts from that transcript.

It does not record microphone audio. It does not add non-Voice-Memos intake. It does not perform speaker recognition, diarization, reference voice matching, or participant attribution.

## Runtime Boundary

MLX ASR is intended to run locally after `mlx-whisper` and its model are installed. Codex postprocessing is the default AI summarization path for this workflow and uses the operator's configured local Codex CLI. Installer agents should validate Codex postprocessing on synthetic sample audio during setup.

The nightly automatic run is optional and should be enabled only after the operator confirms it. If enabled, the Mac must stay awake at the scheduled time, remain plugged in or otherwise powered, and Voice Memos must keep syncing often enough for new recordings to appear locally.

## For AI Agents

Use [`skills/skill_intake.md`](skills/skill_intake.md) as the source of truth for installation, verification, operation, debugging, command reference, and artifact contracts.
