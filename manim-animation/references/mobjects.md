# Mobjects



- Use `Axes` + `c2p(x, y)` for plotted data; avoid screen-space `move_to(np.array(...))`.

- `BackgroundRectangle` behind `MathTex` when drawing over busy backgrounds.

- Labels: `next_to(mob, direction, buff=0.2)` with `buff` large enough to avoid tick overlap.

