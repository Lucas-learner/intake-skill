from __future__ import annotations

import importlib
import json
import os
from datetime import datetime


cli = importlib.import_module("intake_skill.cli")


def test_run_day_syncs_and_generates_mock_artifacts(tmp_path, capsys) -> None:
    source = tmp_path / "source"
    data = tmp_path / "data"
    source.mkdir()
    audio = source / "memo.m4a"
    audio.write_bytes(b"fake-audio")
    stamp = datetime(2026, 5, 12, 9, 30).timestamp()
    os.utime(audio, (stamp, stamp))
    other_audio = source / "other-day.m4a"
    other_audio.write_bytes(b"fake-audio")
    other_stamp = datetime(2026, 5, 13, 9, 30).timestamp()
    os.utime(other_audio, (other_stamp, other_stamp))

    code = cli.main([
        "run-day",
        "--date",
        "20260512",
        "--source",
        str(source),
        "--data-dir",
        str(data),
        "--repo-root",
        str(tmp_path),
        "--asr-engine",
        "mock",
        "--postprocess-engine",
        "mock",
        "--mock-text",
        "Run-day controlled mock text.",
    ])

    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["command"] == "run-day"
    day_dir = data / "20260512"
    assert (day_dir / "20260512_0930_watch.m4a").exists()
    assert (day_dir / "transcript_20260512.csv").exists()
    assert (day_dir / "daily_20260512.md").exists()
    assert not (data / "20260513").exists()
    assert "Run-day controlled mock text" in (day_dir / "transcript_20260512.csv").read_text(encoding="utf-8")


def test_make_sample_audio_fallback_creates_file(tmp_path, capsys) -> None:
    output = tmp_path / "sample.wav"
    code = cli.main(["make-sample-audio", "--output", str(output), "--seconds", "0.1", "--repo-root", str(tmp_path)])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["command"] == "make-sample-audio"
    assert output.exists()
    assert output.stat().st_size > 0
