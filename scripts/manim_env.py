"""PATH helpers so manim subprocesses find ffmpeg + LaTeX when using the project venv."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV_SCRIPTS = ROOT / ".venv" / "Scripts"
VENV_BIN = ROOT / ".venv" / "bin"


def _env_path(name: str) -> Path | None:
    value = os.environ.get(name, "").strip()
    return Path(value) if value else None


MIKTEX_CANDIDATES = [
    _env_path("MIKTEX_BIN"),
    Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64",
    Path(r"C:\Program Files\MiKTeX\miktex\bin\x64"),
    Path(r"C:\texlive\2024\bin\windows"),
    Path(r"C:\texlive\2025\bin\windows"),
]

FFMPEG_CANDIDATES = [
    _env_path("FFMPEG_BIN"),
    Path(r"C:\ffmpeg\bin"),
    VENV_SCRIPTS,
    VENV_BIN,
]


def _first_existing_dir(candidates: list[Path | None]) -> Path | None:
    for path in candidates:
        if path is not None and path.is_dir():
            return path
    return None


def build_path() -> str:
    prepend: list[str] = []
    for venv_bin in (VENV_SCRIPTS, VENV_BIN):
        if venv_bin.is_dir():
            s = str(venv_bin)
            if s not in prepend:
                prepend.append(s)

    miktex = _first_existing_dir(MIKTEX_CANDIDATES)
    if miktex:
        prepend.append(str(miktex))

    ffmpeg = _first_existing_dir(FFMPEG_CANDIDATES)
    if ffmpeg and str(ffmpeg) not in prepend:
        prepend.append(str(ffmpeg))

    return os.pathsep.join(prepend + [os.environ.get("PATH", "")])


def manim_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PATH"] = build_path()
    return env
