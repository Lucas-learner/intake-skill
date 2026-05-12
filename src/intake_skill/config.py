from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_SOURCE_DIR = "~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/"


@dataclass(frozen=True)
class IntakeConfig:
    source_dir: Path
    data_dir: Path
    repo_root: Path


def package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def expand_path(value: str | Path) -> Path:
    return Path(value).expanduser().resolve()


def load_config(
    source_dir: str | Path | None = None,
    data_dir: str | Path | None = None,
    repo_root: str | Path | None = None,
) -> IntakeConfig:
    root = expand_path(repo_root or os.environ.get("INTAKE_REPO_ROOT") or package_root())
    source = expand_path(source_dir or os.environ.get("INTAKE_SOURCE_DIR") or DEFAULT_SOURCE_DIR)
    data = expand_path(data_dir or os.environ.get("INTAKE_DATA_DIR") or root / "data")
    return IntakeConfig(source_dir=source, data_dir=data, repo_root=root)
