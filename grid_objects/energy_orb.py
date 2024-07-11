from PPlay.sprite import Sprite

from .grid_object import GridObject

from utils import Vector
from core.global_data import GlobalData as GD

from math import cos, pi

class EnergyOrb(GridObject):
    def __init__(self, x, y, cell_size, grid_id):
        super().__init__(x, y, cell_size, grid_id)
        self.window = GD.get_window()

        self.og_pos = Vector(x, y)
        self.speed = Vector(0, 0)
        self.collected = False

        self.float_amplitude = 4
        self.theta = 0
        self.float_speed = 4
        self.float_anchor = y

        self.add_sprite("default", f"assets/sprites/grid_objects/collectables/energy_orb{cell_size}.png", 6, 100, False)
        self.get_sprite("default").playing = False

        self.set_action("default", play=False)

        self.add_sound("pickup", "assets/sounds/sfx/energy_orb_pickup.ogg", 20)
    
    def reset(self):
        super().reset()
        self.collected = False
        self.speed.y = 0
        self.set_action("default", play=False)

    def collect(self):
        self.collected = True
        self.speed.y = -1000
        self.get_sprite("default").playing = True
        self.play_sound("pickup")

    def update(self):
        if self.collected:
            self.y += self.speed.y * self.window.delta_time()
        else:
            self.theta += self.float_speed * self.window.delta_time()
            if self.theta >= 2 * pi:
                self.theta = 0
            self.y = self.float_anchor + self.float_amplitude * cos(self.theta)
        super().update()

    def draw(self):
        self.sprite.draw()