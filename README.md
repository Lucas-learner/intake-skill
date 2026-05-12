# Intake Skill

Intake Skill turns Apple Voice Memos that have already synced to a Mac into dated local intake artifacts: normalized audio files, transcript CSVs, daily Markdown and HTML reports, and meeting-note Markdown files.

This repo is meant to be installed by an AI agent. Give the agent this URL:

```text
https://github.com/grapeot/intake-skill
```

Ask it: "Install this repo for me: https://github.com/grapeot/intake-skill". The agent should clone the repo, install it, configure the local Voice Memos path, verify real local ASR, validate sample audio end to end, and only then discuss optional Codex postprocessing or nightly cron.

The detailed installer and operating guide lives in [`skills/skill_intake.md`](skills/skill_intake.md). Human readers normally do not need to run commands from this README; the skill file contains the exact playbook an AI agent should follow.

## What It Does

Intake Skill is intentionally narrow. It reads Apple Voice Memos files from the standard macOS Voice Memos container, copies or converts them into `data/YYYYMMDD/`, transcribes them into `transcript_YYYYMMDD.csv`, and generates daily artifacts from that transcript.

It does not record microphone audio. It does not add non-Voice-Memos intake. It does not perform speaker recognition, diarization, reference voice matching, or participant attribution.

## Privacy Boundary

Mock postprocessing and MLX ASR are intended to run locally. Codex postprocessing is different: `postprocess --engine codex` sends transcript content to the external service used by the local Codex CLI. Use Codex mode only after the operator accepts that boundary.

Cron is optional. If enabled, the Mac must stay awake at the scheduled time, and Voice Memos must remain running or syncing often enough for new recordings to appear locally.

## For AI Agents

Use [`skills/skill_intake.md`](skills/skill_intake.md) as the source of truth for installation, verification, operation, debugging, command reference, and artifact contracts.
