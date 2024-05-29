from PPlay.gameobject import GameObject
from PPlay.sprite import Sprite

from common import GlobalData as GD

class GridObject(GameObject):
    def __init__(self, x, y, cell_size, active):
        super().__init__()
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.active = active