from __future__ import annotations

import importlib
import os
from datetime import datetime
from pathlib import Path


sync = importlib.import_module("intake_skill.sync")


def write_recording(path: Path, stamp: datetime) -> None:
    path.write_bytes(b"fake-audio")
    timestamp = stamp.timestamp()
    os.utime(path, (timestamp, timestamp))


def test_sync_dry_run_plans_without_writing(tmp_path) -> None:
    source = tmp_path / "source"
    data = tmp_path / "data"
    source.mkdir()
    write_recording(source / "memo.m4a", datetime(2026, 5, 12, 9, 30))

    summary = sync.sync_voice_memos(source, data, dry_run=True)

    assert summary["counts"]["copy"] == 1
    destination = data / "20260512" / "20260512_0930_watch.m4a"
    assert not destination.exists()


def test_sync_is_idempotent_when_destination_exists(tmp_path) -> None:
    source = tmp_path / "source"
    data = tmp_path / "data"
    source.mkdir()
    write_recording(source / "memo.m4a", datetime(2026, 5, 12, 9, 30))

    first = sync.sync_voice_memos(source, data, dry_run=False)
    second = sync.sync_voice_memos(source, data, dry_run=False)

    assert first["counts"]["copy"] == 1
    assert second["counts"]["skip"] == 1
    assert sync.build_sync_plan(source, data)[0].action == "skip"


def test_sync_date_filter_limits_plan_to_one_day(tmp_path) -> None:
    source = tmp_path / "source"
    data = tmp_path / "data"
    source.mkdir()
    write_recording(source / "may12.m4a", datetime(2026, 5, 12, 9, 30))
    write_recording(source / "may13.m4a", datetime(2026, 5, 13, 9, 30))

    summary = sync.sync_voice_memos(source, data, dry_run=True, day="20260512")

    assert summary["day"] == "20260512"
    assert summary["counts"]["copy"] == 1
    assert len(summary["items"]) == 1
    assert "may12.m4a" in summary["items"][0]["source"]
    assert "may13.m4a" not in summary["items"][0]["source"]
