from __future__ import annotations

import csv
import importlib
import json
from pathlib import Path
from typing import Any, cast


def day_dir(data_dir: Path, day: str) -> Path:
    return data_dir / day


def transcript_path(data_dir: Path, day: str) -> Path:
    return day_dir(data_dir, day) / f"transcript_{day}.csv"


def audio_files_for_day(data_dir: Path, day: str) -> list[Path]:
    directory = day_dir(data_dir, day)
    if not directory.exists():
        return []
    return sorted(path for path in directory.glob("*.m4a") if path.is_file())


def write_transcript(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["speaker", "content"], extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({"speaker": row.get("speaker", ""), "content": row.get("content", "")})


def run_mock_asr(data_dir: Path, day: str, mock_text: str | None = None) -> dict[str, object]:
    files = audio_files_for_day(data_dir, day)
    rows = [
        {"speaker": "", "content": mock_text or f"Mock transcript for {path.name}."}
        for path in files
    ]
    output = transcript_path(data_dir, day)
    write_transcript(rows, output)
    return {"command": "asr", "engine": "mock", "day": day, "audio_count": len(files), "output_path": str(output)}


def run_mlx_asr(data_dir: Path, day: str) -> dict[str, object]:
    try:
        mlx_whisper = importlib.import_module("mlx_whisper")
    except ImportError as exc:
        raise RuntimeError("mlx engine requires mlx-whisper to be installed in this environment") from exc

    rows: list[dict[str, str]] = []
    for path in audio_files_for_day(data_dir, day):
        transcribe = cast(Any, mlx_whisper).transcribe
        result = cast(dict[str, object], transcribe(str(path)))
        rows.append({"speaker": "", "content": str(result.get("text", "")).strip()})
    output = transcript_path(data_dir, day)
    write_transcript(rows, output)
    return {"command": "asr", "engine": "mlx", "day": day, "audio_count": len(rows), "output_path": str(output)}


def run_asr(data_dir: Path, day: str, engine: str = "mock", mock_text: str | None = None) -> dict[str, object]:
    if engine == "mock":
        return run_mock_asr(data_dir, day, mock_text=mock_text)
    if engine == "mlx":
        return run_mlx_asr(data_dir, day)
    raise ValueError(f"unsupported ASR engine: {engine}")


def dumps_summary(summary: dict[str, object]) -> str:
    return json.dumps(summary, indent=2, sort_keys=True)
