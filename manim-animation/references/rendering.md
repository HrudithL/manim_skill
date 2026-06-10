# Rendering (Manim_Skill repo)

This repo ships scripts so Claude (or you) can write scenes and render without guessing paths.

## One-time setup

```powershell
.\setup.ps1
```

Or manually:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/check_deps.py
```

Requires on PATH (or via `MIKTEX_BIN` / `FFMPEG_BIN` env vars):

- **ffmpeg** — video encode
- **latex** — `MathTex` / `Tex` (MiKTeX or TeX Live)

## Agent workflow

1. Run `python scripts/check_deps.py` — stop and report FAIL items if any.
2. Write scene to `scenes/{name}.py` — one `Scene` / `ThreeDScene` / `MovingCameraScene` class per file.
3. Render last frame (fast check): `python scripts/render.py scenes/{name}.py`
4. Render video: `python scripts/render.py scenes/{name}.py --video`
5. Output lands in `outputs/{name}/` — read PNG or open MP4 for visual review.

## Frame capture when final animation is FadeOut

```powershell
python scripts/render.py scenes/foo.py --frame-end 2
```

`--frame-end N` maps to Manim `-n 0,N` (inclusive play/wait index). End on content still visible.

## Quality flags (video only)

`--quality l|m|h|k` → `-ql` / `-qm` / `-qh` / `-qk`.

## When rendering fails in cloud / sandbox

Manim needs a local Python venv, OpenGL-capable display (or OS software GL), ffmpeg, and LaTeX for math text. Remote sandboxes often lack GPU/display — render on the developer machine instead:

1. Clone repo locally.
2. Run `setup.ps1` and `check_deps.py`.
3. Agent writes `scenes/*.py`; user or agent runs `scripts/render.py` locally.

Headless Linux: install `xvfb` and prefix renders with `xvfb-run` if needed.

## Direct manim CLI (alternative)

```powershell
python -m manim -ql scenes/example_circle.py ExampleCircle
python -m manim -ql --save_last_frame scenes/example_circle.py ExampleCircle
```

Use `scripts/render.py` when you want outputs copied to `outputs/` automatically.
