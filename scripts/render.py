"""Render a Manim scene to PNG (last frame) or MP4.

Usage:
  python scripts/render.py scenes/example_circle.py
  python scripts/render.py scenes/example_circle.py --video
  python scripts/render.py scenes/foo.py --quality m
  python scripts/render.py scenes/foo.py --frame-end 2
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "outputs"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim_env import manim_env  # noqa: E402

QUALITY_FLAGS = {"l": "-ql", "m": "-qm", "h": "-qh", "k": "-qk"}


def get_scene_name(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"class (\w+)\(.*Scene.*\)", text)
    return m.group(1) if m else None


def render_frame(py_path: Path, frame_end: int | None = None) -> Path | None:
    scene = get_scene_name(py_path)
    if not scene:
        print("ERROR: no Scene subclass found in file", file=sys.stderr)
        return None

    stem = py_path.stem
    cmd = [
        sys.executable,
        "-m",
        "manim",
        "-ql",
        "--save_last_frame",
        str(py_path.resolve()),
        scene,
    ]
    if frame_end is not None:
        cmd[4:4] = ["-n", f"0,{frame_end}"]

    r = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=180,
        cwd=ROOT,
        env=manim_env(),
    )
    if r.returncode != 0:
        print((r.stderr or r.stdout)[-2000:], file=sys.stderr)
        return None

    candidates = list((ROOT / "media" / "images" / stem).glob("*.png"))
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def render_video(py_path: Path, quality: str = "l") -> Path | None:
    scene = get_scene_name(py_path)
    if not scene:
        print("ERROR: no Scene subclass found in file", file=sys.stderr)
        return None

    flag = QUALITY_FLAGS.get(quality, "-ql")
    stem = py_path.stem
    cmd = [
        sys.executable,
        "-m",
        "manim",
        flag,
        str(py_path.resolve()),
        scene,
    ]
    r = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600,
        cwd=ROOT,
        env=manim_env(),
    )
    if r.returncode != 0:
        print((r.stderr or r.stdout)[-2000:], file=sys.stderr)
        return None

    videos = list((ROOT / "media" / "videos" / stem).rglob("*.mp4"))
    return max(videos, key=lambda p: p.stat().st_mtime) if videos else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Manim scene from this repo.")
    parser.add_argument("scene", type=Path, help="Path to scene .py file (e.g. scenes/foo.py)")
    parser.add_argument("--video", action="store_true", help="Render MP4 instead of last-frame PNG")
    parser.add_argument(
        "--quality",
        choices=list(QUALITY_FLAGS),
        default="l",
        help="Video quality: l/m/h/k (default: l)",
    )
    parser.add_argument(
        "--frame-end",
        type=int,
        default=None,
        help="Animation index for --save_last_frame (-n 0,N). Use when final play is FadeOut.",
    )
    args = parser.parse_args()

    py_path = args.scene if args.scene.is_absolute() else ROOT / args.scene
    if not py_path.is_file():
        print(f"ERROR: file not found: {py_path}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dest_dir = OUT_DIR / py_path.stem
    dest_dir.mkdir(parents=True, exist_ok=True)

    if args.video:
        result = render_video(py_path, args.quality)
        if not result:
            print("RENDER_FAIL", file=sys.stderr)
            return 1
        dest = dest_dir / result.name
        shutil.copy(result, dest)
        print(dest)
        return 0

    result = render_frame(py_path, args.frame_end)
    if not result:
        print("RENDER_FAIL", file=sys.stderr)
        return 1
    dest = dest_dir / f"{py_path.stem}.png"
    shutil.copy(result, dest)
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
