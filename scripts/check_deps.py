"""Verify Python venv, Manim, ffmpeg, and LaTeX before rendering."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim_env import build_path, manim_env  # noqa: E402


def _ok(msg: str) -> None:
    print(f"  OK   {msg}")


def _fail(msg: str) -> None:
    print(f"  FAIL {msg}")


def check() -> int:
    print("Manim_Skill dependency check\n")
    issues: list[str] = []

    venv_python = ROOT / ".venv" / ("Scripts" if sys.platform == "win32" else "bin") / (
        "python.exe" if sys.platform == "win32" else "python"
    )
    if venv_python.is_file():
        _ok(f"venv at {ROOT / '.venv'}")
    else:
        _fail("no .venv — run setup.ps1 or: python -m venv .venv && pip install -r requirements.txt")
        issues.append("venv")

    try:
        import manim  # noqa: F401

        _ok(f"manim {manim.__version__} (import)")
    except ImportError:
        _fail("manim not installed in active Python")
        issues.append("manim")

    path = build_path()
    ffmpeg = shutil.which("ffmpeg", path=path)
    if ffmpeg:
        _ok(f"ffmpeg ({ffmpeg})")
    else:
        _fail("ffmpeg not on PATH — install ffmpeg and add bin to PATH or set FFMPEG_BIN")
        issues.append("ffmpeg")

    latex = shutil.which("latex", path=path)
    if latex:
        _ok(f"latex ({latex})")
    else:
        _fail("latex not on PATH — install MiKTeX or TeX Live (needed for MathTex)")
        issues.append("latex")

    try:
        r = subprocess.run(
            [sys.executable, "-m", "manim", "--version"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=ROOT,
            env=manim_env(),
        )
        if r.returncode == 0:
            ver = (r.stdout or r.stderr).strip().splitlines()[0]
            _ok(f"manim CLI ({ver})")
        else:
            _fail("manim CLI failed")
            issues.append("manim-cli")
    except Exception as exc:
        _fail(f"manim CLI error: {exc}")
        issues.append("manim-cli")

    print()
    if issues:
        print("Fix the FAIL items above, then re-run: python scripts/check_deps.py")
        return 1
    print("All checks passed. Render with: python scripts/render.py scenes/example_circle.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
