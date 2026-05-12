from __future__ import annotations

import json
import shlex
import subprocess
from datetime import datetime
from pathlib import Path


CRON_MARKER = "# intake_skill midnight run"


def cron_line(repo_root: Path) -> str:
    python_path = repo_root / ".venv" / "bin" / "python"
    log_path = repo_root / "logs" / "intake_cron.log"
    return (
        "0 0 * * * "
        f"cd {shlex.quote(str(repo_root))} && "
        f"{shlex.quote(str(python_path))} -m intake_skill run-day >> {shlex.quote(str(log_path))} 2>&1 "
        f"{CRON_MARKER}"
    )


def backup_path(repo_root: Path, now: datetime | None = None) -> Path:
    stamp = (now or datetime.now()).strftime("%Y%m%d_%H%M%S")
    base = repo_root / "logs" / f"crontab_backup_{stamp}.txt"
    if not base.exists():
        return base
    index = 1
    while True:
        candidate = repo_root / "logs" / f"crontab_backup_{stamp}_{index}.txt"
        if not candidate.exists():
            return candidate
        index += 1


def read_current_crontab() -> str:
    result = subprocess.run(["crontab", "-l"], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return result.stdout
    if "no crontab" in result.stderr.lower():
        return ""
    raise RuntimeError(result.stderr.strip() or "failed to read current crontab")


def append_cron(repo_root: Path, dry_run: bool = False, current: str | None = None) -> dict[str, object]:
    line = cron_line(repo_root)
    existing = read_current_crontab() if current is None and not dry_run else (current or "")
    already_present = CRON_MARKER in existing or line in existing
    new_crontab = existing.rstrip("\n")
    if not already_present:
        new_crontab = f"{new_crontab}\n{line}\n" if new_crontab else f"{line}\n"
    path = backup_path(repo_root)
    summary: dict[str, object] = {
        "command": "install-cron",
        "dry_run": dry_run,
        "already_present": already_present,
        "cron_line": line,
        "backup_path": str(path),
    }
    if dry_run:
        summary["new_crontab"] = new_crontab
        return summary
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(existing, encoding="utf-8")
    subprocess.run(["crontab", "-"], input=new_crontab, text=True, check=True)
    return summary


def dumps_summary(summary: dict[str, object]) -> str:
    return json.dumps(summary, indent=2, sort_keys=True)
