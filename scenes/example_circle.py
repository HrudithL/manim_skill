from manim import *


class ExampleCircle(Scene):
    def construct(self):
        title = Text("Manim_Skill example").to_edge(UP)
        circle = Circle(color=BLUE)
        self.play(FadeIn(title), FadeIn(circle))
        self.wait(0.5)
