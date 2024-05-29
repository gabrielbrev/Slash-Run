from PPlay.sprite import Sprite
from PPlay.gameobject import GameObject

from .grid_object import GridObject

from common import GlobalData as GD

class Ground(GridObject):
    # A ground object is 8 times the cell size
    def __init__(self, x, y, width, height, tile_size, cell_size, active):
        super().__init__(x, y, cell_size, active)
        self.width = width * tile_size
        self.height = height * tile_size
        self.tile_size = tile_size
        self.tiles = []
        for i in range(width):
            tile_list = []
            for j in range(height):
                tile = Sprite(f"assets/terrain/ground{tile_size}.jpeg")
                tile.x = x + i * tile_size
                tile.y = y + j * tile_size
                tile_list.append(tile)
            self.tiles.append(tile_list)
        # self.collapse = False

    def update(self):
        for i, tile_list in enumerate(self.tiles):
            for j, tile in enumerate(tile_list):
                tile.x = self.x + i * self.tile_size
                tile.y = self.y + j * self.tile_size

    def draw(self):
        for tile_list in self.tiles:
            for tile in tile_list:
                if GD.on_screen(tile):
                    tile.draw()
    
        