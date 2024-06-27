from PPlay.sprite import Sprite

from .grid_object import GridObject

from utils import Vector
from core.global_data import GlobalData as GD

class EnergyOrb(GridObject):
    def __init__(self, x, y, cell_size, grid_id):
        super().__init__(x, y, cell_size, grid_id)
        self.window = GD.get_window()

        self.og_pos = Vector(x, y)
        self.speed = Vector(0, 0)
        self.collected = False

        self.add_sprite("default", f"assets/grid_objects/collectables/energy_orb{cell_size}.png", 6, 100, False)
        self.get_sprite("default").playing = False

        self.set_action("default", play=False)
    
    def reset(self):
        super().reset()
        self.collected = False
        self.speed.y = 0
        self.set_action("default", play=False)

    def collect(self):
        self.collected = True
        self.speed.y = -1000
        self.get_sprite("default").playing = True

    def update(self):
        self.y += self.speed.y * self.window.delta_time()
        super().update()

    def draw(self):
        self.sprite.draw()