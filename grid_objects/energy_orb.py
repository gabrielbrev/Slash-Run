from PPlay.sprite import Sprite

from .grid_object import GridObject

from common import Vector
from common import GlobalData as GD

class EnergyOrb(GridObject):
    def __init__(self, x, y, cell_size, active):
        super().__init__(x, y, cell_size, active)
        self.window = GD.get_window()

        self.speed = Vector(0, 0)
        self.collected = False

        self.sprite = Sprite(f"assets/collectables/energy_orb{cell_size}.png", 6)
        self.sprite.playing = False
        self.sprite.set_loop(False)
        self.sprite.set_total_duration(100)
        self.sprite.set_position(x, y)

        self.width = self.sprite.width
        self.height = self.sprite.height
    
    def collect(self):
        self.collected = True
        self.speed.y = -1000
        self.sprite.playing = True

    def update(self):
        self.y += self.speed.y * self.window.delta_time()
        self.sprite.set_position(self.x, self.y)
        self.sprite.update()

    def draw(self):
        self.sprite.draw()