from __future__ import annotations

import importlib
from datetime import datetime


cron = importlib.import_module("intake_skill.cron")


def test_cron_dry_run_appends_midnight_line(tmp_path) -> None:
    summary = cron.append_cron(tmp_path, dry_run=True, current="MAILTO=me@example.com\n")
    assert summary["dry_run"] is True
    assert "0 0 * * *" in summary["cron_line"]
    assert "--asr-engine mlx --postprocess-engine codex" in summary["cron_line"]
    assert cron.CRON_MARKER in summary["new_crontab"]
    assert "MAILTO=me@example.com" in summary["new_crontab"]


def test_cron_dry_run_does_not_duplicate_marker(tmp_path) -> None:
    line = cron.cron_line(tmp_path)
    summary = cron.append_cron(tmp_path, dry_run=True, current=f"{line}\n")
    assert summary["already_present"] is True
    assert summary["new_crontab"].count(cron.CRON_MARKER) == 1


def test_backup_path_never_overwrites(tmp_path) -> None:
    logs = tmp_path / "logs"
    logs.mkdir()
    now = datetime(2026, 5, 12, 1, 2, 3)
    first = cron.backup_path(tmp_path, now=now)
    first.write_text("old", encoding="utf-8")
    second = cron.backup_path(tmp_path, now=now)
    assert first != second
    assert not second.exists()
