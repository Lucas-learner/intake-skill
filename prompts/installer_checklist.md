# Installer Checklist Prompt

You are installing `intake_skill` for a Mac user.

First verify the package:

```bash
uv pip install -e '.[dev]'
python -m pytest -q
python -m intake_skill doctor
```

Then preview private-data operations before running them:

```bash
python -m intake_skill sync --dry-run
python -m intake_skill install-cron --dry-run
```

Warn the operator that Codex postprocessing sends transcript content to an external service, and that cron only works when the Mac is awake and Voice Memos is syncing locally.
