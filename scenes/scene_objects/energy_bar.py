from .bar import Bar

class EnergyBar(Bar):
    def __init__(self):
        super().__init__(0, "assets/scene_objects/game/energy_bar.png", 11)
