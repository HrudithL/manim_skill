# One-time setup for Manim_Skill (Windows)
$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot

Write-Host "Creating venv..."
python -m venv "$Root\.venv"

$pip = "$Root\.venv\Scripts\pip.exe"
$python = "$Root\.venv\Scripts\python.exe"

Write-Host "Installing requirements..."
& $pip install --upgrade pip
& $pip install -r "$Root\requirements.txt"

Write-Host "Checking dependencies..."
& $python "$Root\scripts\check_deps.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nFix FAIL items above (ffmpeg, MiKTeX), then re-run setup.ps1 or check_deps.py"
    exit $LASTEXITCODE
}

Write-Host "`nSmoke render..."
& $python "$Root\scripts\render.py" "$Root\scenes\example_circle.py"
Write-Host "Done. Install skill: copy manim-animation to .cursor\skills\manim-animation"
