---
name: manim-animation
description: >-
  Write and debug Manim Community Edition Python scenes — axes, plots, 3D,
  updaters, camera, pacing. Use when user asks for Manim animations, math
  videos, scene.py, or manim render. In Manim_Skill repo: use scripts/render.py
  after writing scenes/*.py.
---

# Manim Animation Skill

## Repo workflow (Manim_Skill)

When this skill lives in the **Manim_Skill** standalone repo:

1. `python scripts/check_deps.py` — verify venv, manim, ffmpeg, latex.
2. Write scenes under `scenes/{name}.py` (one scene class per file).
3. Quick visual check: `python scripts/render.py scenes/{name}.py` → `outputs/{name}/{name}.png`
4. Full video: `python scripts/render.py scenes/{name}.py --video` → `outputs/{name}/*.mp4`
5. If final `play()` is `FadeOut`, use `--frame-end N` so the PNG is not blank.

Details: [rendering.md](references/rendering.md)

## Workflow

1. One `Scene` / `ThreeDScene` / `MovingCameraScene` class per file.
2. Import: `from manim import *`
3. Render: `python scripts/render.py scenes/your_file.py` (this repo) or `manim -ql your_file.py YourSceneClass`
4. Prereqs on PATH: `manim`, ffmpeg, LaTeX (for `MathTex`).

## Pre-Flight Checklist

- [ ] Use raw strings for `MathTex` / `Tex`: `r"..."`
- [ ] Never `self.add(x)` then `FadeIn(x)` on same object — object already on screen
- [ ] Use `ReplacementTransform` when old content must disappear
- [ ] `ThreeDScene` for `set_camera_orientation`; `MovingCameraScene` for `self.camera.frame`
- [ ] Position labels with `next_to` / `to_edge`, not `to_corner().shift()` into axes
- [ ] Titles above 2D `Axes`: `to_edge(UP)` — never `to_corner(UL)` (collides with plot)
- [ ] `Surface()` / parametric 3D plots require `ThreeDScene`, not plain `Scene`
- [ ] Polygon/data vertices: map with `ax.c2p(*coords)` — no hardcoded screen coords
- [ ] Updater-moved dots: line must `become(Line(...))` each frame — static `Line` disconnects
- [ ] HUD in 3D: `add_fixed_in_frame_mobjects()` before `self.begin_ambient_camera_rotation()` / rotate
- [ ] Staged scenes: end with key content visible — avoid trailing `FadeOut` of everything
- [ ] Explicit `self.wait(seconds)` per stage for pacing; fade out stage N before stage N+1
- [ ] Use `ax.c2p()` for data coordinates, not hardcoded `np.array` positions
- [ ] Clear updaters before conflicting animations
- [ ] Leave room for title: axes `x_length` ≤ 10 when title above
- [ ] One `.animate` chain per `self.play()` call
- [ ] Update connecting lines when endpoint dots use updaters
- [ ] `add_fixed_in_frame_mobjects()` for HUD text in `ThreeDScene`

## Critical Gotchas

### Double add

# BAD
```python
self.add(circle)
self.play(FadeIn(circle))
```

# GOOD
```python
self.play(FadeIn(circle))
```

### Faded anchor

# BAD
```python
self.play(FadeOut(label))
formula.next_to(label, DOWN)
```

# GOOD
```python
self.play(FadeOut(label))
formula.to_edge(DOWN)
```

### Wrong scene base class

# BAD — 3D in plain Scene
```python
class MyScene(Scene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES)
```

# GOOD
```python
class MyScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES)
```

### Moving camera base class

# BAD
```python
class MyScene(Scene):
    def construct(self):
        self.play(self.camera.frame.animate.scale(0.5))
```

# GOOD
```python
class MyScene(MovingCameraScene):
    def construct(self):
        self.play(self.camera.frame.animate.scale(0.5))
```

### ReplacementTransform vs Transform

# BAD
```python
self.play(Transform(box1, box2))  # SurroundingRectangle overlap
```

# GOOD
```python
self.play(ReplacementTransform(box1, box2))
```

### Raw strings in MathTex

# BAD
```python
MathTex("x^2")
```

# GOOD
```python
MathTex(r"x^2")
```

## Layout and Labels

### Corner + shift overlap

# BAD
```python
title.to_corner(UL).shift(DOWN * 1.2)
ax.to_edge(DOWN)
```

# GOOD
```python
title.to_edge(UP)
ax.next_to(title, DOWN, buff=0.5)
```

### to_corner(UL) for titles above axes

# BAD — title drifts into plot area
```python
title = Text("Functions").to_corner(UL)
ax = Axes(x_range=[-5, 5], x_length=9)
```

# GOOD
```python
title = Text("Functions").to_edge(UP)
ax = Axes(x_range=[-5, 5], x_length=9)
ax.next_to(title, DOWN, buff=0.4)
```

### Y-mean label off-screen

# BAD
```python
label.next_to(ax.c2p(0, y_mean), LEFT)  # y-axis label pushed off-screen
```

# GOOD
```python
label.next_to(ax.c2p(0, y_mean), RIGHT, buff=0.15)
```

### Discarded move_to

# BAD — second move_to overrides the first
```python
dot.move_to(LEFT * 2)
dot.move_to(UP * 2)
```

# GOOD
```python
dot.move_to(LEFT * 2 + UP)
```

### Axes too large for title

# BAD
```python
ax = Axes(x_range=[-10, 10], x_length=12)
```

# GOOD
```python
ax = Axes(x_range=[-5, 5], x_length=9)
```

### Label overlap (vector endpoints)

# BAD
```python
origin_text.move_to(ORIGIN)
tip_text.move_to(ORIGIN)
```

# GOOD
```python
origin_text.next_to(dot, DOWN)
tip_text.next_to(arrow.get_end(), RIGHT)
```

## Plotting

### Hardcoded screen position

# BAD
```python
dot.move_to(np.array([-3, 2, 0]))
```

# GOOD
```python
dot.move_to(ax.c2p(x, func(x)))
```

### Graph labels at same anchor

# BAD
```python
sin_label.move_to(axes.c2p(0, 0))  # get_graph_label-style placement wrong
cos_label.move_to(axes.c2p(0, 0))
```

# GOOD
```python
sin_label.next_to(axes.i2gp(-8, sin_graph), UP)
cos_label.next_to(axes.i2gp(2, cos_graph), UP)
```

### Polygon corners without c2p

# BAD — hardcoded screen coords drift off axes
```python
data_coords = [(1, 1), (3, 1), (2, 3)]
Polygon(*[np.array([x, y, 0]) for x, y in data_coords])
```

# GOOD — always convert data coords via c2p
```python
data_coords = [(1, 1), (3, 1), (2, 3)]
Polygon(*[ax.c2p(*coords) for coords in data_coords])
```

## Animation Patterns

### Split animate chains in one play

# BAD
```python
self.play(sq.animate.shift(LEFT), sq.animate.set_fill(ORANGE))
```

# GOOD
```python
self.play(sq.animate.shift(LEFT))
self.play(sq.animate.set_fill(ORANGE))
```

## Updaters

### Updater not cleared before animate

# BAD
```python
line_moving.add_updater(sync)
self.play(theta.animate.set_value(110))
self.play(line_moving.animate.set_color(RED))
```

# GOOD
```python
self.play(theta.animate.set_value(110))
line_moving.clear_updaters()  # remove_updater / clear_updaters before animate
self.play(line_moving.animate.set_color(RED))
```

### Line not updated when dots move

# BAD — static Line disconnects from moving dots
```python
l1 = Line(d1.get_center(), d2.get_center())
d1.add_updater(...)
d2.add_updater(...)
self.add(d1, d2, l1)
```

# GOOD — line updater prevents visual disconnect
```python
l1.add_updater(lambda z: z.become(Line(d1.get_center(), d2.get_center())))
self.add(d1, d2, l1)
```

## Special Camera

### Fixed-in-frame HUD in 3D

# BAD — HUD rotates with camera, unreadable during rotate
```python
text3d.to_corner(UL)
self.add(axes, text3d)
self.begin_ambient_camera_rotation(rate=0.2)
```

# GOOD — pin HUD before camera rotate
```python
self.add_fixed_in_frame_mobjects(text3d)
text3d.to_corner(UL)
self.add(axes)
self.begin_ambient_camera_rotation(rate=0.2)
```

### Surface in plain Scene

# BAD
```python
class MyScene(Scene):
    def construct(self):
        surface = Surface(lambda u, v: np.array([u, v, u**2 + v**2]))
```

# GOOD
```python
class MyScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)
        surface = Surface(lambda u, v: np.array([u, v, u**2 + v**2]))
        self.add(surface)
```

## Scene Pacing and Frame Capture

### Trailing FadeOut blanks still frames

# BAD — save_last_frame captures empty screen
```python
self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.08))
self.play(FadeOut(dots))
```

# GOOD — end with content visible
```python
self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.08))
self.wait(0.5)
```

### Multi-stage pacing

# BAD — final FadeOut leaves blank frame; no explicit waits
```python
self.play(FadeIn(title))
self.play(FadeOut(title))
self.play(FadeIn(formula))
self.play(FadeOut(formula))
```

# GOOD — timed stages, leave final stage on screen
```python
self.play(FadeIn(title))
self.wait(2)
self.play(FadeOut(title))
self.play(FadeIn(diagram))
self.wait(3)
self.play(FadeOut(diagram))
self.play(FadeIn(formula))
self.wait(2)
```

## Basic Concepts

- VGroup z-order / `z_index` matters when shapes overlap
- Brace labels: `Brace(..., DOWN)` + `Text(...).next_to(brace, DOWN)` — not `get_text()` when avoiding TeX
- NumberPlane + Arrow + coordinate labels via `next_to` on endpoints
- Boolean ops / unions: separate labels with `next_to`, not stacked on same anchor
- Path motion: `ReplacementTransform`, `MoveAlongPath`
- Busy background + `MathTex`: wrap with `BackgroundRectangle(formula, color=BLACK, fill_opacity=0.85)`
- Side-by-side layout: `axes.to_edge(LEFT)`; formula panel `VGroup(...).to_edge(RIGHT, buff=0.5)`

## Additional references

Optional detail — read only when needed:

- [rendering.md](references/rendering.md) — setup, `scripts/render.py`, sandbox limits
- [animations.md](references/animations.md)
- [mobjects.md](references/mobjects.md)
- [colors.md](references/colors.md)
