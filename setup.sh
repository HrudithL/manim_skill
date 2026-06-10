#!/usr/bin/env bash
# One-time setup for Manim_Skill (macOS / Linux)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"

python3 -m venv "$ROOT/.venv"
"$ROOT/.venv/bin/pip" install --upgrade pip
"$ROOT/.venv/bin/pip" install -r "$ROOT/requirements.txt"
"$ROOT/.venv/bin/python" "$ROOT/scripts/check_deps.py"
"$ROOT/.venv/bin/python" "$ROOT/scripts/render.py" "$ROOT/scenes/example_circle.py"
echo "Done. Install skill: copy manim-animation to .cursor/skills/manim-animation"
