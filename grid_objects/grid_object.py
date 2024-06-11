from PPlay.gameobject import GameObject
from PPlay.sprite import Sprite

from core.global_data import GlobalData as GD

class GridObject(GameObject):
    def __init__(self, x, y, cell_size, grid_id, fragile = False):
        super().__init__()
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.grid_id = grid_id
        self.fragile = fragile
        self.destroyed = False

    def destroy(self):
        self.destroyed = True
