from PPlay.sprite import Sprite

from .grid_object import GridObject

from core.global_data import GlobalData as GD

from utils import Vector

from time import time

class Ground(GridObject):
    GRAVITY = 500

    # A ground object is 8 times the cell size
    def __init__(self, x, y, tile_width, tile_height, cell_size, grid_id, infinite=False):
        self.SPECIAL_DATA = ["tile_width", "tile_height"]
        super().__init__(x, y, cell_size, grid_id)
        self.tile_size = cell_size * 8
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.width = tile_width * self.tile_size
        self.height = tile_height * self.tile_size
        self.tile_size = self.tile_size
        self.tiles = []
        for i in range(tile_width):
            tile_list = []
            for j in range(tile_height):
                file_format = "png"
                if infinite:
                    if j == 0:
                        name = "top_mid"
                        file_format = "jpeg"
                    else:
                        name = "center_mid"
                        file_format = "jpeg"
                else:
                    if i == tile_width - 1 == 0:
                        if j == 0:
                            name = "top_single"
                        else:
                            name = "center_single"
                    elif i == 0:
                        if j == 0:
                            name = "top_left"
                        else:
                            name = "center_left"
                    elif i == tile_width - 1:
                        if j == 0:
                            name = "top_right"
                        else:
                            name = "center_right"
                    else:
                        if j == 0:
                            name = "top_mid"
                            file_format = "jpeg"
                        else:
                            name = "center_mid"
                            file_format = "jpeg"
                tile = Sprite(f"assets/sprites/grid_objects/ground/{name}{self.tile_size}.{file_format}")
                tile.x = x + i * self.tile_size
                tile.y = y + j * self.tile_size
                tile_list.append(tile)
            self.tiles.append(tile_list)

        self.collapsing = False
        self.speed = Vector(0, 0)

    def collapse(self):
        self.collapsing = True
        self.speed.y += 15

    def update_position(self):
        for i, tile_list in enumerate(self.tiles):
            for j, tile in enumerate(tile_list):
                tile.x = self.x + i * self.tile_size
                tile.y = self.y + j * self.tile_size

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.update_position()

    def update(self):
        self.y += self.speed.y * GD.get_window().delta_time()
        if self.collapsing:
            self.speed.y += Ground.GRAVITY * GD.get_window().delta_time()

        self.update_position()

    def draw(self):
        for tile_list in self.tiles:
            for tile in tile_list:
                match GD.off_screen(tile):
                    case 0:
                        tile.draw()
                    case 1:
                        break
    
        