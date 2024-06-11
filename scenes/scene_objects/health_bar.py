from .bar import Bar

class HealthBar(Bar):
    def __init__(self):
        super().__init__(5, "assets/scene_objects/game/health_bar.png", 6)
