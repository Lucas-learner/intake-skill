from __future__ import annotations

import json
import math
import shutil
import subprocess
import wave
from pathlib import Path


def write_wave(path: Path, seconds: float = 10.0, sample_rate: int = 16_000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = int(seconds * sample_rate)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        for index in range(frames):
            value = int(16_000 * math.sin(2 * math.pi * 440 * index / sample_rate))
            handle.writeframesraw(value.to_bytes(2, byteorder="little", signed=True))


def make_sample_audio(output: Path, seconds: float = 10.0) -> dict[str, object]:
    output.parent.mkdir(parents=True, exist_ok=True)
    say = shutil.which("say")
    ffmpeg = shutil.which("ffmpeg")
    if say and ffmpeg and output.suffix.lower() == ".m4a":
        temp_aiff = output.with_suffix(".aiff")
        subprocess.run([say, "-o", str(temp_aiff), "This is synthetic sample audio for intake skill testing."], check=True)
        subprocess.run([ffmpeg, "-y", "-stream_loop", "3", "-i", str(temp_aiff), "-t", str(seconds), str(output)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        temp_aiff.unlink(missing_ok=True)
        return {"command": "make-sample-audio", "engine": "say+ffmpeg", "output_path": str(output), "seconds": seconds}
    wave_output = output if output.suffix.lower() == ".wav" else output.with_suffix(".wav")
    write_wave(wave_output, seconds=seconds)
    return {"command": "make-sample-audio", "engine": "python-wave", "output_path": str(wave_output), "seconds": seconds}


def dumps_summary(summary: dict[str, object]) -> str:
    return json.dumps(summary, indent=2, sort_keys=True)
