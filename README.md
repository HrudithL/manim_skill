# Manim_Skill

Standalone shippable skill for **Manim Community Edition** — write scenes, render frames/videos, review output. Sibling of [Manim-Test](../Manim-Test): that repo keeps the eval harness and a frozen copy of this skill under `ship/manim-animation/` for comparison.

## Quick start

```powershell
cd Manim_Skill
.\setup.ps1
```

Then install the skill into Cursor:

```powershell
xcopy /E /I "manim-animation" "%USERPROFILE%\.cursor\skills\manim-animation"
```

Or per-project: `.cursor/skills/manim-animation/`

## Layout

| Path | Purpose |
|------|---------|
| `manim-animation/` | Installable skill (`SKILL.md` + references) |
| `scenes/` | Scene `.py` files — agent writes here |
| `scripts/check_deps.py` | Verify venv, manim, ffmpeg, latex |
| `scripts/render.py` | Render PNG (last frame) or MP4 → `outputs/` |
| `outputs/` | Render artifacts (gitignored) |

## Render commands

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/check_deps.py
python scripts/render.py scenes/example_circle.py
python scripts/render.py scenes/example_circle.py --video
python scripts/render.py scenes/foo.py --frame-end 2   # when final play is FadeOut
```

## Agent loop

1. Read `@manim-animation` skill (or project-installed copy).
2. `python scripts/check_deps.py` — report any FAIL before claiming render works.
3. Write `scenes/{name}.py`.
4. `python scripts/render.py scenes/{name}.py` — inspect `outputs/{name}/`.
5. Fix scene using skill gotchas; re-render until good.
6. Optional: `--video` for full MP4.

## Prerequisites

| Dependency | Why |
|------------|-----|
| Python 3.10+ | Manim |
| `manim` (pip) | Scene runtime |
| ffmpeg | Video encode |
| LaTeX (MiKTeX / TeX Live) | `MathTex` |

Set `FFMPEG_BIN` or `MIKTEX_BIN` if binaries are not on default PATH.

## When rendering is not possible

Cloud agents and some sandboxes lack OpenGL/display, ffmpeg, or LaTeX. Manim is **local-render** software.

**What works today:** On your Windows machine (verified): ffmpeg + MiKTeX on PATH, venv with manim → `scripts/render.py` produces PNG/MP4.

**If the agent cannot render in-session:**

1. Agent still writes `scenes/*.py` following the skill.
2. You run `setup.ps1` once locally, then `python scripts/render.py ...`.
3. Share the output PNG/MP4 back into chat for visual review.

**Headless Linux:** Install `xvfb` and run `xvfb-run python scripts/render.py ...`.

**CI (optional):** Add a workflow that runs `setup.sh`, `check_deps.py`, and `render.py` on `scenes/example_circle.py` — same scripts, no harness required.

## Relation to Manim-Test

- **Manim-Test** — full eval loop (corpus, harness, skill iterations, `ship/` snapshot).
- **Manim_Skill** — production skill + minimal tooling to build and render. No corpus or benchmark harness.
