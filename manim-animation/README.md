# manim-animation

Shippable Cursor / Claude Code skill for Manim Community Edition. This folder is the installable skill; the parent repo adds render tooling.

## Install

**Cursor (personal):**

```powershell
xcopy /E /I "manim-animation" "%USERPROFILE%\.cursor\skills\manim-animation"
```

**Cursor / Claude (per project):**

```text
.cursor/skills/manim-animation/
```

Copy this entire `manim-animation` folder there.

## Use

Invoke `@manim-animation` (Cursor) or reference the skill when asking for Manim scenes.

When working inside the **Manim_Skill** repo root, follow `references/rendering.md` — `scripts/render.py` handles frame and video output.

Prereqs on the machine: Python venv with `manim`, ffmpeg, LaTeX (for `MathTex`).

## Contents

- `SKILL.md` — main rules and BAD/GOOD patterns
- `references/` — optional short refs (load on demand)
- `references/rendering.md` — repo-specific setup and render commands
