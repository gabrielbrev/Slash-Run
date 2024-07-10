from .grid_object import GridObject

from time import time

class Spike(GridObject):
    def __init__(self, x, y, cell_size, grid_id):
        super().__init__(x, y, cell_size, grid_id, False)

        self.damaged_player = False

        self.add_sprite("default", f"assets/sprites/grid_objects/spike/default{cell_size * 2}.png", 1)

        self.set_action("default")

        self.set_sprite_anchor(-cell_size/2, -cell_size)

    def damage_player(self):
        self.damaged_player = True
            